"""
Backend Flask para Video Generator
Conecta a interface HTML com o processamento Python
"""

from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
import json
import threading
import time
from pathlib import Path
import sys
import os
from datetime import datetime

# Fix Windows encoding for emoji output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Importa o video_generator
sys.path.append(str(Path(__file__).parent))

# FORÇA RELOAD para pegar código atualizado
import importlib
if 'video_generator' in sys.modules:
    importlib.reload(sys.modules['video_generator'])

from video_generator import VideoGenerator

app = Flask(__name__, static_folder='.')
CORS(app)

# Estado global do processamento
processing_state = {
    'active': False,
    'current_scene': 0,
    'total_scenes': 0,
    'logs': [],
    'error': None,
    'waiting_browser_confirm': False,
    'cancelled': False,
    'start_time': None,
    'last_heartbeat': None
}

# Evento para sincronização da confirmação do browser
browser_confirm_event = threading.Event()
browser_confirmed_flag = threading.Event()  # NOVO: flag separada para polling

# Lock para thread safety
state_lock = threading.Lock()

# Variável para controlar a thread de processamento
processing_thread = None

# Referência global para o generator atual (para confirmar browsers)
_current_generator = None

# Flag simples compartilhada entre threads (substitui Event complexo)
_browser_confirm = {'confirmed': False}

# Configurações
BROWSER_CONFIRM_TIMEOUT = int(os.getenv('BROWSER_CONFIRM_TIMEOUT', 300))


def add_log(message, log_type='info'):
    """Adiciona log ao estado - SEM lock para evitar deadlock"""
    try:
        timestamp = time.strftime('%H:%M:%S')
        processing_state['logs'].append({
            'timestamp': timestamp,
            'message': message,
            'type': log_type
        })
        processing_state['last_heartbeat'] = time.time()
    except Exception as e:
        print(f"[add_log ERRO] {e}: {message}")


def _set_waiting_browser(waiting):
    """Atualiza o estado de espera por confirmação do browser"""
    with state_lock:
        processing_state['waiting_browser_confirm'] = waiting
        if waiting:
            browser_confirm_event.clear()  # Reseta o evento


def process_roteiro_async(roteiro_data, output_dir):
    """Processa o roteiro em uma thread separada"""
    global _current_generator
    generator = None
    try:
        # FORÇA RELOAD do módulo video_generator DENTRO da thread
        import importlib
        import sys
        if 'video_generator' in sys.modules:
            importlib.reload(sys.modules['video_generator'])
        
        from video_generator import VideoGenerator
        
        with state_lock:
            processing_state['active'] = True
            processing_state['current_scene'] = 0
            processing_state['total_scenes'] = len(roteiro_data['cenas'])
            processing_state['logs'] = []
            processing_state['error'] = None
            processing_state['cancelled'] = False
            processing_state['start_time'] = time.time()

        # Salva roteiro temporário
        temp_json = Path(output_dir) / 'temp_roteiro.json'
        temp_json.parent.mkdir(parents=True, exist_ok=True)
        with open(temp_json, 'w', encoding='utf-8') as f:
            json.dump(roteiro_data, f, indent=2, ensure_ascii=False)

        add_log(f"🎬 Iniciando processamento de {len(roteiro_data['cenas'])} cenas", 'info')
        add_log(f"📋 Projeto: {roteiro_data.get('projeto', 'Sem nome')}", 'info')

        # Cria instância do gerador
        generator = VideoGenerator(output_dir=output_dir)
        
        # Passa o evento de confirmação para o gerador
        generator.browser_confirm_event = browser_confirm_event
        generator.set_waiting_callback(lambda waiting: _set_waiting_browser(waiting))
        
        # Guarda referência global para o Flask endpoint poder confirmar diretamente
        global _current_generator
        _current_generator = generator
        generator._browser_confirm_flag = _browser_confirm  # Flag compartilhada
        
        # Configura navegador
        add_log("🌐 Configurando navegador...", 'info')
        try:
            generator.setup_browser()
            print("[THREAD] setup_browser() retornou - chamando add_log...")
            add_log("✓ Navegador configurado com sucesso", 'success')
            print("[THREAD] add_log chamado com sucesso")
        except Exception as e:
            print(f"[THREAD] ERRO no setup_browser: {e}")
            add_log(f"❌ Erro ao configurar navegador: {str(e)}", 'error')
            with state_lock:
                processing_state['active'] = False
            return
        
        add_log(f"🔍 Iniciando loop de cenas ({len(roteiro_data['cenas'])} cenas)...", 'info')

        # Garante que todos os campos opcionais existem
        for cena in roteiro_data['cenas']:
            if 'use_previous_frame' not in cena:
                cena['use_previous_frame'] = False

        # Processa cada cena
        for i, cena in enumerate(roteiro_data['cenas'], 1):
            # Verifica se foi cancelado
            with state_lock:
                if processing_state['cancelled']:
                    add_log("⚠️ Processamento cancelado pelo usuário", 'warning')
                    break
            
            with state_lock:
                processing_state['current_scene'] = i

            add_log(f"\n{'='*60}", 'separator')
            add_log(f"🎬 PROCESSANDO CENA {i}/{len(roteiro_data['cenas'])}", 'scene')
            add_log(f"{'='*60}", 'separator')

            try:
                # 1. Obter/gerar imagem inicial
                if cena.get('use_previous_frame', False) and generator.last_frame:
                    add_log(f"🔄 Usando último frame da cena anterior", 'info')
                    image_path = generator.last_frame
                else:
                    add_log(f"🎨 Gerando imagem com DALL-E...", 'info')
                    add_log(f"📝 Prompt: {cena['dalle_prompt'][:80]}...", 'detail')
                    try:
                        image_path = generator.generate_image_dalle(
                            cena['dalle_prompt'], 
                            i
                        )
                        add_log(f"✓ Imagem gerada: {image_path}", 'success')
                    except Exception as e:
                        add_log(f"❌ ERRO ao gerar imagem: {str(e)}", 'error')
                        import traceback
                        add_log(f"📋 Traceback: {traceback.format_exc()}", 'error')
                        continue

                # 2. Gerar vídeo no Grok
                add_log(f"\n🎬 Gerando vídeo com Grok Imagine...", 'info')
                add_log(f"📝 Movimento: {cena['grok_movement'][:80]}...", 'detail')
                video_path = generator.generate_video_grok(
                    image_path,
                    cena['grok_movement'],
                    i
                )
                add_log(f"✓ Vídeo gerado", 'success')

                # 2.5 UPSCALING (se habilitado no roteiro)
                upscale_enabled = roteiro_data.get('upscale_videos', True)
                if upscale_enabled:
                    scale_factor = roteiro_data.get('upscale_factor', 2)
                    add_log(f"\n🎨 Fazendo upscaling {scale_factor}x...", 'info')
                    video_path = generator.upscale_video(video_path, i, scale_factor)
                    add_log(f"✓ Upscaling concluído", 'success')

                # 3. Extrair último frame
                add_log(f"\n🖼️ Extraindo último frame...", 'info')
                generator.last_frame = generator.extract_last_frame(video_path, i)
                add_log(f"✓ Frame extraído", 'success')

                add_log(f"✅ Cena {i} concluída!", 'success')

            except Exception as e:
                add_log(f"❌ Erro na cena {i}: {str(e)}", 'error')
                # Continua para próxima cena em vez de abortar tudo
                continue

        # Finalização
        with state_lock:
            if not processing_state['cancelled']:
                add_log(f"\n{'='*60}", 'separator')
                add_log("🎉 PROCESSAMENTO CONCLUÍDO!", 'success')
                add_log(f"📁 Arquivos salvos em: {output_dir}", 'success')
                add_log(f"{'='*60}", 'separator')
            else:
                add_log(f"\n{'='*60}", 'separator')
                add_log("⚠️ PROCESSAMENTO CANCELADO", 'warning')
                add_log(f"{'='*60}", 'separator')

        if generator:
            generator.create_summary()

    except Exception as e:
        add_log(f"❌ ERRO FATAL: {str(e)}", 'error')
        with state_lock:
            processing_state['error'] = str(e)
    finally:
        with state_lock:
            processing_state['active'] = False
        
        # Limpa referência global
        _current_generator = None
        
        # Fecha navegador
        if generator and generator.driver:
            try:
                generator.driver.quit()
                add_log("✓ Navegador fechado", 'info')
            except:
                pass


@app.route('/')
def index():
    """Serve a interface HTML"""
    return send_from_directory('.', 'interface.html')


@app.route('/api/process', methods=['POST'])
def start_processing():
    """Inicia o processamento do roteiro"""
    global processing_thread
    try:
        data = request.json
        
        # Valida dados
        if 'roteiro' not in data:
            return jsonify({'error': 'Roteiro não fornecido'}), 400
        
        roteiro = data['roteiro']
        output_dir = data.get('output_dir', './output')
        
        # Auto-detecta pasta da aula baseado no nome do projeto
        projeto_name = roteiro.get('projeto', '')
        if 'AULA 01' in projeto_name or 'Senta' in projeto_name or 'senta' in projeto_name:
            output_dir = './output/aula_01_senta'
        elif 'AULA 02' in projeto_name or 'Deita' in projeto_name or 'deita' in projeto_name:
            output_dir = './output/aula_02_deita'
        elif 'AULA 03' in projeto_name or 'Fica' in projeto_name or 'fica' in projeto_name:
            output_dir = './output/aula_03_fica'
        elif 'AULA 04' in projeto_name or 'Rola' in projeto_name or 'rola' in projeto_name:
            output_dir = './output/aula_04_rola'
        elif 'AULA 05' in projeto_name or 'Pata' in projeto_name or 'pata' in projeto_name:
            output_dir = './output/aula_05_da_a_pata'
        elif 'AULA 06' in projeto_name or 'Vem' in projeto_name or 'vem' in projeto_name:
            output_dir = './output/aula_06_vem'
        elif 'AULA 07' in projeto_name or 'Joga' in projeto_name or 'joga' in projeto_name:
            output_dir = './output/aula_07_joga'
        elif 'AULA 08' in projeto_name or 'Lugar' in projeto_name or 'lugar' in projeto_name:
            output_dir = './output/aula_08_lugar'
        elif 'AULA 09' in projeto_name or 'Nao' in projeto_name or 'não' in projeto_name.lower():
            output_dir = './output/aula_09_nao'
        elif 'AULA 10' in projeto_name or 'Livre' in projeto_name or 'livre' in projeto_name:
            output_dir = './output/aula_10_livre'

        # Verifica se já está processando
        with state_lock:
            if processing_state['active']:
                return jsonify({'error': 'Já existe um processamento em andamento'}), 409

        # Inicia processamento em thread separada
        processing_thread = threading.Thread(
            target=process_roteiro_async,
            args=(roteiro, output_dir)
        )
        processing_thread.daemon = True
        processing_thread.start()

        return jsonify({'message': 'Processamento iniciado', 'status': 'started'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna o status atual do processamento"""
    with state_lock:
        # Calcula tempo decorrido
        elapsed = 0
        if processing_state['start_time']:
            elapsed = time.time() - processing_state['start_time']
        
        return jsonify({
            'active': processing_state['active'],
            'current_scene': processing_state['current_scene'],
            'total_scenes': processing_state['total_scenes'],
            'logs': processing_state['logs'],
            'error': processing_state['error'],
            'waiting_browser_confirm': processing_state['waiting_browser_confirm'],
            'cancelled': processing_state['cancelled'],
            'elapsed_seconds': int(elapsed),
            'last_heartbeat': processing_state['last_heartbeat']
        })


@app.route('/api/browser-confirm', methods=['POST'])
def browser_confirm():
    """Confirma ou cancela após abrir o browser"""
    try:
        data = request.json
        confirmed = data.get('confirmed', False)
        print(f"\n*** BROWSER CONFIRM ENDPOINT CALLED! confirmed={confirmed} ***")
        print(f"*** _browser_confirm={_browser_confirm} ***")
        print(f"*** _current_generator={_current_generator} ***")
        
        if confirmed:
            add_log("✅ Usuário confirmou que browsers estão prontos", 'success')
            browser_confirm_event.set()
            _browser_confirm['confirmed'] = True
            if _current_generator:
                _current_generator._browser_confirmed = True
                print(f"*** Set _current_generator._browser_confirmed = True ***")
            with state_lock:
                processing_state['waiting_browser_confirm'] = False
            return jsonify({'message': 'Confirmado', 'status': 'confirmed'})
        else:
            add_log("❌ Usuário cancelou - browsers não estão prontos", 'error')
            with state_lock:
                processing_state['error'] = 'Processamento cancelado pelo usuário'
                processing_state['active'] = False
                processing_state['waiting_browser_confirm'] = False
                processing_state['cancelled'] = True
            browser_confirm_event.set()
            return jsonify({'message': 'Cancelado', 'status': 'cancelled'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/debug-state', methods=['GET'])
def debug_state():
    """Debug: mostra estado atual"""
    return jsonify({
        'browser_confirm': _browser_confirm,
        'current_generator': _current_generator is not None,
        'generator_confirmed': _current_generator._browser_confirmed if _current_generator else None,
        'waiting_browser': processing_state.get('waiting_browser_confirm', False),
        'active': processing_state['active']
    })


@app.route('/api/confirm-poll', methods=['GET'])
def confirm_poll():
    """Endpoint GET simples para confirmação - mais confiável que POST"""
    print("*** CONFIRM-POLL ENDPOINT CALLED ***")
    print(f"*** _browser_confirm={_browser_confirm} ***")
    _browser_confirm['confirmed'] = True
    browser_confirm_event.set()
    if _current_generator:
        _current_generator._browser_confirmed = True
        print(f"*** Set _current_generator._browser_confirmed = True via GET ***")
    with state_lock:
        processing_state['waiting_browser_confirm'] = False
    add_log("✅ Usuário confirmou que browsers estão prontos (via GET)", 'success')
    return jsonify({'status': 'confirmed'})


@app.route('/api/cancel', methods=['POST'])
def cancel_processing():
    """Cancela o processamento ativo"""
    try:
        with state_lock:
            if not processing_state['active']:
                return jsonify({'error': 'Nenhum processamento ativo'}), 400
            
            processing_state['cancelled'] = True
            processing_state['error'] = 'Cancelado pelo usuário'
            processing_state['waiting_browser_confirm'] = False
        
        # Libera a thread se estiver bloqueada no browser_confirm
        browser_confirm_event.set()
        
        add_log("⚠️ Cancelamento solicitado pelo usuário", 'warning')
        
        return jsonify({'message': 'Cancelamento solicitado', 'status': 'cancelling'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auto-confirm', methods=['POST'])
def auto_confirm():
    """Confirma browsers automaticamente (para automação)"""
    try:
        with state_lock:
            if not processing_state['waiting_browser_confirm']:
                return jsonify({'error': 'Não está aguardando confirmação'}), 400
        
        add_log("🤖 Confirmação automática de browsers", 'info')
        browser_confirm_event.set()
        
        with state_lock:
            processing_state['waiting_browser_confirm'] = False
        
        return jsonify({'message': 'Confirmado automaticamente', 'status': 'confirmed'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check para monitoramento"""
    with state_lock:
        return jsonify({
            'status': 'ok',
            'python': sys.version,
            'pid': os.getpid(),
            'active': processing_state['active'],
            'uptime': time.time() - processing_state.get('start_time', time.time()) if processing_state['start_time'] else 0
        })


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Retorna apenas os logs mais recentes"""
    since = request.args.get('since', 0, type=int)
    
    with state_lock:
        logs = processing_state['logs'][since:]
        return jsonify({
            'logs': logs,
            'total': len(processing_state['logs'])
        })


@app.route('/api/output', methods=['GET'])
def list_output():
    """Lista arquivos gerados no diretório de output"""
    try:
        output_dir = Path('./output')
        if not output_dir.exists():
            return jsonify({'files': [], 'directories': []})
        
        files = []
        directories = []
        
        for item in output_dir.rglob('*'):
            if item.is_file():
                files.append({
                    'path': str(item.relative_to(output_dir)),
                    'size': item.stat().st_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                })
            elif item.is_dir():
                directories.append(str(item.relative_to(output_dir)))
        
        return jsonify({
            'files': files,
            'directories': directories
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('SERVER_PORT', 5016))
    
    # Tenta liberar a porta se estiver ocupada por processo morto
    import socket
    def is_port_free(p):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex(('127.0.0.1', p))
            s.close()
            return result != 0
        except:
            return True
    
    if not is_port_free(port):
        print(f"⚠️ Porta {port} ocupada! Tentando porta {port + 1}...")
        port = port + 1
        # Verifica se a próxima também está livre
        while not is_port_free(port) and port < 5200:
            port += 1
        os.environ['SERVER_PORT'] = str(port)
        print(f"📡 Usando porta {port}")
    
    print("\n" + "="*60)
    print("🎬 VIDEO GENERATOR - Servidor Backend")
    print("="*60)
    print(f"\n📡 Servidor rodando em: http://localhost:{port}")
    print(f"🌐 Abra seu navegador e acesse: http://localhost:{port}")
    print("\n⚠️  Certifique-se de estar logado em:")
    print("   • ChatGPT (chat.openai.com)")
    print("   • Grok (x.ai/grok)")
    print("\n📋 Endpoints disponíveis:")
    print("   • GET  /api/status - Status do processamento")
    print("   • POST /api/process - Iniciar processamento")
    print("   • POST /api/cancel - Cancelar processamento")
    print("   • POST /api/auto-confirm - Confirmar browsers auto")
    print("   • GET  /api/health - Health check")
    print("   • GET  /api/output - Listar arquivos gerados")
    print("\n" + "="*60 + "\n")
    
    # Desabilita reloader para evitar cache de código antigo
    app.run(debug=False, port=port, threaded=True, use_reloader=False)
