"""
Video Generator - Automação de criação de vídeos a partir de roteiro JSON
Fluxo: JSON → DALL-E (imagem) → Grok Imagine (vídeo) → Extração de frames
"""

import json
import os
import time
import shutil
import glob
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional
import requests
from datetime import datetime

# Importações para automação do navegador
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import undetected_chromedriver as uc

# Importações para processamento de imagem/vídeo
from PIL import Image
import cv2


class VideoGenerator:
    """Classe principal para geração de vídeos a partir de roteiro"""
    
    def __init__(self, output_dir: str = "./output", wait_between_scenes: int = 180):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Diretórios organizados (em português)
        self.images_dir = self.output_dir / "imagens"
        self.videos_dir = self.output_dir / "videos"
        self.videos_hd_dir = self.output_dir / "videos_hd"
        self.frames_dir = self.output_dir / "frames"
        
        for dir_path in [self.images_dir, self.videos_dir, self.videos_hd_dir, self.frames_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        self.driver = None
        self.last_frame = None
        
        # Contador de cenas processadas (para reiniciar navegador periodicamente)
        self.scenes_processed = 0
        self.restart_interval = 5  # Reinicia navegador a cada 5 cenas
        
        # Handles das abas (para gerenciar ChatGPT e Grok)
        self.chatgpt_tab = None
        self.grok_tab = None
        
        # Para sincronização com a interface web
        self.browser_confirm_event = None  # Será setado pelo server.py
        self.waiting_callback = None  # Callback para notificar estado de espera
        
        # CONFIGURAÇÃO DE RATE LIMITING
        # Ajuste este valor conforme necessário:
        # 60 = 1 minuto (rápido, pode bater limite)
        # 180 = 3 minutos (recomendado, seguro 24/7)
        # 300 = 5 minutos (muito conservador)
        self.wait_between_scenes = wait_between_scenes
        print(f"⏱️  Configurado para aguardar {self.wait_between_scenes // 60} minutos entre cenas")
    
    def set_waiting_callback(self, callback):
        """Define callback para notificar quando está aguardando confirmação"""
        self.waiting_callback = callback
    
    def switch_to_chatgpt(self):
        """Troca para a aba do ChatGPT"""
        if self.chatgpt_tab and self.driver:
            self.driver.switch_to.window(self.chatgpt_tab)
            time.sleep(1)
    
    def switch_to_grok(self):
        """Troca para a aba do Grok"""
        if self.grok_tab and self.driver:
            self.driver.switch_to.window(self.grok_tab)
            time.sleep(1)
    
    def restart_browser(self):
        """Reinicia o navegador preservando a sessão (login)"""
        print(f"\n🔄 REINICIANDO NAVEGADOR (preservando sessão)")
        print("   Isso ajuda a evitar crashes e problemas de memória...")
        
        automation_profile = getattr(self, '_automation_profile', 
            os.path.join(tempfile.gettempdir(), f"chrome_automation_{os.getpid()}"))
        
        try:
            # Fecha o navegador atual
            if self.driver:
                self.driver.quit()
        except:
            pass
        
        time.sleep(3)
        
        # Reconfigura o Chrome com o mesmo perfil (mantém login)
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={automation_profile}")
        options.add_argument("--profile-directory=Default")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--mute-audio')
        
        # Configurações para downloads
        prefs = {
            "download.default_directory": str(self.videos_dir.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = uc.Chrome(options=options, version_main=148)
            print("   ✓ Navegador reiniciado com sucesso!")
            
            # Reabre ChatGPT e Grok
            print("   📂 Reabrindo ChatGPT...")
            self.driver.get("https://chat.openai.com")
            self.chatgpt_tab = self.driver.current_window_handle
            time.sleep(3)
            
            print("   📂 Reabrindo Grok...")
            self.driver.execute_script("window.open('https://grok.com/imagine', '_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.grok_tab = self.driver.current_window_handle
            time.sleep(5)
            
            print("   ✓ Abas reconfiguradas!\n")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro ao reiniciar navegador: {e}")
            return False
        
    def setup_browser(self):
        """Configura o navegador Chrome para automação (anti-detecção)"""
        
        # Usa perfil temporário único para evitar conflito com Chrome aberto
        automation_profile = os.path.join(tempfile.gettempdir(), f"chrome_automation_{os.getpid()}")
        os.makedirs(automation_profile, exist_ok=True)
        self._automation_profile = automation_profile
        
        # Configurações do undetected_chromedriver (bypass Cloudflare)
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={automation_profile}")
        options.add_argument("--profile-directory=Default")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-extensions')
        options.add_argument('--mute-audio')
        
        # Para downloads automáticos
        prefs = {
            "download.default_directory": str(self.videos_dir.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        options.add_experimental_option("prefs", prefs)
        
        try:
            self.driver = uc.Chrome(options=options, version_main=148)
            # Timeouts para evitar travamentos
            self.driver.set_page_load_timeout(60)
            self.driver.set_script_timeout(30)
            print("✓ Navegador configurado (anti-detecção ativa, timeouts configurados)")
            print("ℹ️  Este é um Chrome separado - você pode usar seu Chrome normal normalmente!")
        except Exception as e:
            print(f"\n❌ ERRO ao abrir Chrome: {e}")
            print("\n🔧 SOLUÇÕES:")
            print("   1. Feche TODOS os Chromes abertos")
            print("   2. Aguarde 5 segundos")
            print("   3. Tente novamente")
            print("\n   Ou no PowerShell execute:")
            print("   taskkill /F /IM chrome.exe")
            print()
            raise Exception("Não foi possível abrir o Chrome. Feche todas as instâncias e tente novamente.")
        
        # PAUSA PARA LOGIN MANUAL
        print("\n" + "="*60)
        print("⚠️  CONFIGURAÇÃO INICIAL")
        print("="*60)
        
        # NOVA ABORDAGEM: começa com about:blank, DEPOIS navega para cada site
        # Isso evita o erro "target window already closed"
        
        print("\n🔗 Abrindo ChatGPT...")
        self.chatgpt_tab = self.driver.current_window_handle
        try:
            self.driver.get("https://chat.openai.com")
            print("   ✓ ChatGPT carregado")
        except Exception as e:
            print(f"   ⚠️ Chat carregou: {str(e)[:60]}")
        
        print("\n🔗 Abrindo Grok...")
        try:
            # Selenium 4: cria nova aba sem usar window.open()
            self.driver.switch_to.new_window('tab')
            self.grok_tab = self.driver.current_window_handle
            self.driver.get("https://grok.com/imagine")
            print("   ✓ Grok carregado")
        except Exception as e:
            print(f"   ⚠️ Método 1 falhou: {e}")
            try:
                # Fallback: window.open
                self.driver.switch_to.window(self.chatgpt_tab)
                self.driver.execute_script("window.open('about:blank');")
                handles = self.driver.window_handles
                self.grok_tab = [h for h in handles if h != self.chatgpt_tab][0]
                self.driver.switch_to.window(self.grok_tab)
                self.driver.get("https://grok.com/imagine")
                print("   ✓ Grok carregado (fallback)")
            except Exception as e2:
                print(f"   ❌ Não abriu Grok: {e2}")
                self.grok_tab = None
        
        # Volta para aba do ChatGPT (com fallback se fechou)
        try:
            self.driver.switch_to.window(self.chatgpt_tab)
        except:
            print("   ⚠️ Aba do ChatGPT foi fechada, recriando...")
            self.driver.get("https://chat.openai.com")
            self.chatgpt_tab = self.driver.current_window_handle
        
        print("\n📋 INSTRUÇÕES:")
        print("   1. Faça LOGIN no ChatGPT (se necessário)")
        print("   2. Feche quaisquer popups/tours")
        print("   3. Certifique-se que vê o campo de texto")
        print("   4. Teste gerando uma imagem manualmente:")
        print("      Digite: 'Generate an image: a cat'")
        print("   5. Se funcionou, volte aqui!")
        print("   6. Troque para aba do Grok e faça LOGIN")
        print("   7. Volte para a aba do ChatGPT")
        print("\n✅ Aguardando confirmação na INTERFACE WEB...")
        print("   (Clique no botão 'Sim, estão prontos' na interface)\n")
        
        # Anuncia para a interface que está aguardando confirmação
        if self.waiting_callback:
            self.waiting_callback(True)
        
        # Aguarda confirmação da interface via POLLING (mais confiável que Event)
        print("⏳ Aguardando confirmação na interface...")
        print(f"   _browser_confirm_flag presente: {hasattr(self, '_browser_confirm_flag')}")
        if hasattr(self, '_browser_confirm_flag'):
            print(f"   _browser_confirm_flag valor: {self._browser_confirm_flag}")
        self._browser_confirmed = False
        wait_start = time.time()
        timeout = 300  # 5 minutos
        while not self._browser_confirmed:
            elapsed = time.time() - wait_start
            if elapsed > timeout:
                print("⚠️ TIMEOUT: Confirmação não recebida em 5 minutos!")
                print("   Continuando processamento mesmo assim...")
                break
            if int(elapsed) % 10 == 0 and int(elapsed) > 0:
                print(f"   ⏳ Aguardando... {int(elapsed)}s/{timeout}s")
                if hasattr(self, '_browser_confirm_flag'):
                    print(f"      flag valor: {self._browser_confirm_flag}")
            time.sleep(0.5)  # Poll a cada 500ms
            
            # Verifica flag compartilhada do server.py
            if hasattr(self, '_browser_confirm_flag') and self._browser_confirm_flag.get('confirmed', False):
                print("   ✓ Flag compartilhada detectada!")
                self._browser_confirmed = True
                break
            
            # Tambem verifica o evento antigo como fallback
            if self.browser_confirm_event and self.browser_confirm_event.is_set():
                print("   ✓ Evento detectado via is_set()!")
                self._browser_confirmed = True
                break
        
        print(f"✅ POLLING ENCERRADO: _browser_confirmed={self._browser_confirmed}")
        
        # Notifica que não está mais aguardando
        if self.waiting_callback:
            self.waiting_callback(False)
        
        print("\n✅ Confirmação recebida! Continuando processamento!")
        print("="*60 + "\n")
        
        print("[SETUP] setup_browser() FINALIZADO - retornando para process_roteiro_async")
        
    def load_roteiro(self, json_path: str) -> Dict:
        """Carrega e valida o arquivo roteiro.json"""
        print(f"\n📖 Carregando roteiro: {json_path}")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                roteiro = json.load(f)
            
            # Validação da estrutura
            if 'cenas' not in roteiro:
                raise ValueError("JSON inválido: campo 'cenas' não encontrado")
            
            for i, cena in enumerate(roteiro['cenas']):
                required_fields = ['dalle_prompt', 'grok_movement']
                missing = [f for f in required_fields if f not in cena]
                if missing:
                    raise ValueError(f"Cena {i+1} inválida: faltam campos {missing}")
                # Campo opcional com default
                if 'use_previous_frame' not in cena:
                    cena['use_previous_frame'] = False
            
            print(f"✓ Roteiro validado: {len(roteiro['cenas'])} cenas")
            return roteiro
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao ler JSON: {e}")
        except FileNotFoundError:
            raise ValueError(f"Arquivo não encontrado: {json_path}")
    
    def generate_image_dalle(self, prompt: str, scene_num: int) -> str:
        """Gera imagem usando DALL-E via ChatGPT"""
        import sys
        def dbg(msg):
            ts = time.strftime('%H:%M:%S')
            line = f"[DALLE {ts}] {msg}"
            print(line, flush=True)
            sys.stdout.flush()
        
        dbg(f"INICIO generate_image_dalle cena {scene_num}")
        dbg(f"Prompt: {prompt[:100]}...")
        
        try:
            dbg(f"chatgpt_tab={self.chatgpt_tab is not None}, grok_tab={self.grok_tab is not None}, driver={self.driver is not None}")
            
            # Verifica se o driver ainda está vivo
            try:
                title = self.driver.title
                dbg(f"Driver vivo, titulo: {title}")
            except Exception as e:
                dbg(f"ERRO: Driver morto! {e}")
                raise
            
            # **SEMPRE** troca para aba do ChatGPT primeiro!
            dbg("Trocando para aba do ChatGPT...")
            self.switch_to_chatgpt()
            dbg("Aba ChatGPT ativa")
            
            # OTIMIZAÇÃO: Cena 1 já está no ChatGPT (setup_browser), não precisa navegar
            # Cenas 2+: navega para nova URL (força reload fresco)
            if scene_num == 1:
                dbg("Cena 1: usando página atual do ChatGPT (sem navegação)")
                time.sleep(2)
            else:
                dbg(f"Abrindo nova conversa no ChatGPT (cena {scene_num})...")
                try:
                    self.driver.get("https://chat.openai.com")
                    dbg("Navegação OK")
                except Exception as nav_e:
                    dbg(f"Navegação com aviso: {nav_e}")
                time.sleep(2)
            
            dbg("Tirando screenshot de debug...")
            debug_start = self.output_dir / f"debug_inicio_cena_{scene_num}.png"
            self.driver.save_screenshot(str(debug_start))
            dbg(f"Screenshot salvo: {debug_start}")
            
            # Fecha possíveis popups ou modais
            try:
                # Tenta fechar modal de boas-vindas, tour, etc
                close_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Close'], button.close, button[data-testid='close-button']")
                for btn in close_buttons:
                    try:
                        btn.click()
                        time.sleep(0.5)
                    except:
                        pass
            except:
                pass
            
            # Aguarda um pouco mais
            time.sleep(2)
            
            # SCREENSHOT DEPOIS DE FECHAR POPUPS
            debug_after_close = self.output_dir / f"debug_depois_popup_cena_{scene_num}.png"
            self.driver.save_screenshot(str(debug_after_close))
            print(f"📸 Screenshot após fechar popups: {debug_after_close}")
            
            # Localiza campo de input - tenta vários métodos
            wait = WebDriverWait(self.driver, 30)
            input_box = None
            
            print("🔍 Procurando campo de texto...")
            
            # Método 0: Procura o input "Pergunte alguma coisa" (novo ChatGPT)
            try:
                print("   Tentando método 0: Procurando 'Pergunte alguma coisa'...")
                input_box = self.driver.execute_script("""
                    // Procura por elemento com placeholder "Pergunte alguma coisa"
                    const elements = document.querySelectorAll('div[contenteditable="true"], textarea, [role="textbox"]');
                    for (let el of elements) {
                        const rect = el.getBoundingClientRect();
                        // Campo de input fica na parte central inferior
                        if (rect.width > 200 && rect.height > 20 && rect.top > 400) {
                            return el;
                        }
                    }
                    
                    // Fallback: procura por div com placeholder
                    const allDivs = document.querySelectorAll('div');
                    for (let div of allDivs) {
                        if (div.getAttribute('data-placeholder') || 
                            div.getAttribute('placeholder') ||
                            div.textContent.includes('Pergunte alguma coisa')) {
                            return div;
                        }
                    }
                    return null;
                """)
                if input_box:
                    print("   ✓ Encontrado via JS (Pergunte alguma coisa)!")
            except Exception as e:
                print(f"   ✗ Método 0 falhou: {str(e)[:100]}")
            
            # Método 1: Procura por contenteditable
            if not input_box:
                try:
                    print("   Tentando método 1: div[contenteditable='true']")
                    input_box = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true']"))
                    )
                    print("   ✓ Encontrado com contenteditable!")
                except Exception as e:
                    print(f"   ✗ Contenteditable falhou: {str(e)[:100]}")
            
            # Método 2: Procura por textarea (interface antiga)
            if not input_box:
                try:
                    print("   Tentando método 2: textarea")
                    textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
                    for textarea in textareas:
                        if textarea.is_displayed():
                            input_box = textarea
                            print("   ✓ Encontrado textarea!")
                            break
                except Exception as e:
                    print(f"   ✗ Método 2 falhou: {str(e)[:100]}")
            
            # Método 3: Procura por role="textbox"
            if not input_box:
                try:
                    print("   Tentando método 3: [role='textbox']")
                    input_box = self.driver.find_element(By.CSS_SELECTOR, "[role='textbox']")
                    print("   ✓ Encontrado via role='textbox'!")
                except Exception as e:
                    print(f"   ✗ Método 3 falhou: {str(e)[:100]}")
            
            # Método 4: Clica na área do placeholder diretamente
            if not input_box:
                try:
                    print("   Tentando método 4: Clicando na área do placeholder...")
                    clicked = self.driver.execute_script("""
                        // Procura elemento que contém o texto do placeholder
                        const walker = document.createTreeWalker(
                            document.body,
                            NodeFilter.SHOW_TEXT,
                            null,
                            false
                        );
                        
                        while (walker.nextNode()) {
                            const node = walker.currentNode;
                            if (node.textContent.includes('Pergunte alguma coisa') || 
                                node.textContent.includes('Ask anything')) {
                                // Clica no elemento pai
                                let parent = node.parentElement;
                                for (let i = 0; i < 5; i++) {
                                    if (parent && parent.getAttribute('contenteditable')) {
                                        return parent;
                                    }
                                    parent = parent?.parentElement;
                                }
                                // Se não encontrou contenteditable, retorna o elemento do texto
                                return node.parentElement;
                            }
                        }
                        return null;
                    """)
                    if clicked:
                        input_box = clicked
                        print("   ✓ Encontrado via placeholder text!")
                except Exception as e:
                    print(f"   ✗ Método 4 falhou: {str(e)[:100]}")
            
            if not input_box:
                # SCREENSHOT FINAL DO ERRO
                debug_error = self.output_dir / f"debug_erro_campo_cena_{scene_num}.png"
                self.driver.save_screenshot(str(debug_error))
                print(f"📸 Screenshot do erro: {debug_error}")
                print("\n⚠️  ENVIE ESTES 3 SCREENSHOTS:")
                print(f"   1. {debug_start}")
                print(f"   2. {debug_after_close}")
                print(f"   3. {debug_error}")
                raise Exception("Campo de texto não encontrado no ChatGPT")
            
            # Continua o processamento...
            print("✓ Campo de texto encontrado! Continuando...")
            
            # ATIVA O CAMPO - Múltiplas tentativas
            print("🖱️ Ativando campo de texto...")
            
            # Tentativa 1: Clique direto
            try:
                input_box.click()
                print("   ✓ Clique direto funcionou")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ✗ Clique direto falhou: {str(e)[:50]}")
            
            # Tentativa 2: JavaScript click
            try:
                self.driver.execute_script("arguments[0].click();", input_box)
                print("   ✓ JavaScript click funcionou")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ✗ JavaScript click falhou: {str(e)[:50]}")
            
            # Tentativa 3: Scroll + focus
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_box)
                time.sleep(0.3)
                self.driver.execute_script("arguments[0].focus();", input_box)
                print("   ✓ Scroll + focus funcionou")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ✗ Scroll + focus falhou: {str(e)[:50]}")
            
            # Tentativa 4: Clique nas coordenadas
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                actions = ActionChains(self.driver)
                actions.move_to_element(input_box).click().perform()
                print("   ✓ ActionChains click funcionou")
                time.sleep(0.5)
            except Exception as e:
                print(f"   ✗ ActionChains click falhou: {str(e)[:50]}")
            
            # Screenshot após ativar
            debug_activated = self.output_dir / f"debug_campo_ativado_cena_{scene_num}.png"
            self.driver.save_screenshot(str(debug_activated))
            print(f"📸 Screenshot após ativar campo: {debug_activated}")
            
            # Limpa campo e digita o prompt
            dalle_command = f"Generate an image: {prompt}"
            print(f"⌨️ Digitando comando...")
            
            # Primeiro, foca no campo
            try:
                self.driver.execute_script("arguments[0].focus();", input_box)
                time.sleep(0.5)
            except:
                pass
            
            # Tenta limpar o campo
            try:
                # Para contenteditable, seleciona tudo e deleta
                self.driver.execute_script("""
                    const el = arguments[0];
                    el.focus();
                    el.textContent = '';
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                """, input_box)
                time.sleep(0.3)
            except:
                try:
                    input_box.clear()
                except:
                    pass
            
            # Método 1: send_keys (funciona para textarea e alguns contenteditable)
            typed = False
            try:
                input_box.send_keys(dalle_command)
                typed = True
                print("   ✓ Texto digitado via send_keys!")
                time.sleep(1)
            except Exception as e:
                print(f"   ✗ send_keys falhou: {str(e)[:50]}")
            
            # Método 2: JavaScript para contenteditable (se send_keys falhou)
            if not typed:
                try:
                    self.driver.execute_script("""
                        const el = arguments[0];
                        const text = arguments[1];
                        el.focus();
                        el.textContent = text;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    """, input_box, dalle_command)
                    typed = True
                    print("   ✓ Texto inserido via JS (contenteditable)!")
                    time.sleep(1)
                except Exception as e2:
                    print(f"   ✗ JS contenteditable falhou: {str(e2)[:50]}")
            
            # Método 3: Simula digitação caractere por caractere (último recurso)
            if not typed:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.click(input_box)
                    actions.send_keys(dalle_command)
                    actions.perform()
                    typed = True
                    print("   ✓ Texto digitado via ActionChains!")
                    time.sleep(1)
                except Exception as e3:
                    print(f"   ✗ ActionChains falhou: {str(e3)[:50]}")
            
            if not typed:
                raise Exception("Não foi possível digitar o prompt")
            
            # Screenshot após digitar
            debug_typed = self.output_dir / f"debug_depois_digitar_cena_{scene_num}.png"
            self.driver.save_screenshot(str(debug_typed))
            print(f"📸 Screenshot após digitar: {debug_typed}")
            
            time.sleep(1)
            
            # Clica em enviar - tenta vários métodos
            send_clicked = False
            
            print("🔍 Procurando botão de enviar...")
            
            # Método 1: data-testid
            try:
                send_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='send-button']")
                if send_button.is_displayed():
                    self.driver.execute_script("arguments[0].click();", send_button)
                    send_clicked = True
                    print("✓ Enviado com método 1!")
            except:
                pass
            
            # Método 2: aria-label
            if not send_clicked:
                try:
                    send_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label*='Send']")
                    self.driver.execute_script("arguments[0].click();", send_button)
                    send_clicked = True
                    print("✓ Enviado com método 2!")
                except:
                    pass
            
            # Método 3: Enter
            if not send_clicked:
                from selenium.webdriver.common.keys import Keys
                input_box.send_keys(Keys.RETURN)
                send_clicked = True
                print("✓ Enviado com Enter!")
            
            if not send_clicked:
                raise Exception("Não foi possível enviar o prompt")
            
            # Aguarda geração da imagem (DALL-E é lento)
            print("⏳ Aguardando DALL-E gerar imagem (pode levar 30-60 segundos)...")
            time.sleep(10)  # Espera inicial
            
            # SCROLL até o FINAL da página para ver a imagem mais recente
            try:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            except:
                pass
            
            # Aguarda até encontrar imagem (até 2 minutos)
            max_attempts = 24  # 24 x 5s = 2 minutos
            for attempt in range(max_attempts):
                print(f"   Tentativa {attempt + 1}/{max_attempts}...")
                
                # Busca todos os elementos de imagem
                images = self.driver.find_elements(By.TAG_NAME, "img")
                
                # IMPORTANTE: Pega apenas imagens VISÍVEIS (Y > 0) e com maior Y
                dalle_images = []
                
                for img in images:
                    src = img.get_attribute("src")
                    if not src:
                        continue
                    
                    # Verifica se é imagem do DALL-E (vários padrões possíveis)
                    dalle_patterns = [
                        "oaidalleapiprodscus",
                        "dalle",
                        "openai",
                        "blob:",
                        "data:image"
                    ]
                    
                    is_dalle = any(pattern in src.lower() for pattern in dalle_patterns)
                    
                    # Verifica tamanho (imagens DALL-E são grandes)
                    try:
                        size = img.size
                        if size['width'] >= 256 and size['height'] >= 256:
                            is_dalle = True
                    except:
                        pass
                    
                    if is_dalle and len(src) > 50:  # URL válida
                        try:
                            location = img.location
                            y_pos = location.get('y', 0)
                            
                            # IMPORTANTE: Só aceita imagens VISÍVEIS (Y > 0)
                            # Imagens com Y negativo estão scrolladas para fora (antigas!)
                            if y_pos > 0:
                                dalle_images.append((img, src, y_pos))
                        except:
                            pass
                
                # Pega a imagem com MAIOR Y POSITIVO (mais recente = mais embaixo)
                if dalle_images:
                    # Ordena por posição Y (maior = mais recente)
                    dalle_images.sort(key=lambda x: x[2], reverse=True)
                    img, src, y_pos = dalle_images[0]  # Primeira = maior Y!
                    
                    print(f"✓ Imagem encontrada! URL: {src[:80]}...")
                    if len(dalle_images) > 1:
                        print(f"   ℹ️  {len(dalle_images)} imagens VISÍVEIS na página, usando a MAIS RECENTE (Y={y_pos}px)")
                    
                    # AGUARDA A IMAGEM CARREGAR COMPLETAMENTE
                    print("   ⏳ Aguardando imagem DALL-E carregar completamente...")
                    print("   (DALL-E pode levar até 2 minutos para renderizar)")
                    
                    # Verifica se a imagem está carregada via JavaScript
                    max_wait = 30  # 30 segundos
                    loaded = False
                    
                    for wait_time in range(max_wait):
                        try:
                            # Verifica se a imagem foi carregada completamente
                            is_loaded = self.driver.execute_script("""
                                var img = arguments[0];
                                return img.complete && img.naturalHeight !== 0;
                            """, img)
                            
                            if is_loaded:
                                # Verifica também se o tamanho é adequado (não é placeholder)
                                size = img.size
                                if size['width'] >= 512 and size['height'] >= 512:
                                    loaded = True
                                    print(f"   ✓ Imagem carregada após {wait_time} segundos ({size['width']}x{size['height']})")
                                    break
                            
                            # Mostra progresso a cada 10 segundos
                            if wait_time % 10 == 0 and wait_time > 0:
                                print(f"   ⏱️  Aguardando... {wait_time}s decorridos")
                            
                            time.sleep(1)
                        except:
                            time.sleep(1)
                    
                    if not loaded:
                        print(f"   ⚠️ Timeout após {max_wait}s, tentando capturar mesmo assim...")
                    
                    # Aguarda mais 3 segundos de segurança para renderização final
                    print("   ⏳ Aguardando renderização final...")
                    time.sleep(3)
                    
                    # Download da imagem
                    image_path = self.images_dir / f"scene_{scene_num:03d}.png"
                    
                    try:
                        # Passa o elemento img ao invés da URL
                        self._download_image(img, image_path)
                        
                        # Validação
                        if self._validate_image(image_path):
                            print(f"✓ Imagem salva: {image_path}")
                            return str(image_path)
                    except Exception as download_error:
                        print(f"⚠️ Erro ao baixar: {download_error}")
                        print(f"   🔄 Re-buscando imagem mais recente...")
                        # NÃO faz continue! Deixa aguardar 5s e tentar de novo
                        # para RE-BUSCAR a imagem com maior Y
                
                # Se não encontrou ainda, aguarda mais
                time.sleep(5)
            
            # Se chegou aqui, não encontrou
            print("\n⚠️ Não foi possível encontrar a imagem gerada.")
            print("⚠️ Possíveis causas:")
            print("   1. ChatGPT não está logado")
            print("   2. DALL-E ainda está processando (tente aumentar o tempo)")
            print("   3. Limite de geração atingido")
            print("\n🔍 Salvando screenshot para debug...")
            debug_path = self.output_dir / f"debug_scene_{scene_num}.png"
            self.driver.save_screenshot(str(debug_path))
            print(f"   Screenshot salvo em: {debug_path}")
            
            raise Exception("Imagem não encontrada na resposta do ChatGPT - verifique o screenshot de debug")
            
        except Exception as e:
            print(f"✗ Erro ao gerar imagem: {e}")
            # Salva screenshot do erro
            try:
                error_path = self.output_dir / f"error_scene_{scene_num}.png"
                self.driver.save_screenshot(str(error_path))
                print(f"   Screenshot do erro salvo em: {error_path}")
            except:
                pass
            raise
    
    def _download_image(self, img_element, save_path: Path):
        """Baixa imagem em ALTA QUALIDADE usando URL original"""
        try:
            print(f"   Tentando baixar imagem em ALTA QUALIDADE...")
            
            # Método 1: Baixar via URL original (melhor qualidade)
            try:
                src = img_element.get_attribute("src")
                
                if src and len(src) > 50:
                    # Pega cookies do selenium para autenticação
                    selenium_cookies = self.driver.get_cookies()
                    cookies_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
                    
                    # Headers necessários
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Referer': 'https://chat.openai.com/',
                    }
                    
                    # Tenta baixar com cookies e headers
                    response = requests.get(src, cookies=cookies_dict, headers=headers, stream=True, timeout=30)
                    
                    if response.status_code == 200:
                        with open(save_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        print(f"   ✓ Imagem baixada em ALTA QUALIDADE via URL")
                        return
                    else:
                        print(f"   ✗ Download via URL retornou: {response.status_code}")
                
            except Exception as e:
                print(f"   ✗ Download via URL falhou: {str(e)[:50]}")
            
            # Método 2: Screenshot do elemento (fallback - qualidade menor)
            try:
                # Scroll até a imagem
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img_element)
                time.sleep(0.5)
                
                # Pega a screenshot da imagem
                img_element.screenshot(str(save_path))
                print(f"   ⚠️ Imagem capturada via screenshot (qualidade reduzida)")
                return
            except Exception as e:
                print(f"   ✗ Screenshot direto falhou: {str(e)[:50]}")
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img_element)
                time.sleep(0.5)
                
                # Pega a screenshot da imagem
                img_element.screenshot(str(save_path))
                print(f"   ✓ Imagem capturada via screenshot")
                return
            except Exception as e:
                print(f"   ✗ Screenshot direto falhou: {str(e)[:50]}")
            
            # Método 2: Clicar direito e salvar (mais complexo, requer configuração de download)
            try:
                from selenium.webdriver.common.action_chains import ActionChains
                from selenium.webdriver.common.keys import Keys
                
                # Clica direito na imagem
                actions = ActionChains(self.driver)
                actions.context_click(img_element).perform()
                time.sleep(1)
                
                # Tenta "Salvar imagem como..." (pode variar por idioma)
                # V = Save image as (inglês), S = Salvar imagem (português)
                actions.send_keys('v').perform()
                time.sleep(1)
                
                # Digite o caminho e salve
                actions.send_keys(str(save_path.absolute())).perform()
                time.sleep(0.5)
                actions.send_keys(Keys.RETURN).perform()
                
                print(f"   ✓ Imagem salva via menu de contexto")
                return
            except Exception as e:
                print(f"   ✗ Menu de contexto falhou: {str(e)[:50]}")
            
            # Método 3: Fallback para requests com cookies do selenium
            try:
                src = img_element.get_attribute("src")
                
                # Pega cookies do selenium
                selenium_cookies = self.driver.get_cookies()
                cookies_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
                
                # Tenta baixar com os cookies
                response = requests.get(src, cookies=cookies_dict, stream=True)
                response.raise_for_status()
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"   ✓ Imagem baixada com cookies")
                return
            except Exception as e:
                print(f"   ✗ Download com cookies falhou: {str(e)[:50]}")
                raise Exception("Todos os métodos de download falharam")
                
        except Exception as e:
            print(f"   ✗ Erro ao baixar imagem: {e}")
            raise
    
    def _validate_image(self, image_path: Path) -> bool:
        """Valida se a imagem foi baixada corretamente"""
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # Validações básicas
            if width < 100 or height < 100:
                print("✗ Imagem muito pequena")
                return False
            
            # Verifica se não está corrompida
            img.verify()
            
            print(f"✓ Imagem validada: {width}x{height}px")
            return True
            
        except Exception as e:
            print(f"✗ Validação falhou: {e}")
            return False
    
    def generate_video_grok(self, image_path: str, movement_prompt: str, scene_num: int) -> str:
        """Gera vídeo usando Grok Imagine - Fluxo: + → Upload → Video → 10s → Prompt → Send"""
        print(f"\n🎬 Gerando vídeo para cena {scene_num}...")
        print(f"Movimento: {movement_prompt[:100]}...")
        
        # Verifica se precisa reiniciar navegador (a cada X cenas)
        if self.scenes_processed > 0 and self.scenes_processed % self.restart_interval == 0:
            if not self.restart_browser():
                print("   ⚠️ Falha ao reiniciar, tentando setup_browser()...")
                self.setup_browser()
        
        try:
            # Troca para aba do Grok
            print("🔄 Trocando para aba do Grok...")
            self.switch_to_grok()
            
            # SEMPRE navega para Grok Imagine fresco (garante tela limpa)
            print("🌐 Navegando para Grok Imagine...")
            self.driver.get("https://grok.com/imagine")
            time.sleep(8)
            
            print(f"📍 URL: {self.driver.current_url}")
            
            # Screenshot inicial
            debug_inicial = self.output_dir / f"debug_grok_inicial_{scene_num}.png"
            self.driver.save_screenshot(str(debug_inicial))
            print(f"📸 Screenshot inicial: {debug_inicial}")
            
            # ============================================
            # ETAPA 1: CLICAR NO "+" E FAZER UPLOAD
            # ============================================
            print("\n📤 ETAPA 1: Clicando no '+' e fazendo upload...")
            print(f"   Arquivo: {image_path}")
            
            time.sleep(3)
            
            # Clica no botão "+" (canto inferior esquerdo do input)
            plus_clicked = False
            try:
                # Método 1: Procura botão com "+" por JS
                plus_clicked = self.driver.execute_script("""
                    // Procura botão com "+" no aria-label ou texto
                    const buttons = document.querySelectorAll('button');
                    for (let btn of buttons) {
                        const rect = btn.getBoundingClientRect();
                        // Botão "+" fica na parte inferior (y > 900) e à esquerda do input
                        if (rect.top > 900 && rect.left > 100 && rect.left < 400) {
                            const text = btn.textContent.trim();
                            const ariaLabel = btn.getAttribute('aria-label') || '';
                            // Verifica se é o botão "+" ou "Adicionar"
                            if (text === '+' || text === '+' || ariaLabel.includes('upload') || 
                                ariaLabel.includes('adicionar') || ariaLabel.includes('attach') ||
                                btn.querySelector('svg')) {
                                btn.click();
                                return true;
                            }
                        }
                    }
                    
                    // Fallback: procura por input[type='file'] que pode estar associado ao "+"
                    const fileInputs = document.querySelectorAll('input[type="file"]');
                    if (fileInputs.length > 0) {
                        return 'has_file_input';
                    }
                    return false;
                """)
                
                if plus_clicked == 'has_file_input':
                    print("   ℹ️  Botão '+' não encontrado, mas input[type='file'] existe")
                    plus_clicked = False
                elif plus_clicked:
                    print("   ✅ Botão '+' clicado via JS!")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"   ⚠️ JS falhou: {str(e)[:50]}")
            
            # Método 2: Selenium - procura botão "+" 
            if not plus_clicked:
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in buttons:
                        if btn.is_displayed():
                            location = btn.location
                            size = btn.size
                            text = btn.text.strip()
                            aria_label = btn.get_attribute('aria-label') or ''
                            
                            # Verifica se é o botão "+" (parte inferior, à esquerda)
                            if location['y'] > 900 and 100 < location['x'] < 400:
                                if text in ['+', '+'] or 'upload' in aria_label.lower() or 'attach' in aria_label.lower():
                                    try:
                                        btn.click()
                                        plus_clicked = True
                                        print(f"   ✅ Botão '+' clicado via Selenium! (X={location['x']}, Y={location['y']})")
                                        time.sleep(2)
                                        break
                                    except:
                                        continue
                except Exception as e:
                    print(f"   ⚠️ Selenium falhou: {str(e)[:50]}")
            
            # Fallback: tenta encontrar input[type='file'] diretamente
            if not plus_clicked:
                print("   Buscando input[type='file'] diretamente...")
            
            # Faz upload via input[type='file']
            print("   Fazendo upload da imagem...")
            file_uploaded = False
            
            for attempt in range(5):
                file_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='file']")
                
                if file_inputs:
                    for file_input in file_inputs:
                        try:
                            file_input.send_keys(str(Path(image_path).absolute()))
                            file_uploaded = True
                            print(f"   ✅ Imagem enviada! (tentativa {attempt + 1})")
                            time.sleep(8)  # Aguarda upload e processamento
                            break
                        except:
                            continue
                    if file_uploaded:
                        break
                
                if not file_uploaded and attempt < 4:
                    print(f"   ⚠️ Input não encontrado, tentativa {attempt + 1}/5...")
                    time.sleep(2)
                    # Tenta clicar no "+" novamente
                    try:
                        self.driver.execute_script("""
                            const btns = document.querySelectorAll('button');
                            for (let b of btns) {
                                if (b.textContent.includes('+') || b.getAttribute('aria-label')?.includes('upload')) {
                                    b.click();
                                    break;
                                }
                            }
                        """)
                        time.sleep(1)
                    except:
                        pass
            
            if not file_uploaded:
                debug_erro = self.output_dir / f"debug_grok_upload_failed_{scene_num}.png"
                self.driver.save_screenshot(str(debug_erro))
                print(f"   📸 Screenshot: {debug_erro}")
                raise Exception("Não foi possível fazer upload da imagem")
            
            # Screenshot após upload
            debug_apos_upload = self.output_dir / f"debug_grok_apos_upload_{scene_num}.png"
            self.driver.save_screenshot(str(debug_apos_upload))
            print(f"📸 Screenshot após upload: {debug_apos_upload}")
            
            # ============================================
            # ETAPA 2: SELECIONAR MODO "VIDEO"
            # ============================================
            print("\n🎬 ETAPA 2: Selecionando modo 'Video'...")
            time.sleep(2)
            
            video_mode_clicked = False
            
            # Método 1: Clica no texto "Video" na barra inferior
            try:
                video_mode_clicked = self.driver.execute_script("""
                    // Procura por elemento com texto "Video" ou "Vídeo"
                    const elements = document.querySelectorAll('button, div, span, a, label');
                    for (let el of elements) {
                        const text = el.textContent.trim().toLowerCase();
                        if (text === 'video' || text === 'vídeo') {
                            el.click();
                            return true;
                        }
                    }
                    return false;
                """)
                if video_mode_clicked:
                    print("   ✅ Modo 'Video' selecionado via JS!")
                    time.sleep(2)
            except:
                pass
            
            # Método 2: Selenium
            if not video_mode_clicked:
                try:
                    elements = self.driver.find_elements(By.XPATH,
                        "//*[contains(text(), 'Video') or contains(text(), 'Vídeo')]"
                    )
                    for elem in elements:
                        if elem.is_displayed():
                            location = elem.location
                            # Barra inferior (y > 1000)
                            if location['y'] > 1000:
                                try:
                                    elem.click()
                                    video_mode_clicked = True
                                    print(f"   ✅ Modo 'Video' clicado via Selenium! (Y={location['y']})")
                                    time.sleep(2)
                                    break
                                except:
                                    continue
                except:
                    pass
            
            if not video_mode_clicked:
                print("   ⚠️ Modo 'Video' não encontrado - pode já estar selecionado")
            
            # ============================================
            # ETAPA 3: SELECIONAR DURAÇÃO "10s"
            # ============================================
            print("\n⏱️ ETAPA 3: Selecionando duração '10s'...")
            time.sleep(1)
            
            duration_clicked = False
            
            # Método 1: Clica no "10s"
            try:
                duration_clicked = self.driver.execute_script("""
                    const elements = document.querySelectorAll('button, div, span, a, label');
                    for (let el of elements) {
                        const text = el.textContent.trim();
                        if (text === '10s' || text === '10s') {
                            el.click();
                            return true;
                        }
                    }
                    return false;
                """)
                if duration_clicked:
                    print("   ✅ Duração '10s' selecionada via JS!")
                    time.sleep(1)
            except:
                pass
            
            # Método 2: Selenium
            if not duration_clicked:
                try:
                    elements = self.driver.find_elements(By.XPATH,
                        "//*[contains(text(), '10s')]"
                    )
                    for elem in elements:
                        if elem.is_displayed():
                            location = elem.location
                            if location['y'] > 1000:
                                try:
                                    elem.click()
                                    duration_clicked = True
                                    print(f"   ✅ '10s' clicado via Selenium!")
                                    time.sleep(1)
                                    break
                                except:
                                    continue
                except:
                    pass
            
            if not duration_clicked:
                print("   ⚠️ '10s' não encontrado - usando duração padrão")
            
            # Screenshot após configurações
            debug_config = self.output_dir / f"debug_grok_config_{scene_num}.png"
            self.driver.save_screenshot(str(debug_config))
            print(f"📸 Screenshot após config: {debug_config}")
            
            # ============================================
            # ETAPA 4: DIGITAR PROMPT
            # ============================================
            print("\n⌨️ ETAPA 4: Digitando prompt de movimento...")
            time.sleep(2)
            
            # Encontra o campo de prompt
            prompt_input = None
            
            # Método 1: Procura por placeholder "Digite para o Imagine" ou "Pergunte"
            try:
                print("   Tentando método 1: Procurando por placeholder...")
                prompt_input = self.driver.execute_script("""
                    // Procura por elemento com placeholder adequado
                    const elements = document.querySelectorAll('div[contenteditable="true"], textarea, [role="textbox"], input[type="text"]');
                    for (let el of elements) {
                        const rect = el.getBoundingClientRect();
                        // Campo de input fica na parte inferior (y > 800)
                        if (rect.width > 200 && rect.height > 20 && rect.top > 800) {
                            return el;
                        }
                    }
                    
                    // Fallback: procura por div com placeholder
                    const allDivs = document.querySelectorAll('div');
                    for (let div of allDivs) {
                        const placeholder = div.getAttribute('data-placeholder') || div.getAttribute('placeholder') || '';
                        if (placeholder.includes('Imagine') || placeholder.includes('Pergunte') || 
                            placeholder.includes('Digite') || placeholder.includes('Ask')) {
                            return div;
                        }
                    }
                    
                    // Fallback 2: procura por texto do placeholder
                    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
                    while (walker.nextNode()) {
                        const node = walker.currentNode;
                        const text = node.textContent;
                        if (text.includes('Digite para o Imagine') || text.includes('Pergunte alguma coisa') ||
                            text.includes('Ask anything') || text.includes('Type to imagine')) {
                            return node.parentElement;
                        }
                    }
                    return null;
                """)
                if prompt_input:
                    print("   ✅ Campo de prompt encontrado via JS!")
            except Exception as e:
                print(f"   ✗ Método 1 falhou: {str(e)[:80]}")
            
            # Método 2: Selenium - procura por contenteditable
            if not prompt_input:
                try:
                    print("   Tentando método 2: contenteditable...")
                    elements = self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true']")
                    for elem in elements:
                        if elem.is_displayed():
                            location = elem.location
                            if location['y'] > 800:
                                prompt_input = elem
                                print("   ✅ Encontrado via contenteditable!")
                                break
                except Exception as e:
                    print(f"   ✗ Método 2 falhou: {str(e)[:50]}")
            
            # Método 3: Procura textarea
            if not prompt_input:
                try:
                    print("   Tentando método 3: textarea...")
                    elements = self.driver.find_elements(By.TAG_NAME, "textarea")
                    for elem in elements:
                        if elem.is_displayed():
                            prompt_input = elem
                            print("   ✅ Encontrado textarea!")
                            break
                except Exception as e:
                    print(f"   ✗ Método 3 falhou: {str(e)[:50]}")
            
            # Método 4: Clica na área do input diretamente
            if not prompt_input:
                try:
                    print("   Tentando método 4: Clicando na área do input...")
                    clicked = self.driver.execute_script("""
                        // Procura qualquer elemento clicável na parte inferior
                        const elements = document.querySelectorAll('div, span, p');
                        for (let el of elements) {
                            const rect = el.getBoundingClientRect();
                            const text = el.textContent || '';
                            // Verifica se é o placeholder ou está perto dele
                            if (rect.top > 850 && rect.top < 950 && rect.width > 100) {
                                if (text.includes('Digite') || text.includes('Imagine') || text.includes('Pergunte')) {
                                    return el;
                                }
                            }
                        }
                        return null;
                    """)
                    if clicked:
                        prompt_input = clicked
                        print("   ✅ Encontrado via área do placeholder!")
                except Exception as e:
                    print(f"   ✗ Método 4 falhou: {str(e)[:50]}")
            
            if not prompt_input:
                debug_prompt = self.output_dir / f"debug_grok_no_prompt_{scene_num}.png"
                self.driver.save_screenshot(str(debug_prompt))
                print(f"   📸 Screenshot: {debug_prompt}")
                raise Exception("Campo de prompt não encontrado")
            
            # Clica no campo e digita o prompt
            try:
                prompt_input.click()
                time.sleep(1)
                
                # Limpa campo
                try:
                    self.driver.execute_script("arguments[0].textContent = '';", prompt_input)
                except:
                    try:
                        prompt_input.clear()
                    except:
                        pass
                
                time.sleep(0.5)
                
                # Digita o prompt
                prompt_input.send_keys(movement_prompt)
                print(f"   ✅ Prompt enviado: {movement_prompt[:50]}...")
                time.sleep(2)
                
            except Exception as e:
                # Fallback via JS
                print(f"   ⚠️ Método direto falhou, tentando JS...")
                self.driver.execute_script("""
                    const el = arguments[0];
                    el.focus();
                    el.textContent = arguments[1];
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                """, prompt_input, movement_prompt)
                print("   ✅ Prompt enviado via JS")
                time.sleep(2)
            
            # Screenshot após prompt
            debug_apos_prompt = self.output_dir / f"debug_grok_apos_prompt_{scene_num}.png"
            self.driver.save_screenshot(str(debug_apos_prompt))
            print(f"📸 Screenshot após prompt: {debug_apos_prompt}")
            
            # ============================================
            # ETAPA 5: CLICAR BOTÃO ENVIAR
            # ============================================
            print("\n🖱️ ETAPA 5: Enviando prompt...")
            time.sleep(2)
            
            send_clicked = False
            
            # MÉTODO PRINCIPAL: Enter no campo de prompt (mais confiável)
            try:
                print("   Método Enter: reencontrando campo de prompt...")
                fresh_prompt = self.driver.execute_script("""
                    const elements = document.querySelectorAll('textarea, div[contenteditable="true"], [role="textbox"]');
                    for (let el of elements) {
                        const rect = el.getBoundingClientRect();
                        if (rect.top > 800 && rect.width > 200) return el;
                    }
                    return null;
                """)
                if fresh_prompt:
                    # Clica no campo para garantir foco
                    self.driver.execute_script("arguments[0].click();", fresh_prompt)
                    time.sleep(0.5)
                    
                    # Digita Enter via ActionChains (mais confiável que send_keys)
                    from selenium.webdriver.common.action_chains import ActionChains
                    from selenium.webdriver.common.keys import Keys
                    ActionChains(self.driver).click(fresh_prompt).send_keys(Keys.RETURN).perform()
                    send_clicked = True
                    print("   ✅ Enter enviado via ActionChains!")
                else:
                    print("   ⚠️ Campo de prompt não reencontrado")
            except Exception as e:
                print(f"   ✗ Enter falhou: {str(e)[:80]}")
            
            # FALLBACK: Clica no botão de enviar por coordenadas relativas ao prompt
            if not send_clicked:
                try:
                    print("   Método coordenadas: clicando à direita do prompt...")
                    clicked = self.driver.execute_script("""
                        const promptArea = document.querySelector('textarea, div[contenteditable="true"], [role="textbox"]');
                        if (!promptArea) return false;
                        
                        const promptRect = promptArea.getBoundingClientRect();
                        
                        // O botão de enviar fica ~50px à direita do final do prompt, na mesma linha
                        const targetX = promptRect.right + 50;
                        const targetY = promptRect.top + (promptRect.height / 2);
                        
                        // Usa.elementFromPoint para encontrar o que está nessa posição
                        const element = document.elementFromPoint(targetX, targetY);
                        if (element) {
                            // Sobe na árvore DOM até encontrar um button
                            let current = element;
                            for (let i = 0; i < 10; i++) {
                                if (!current) break;
                                if (current.tagName === 'BUTTON') {
                                    current.click();
                                    return true;
                                }
                                current = current.parentElement;
                            }
                        }
                        
                        // Se não encontrou, tenta position fixa (mais à direita)
                        const targetX2 = Math.min(promptRect.right + 80, window.innerWidth - 50);
                        const element2 = document.elementFromPoint(targetX2, targetY);
                        if (element2) {
                            element2.click();
                            return true;
                        }
                        return false;
                    """)
                    if clicked:
                        send_clicked = True
                        print("   ✅ Botão clicado via coordenadas!")
                except Exception as e:
                    print(f"   ✗ Coordenadas falharam: {str(e)[:80]}")
            
            # FALLBACK 2: JavaScript dispatch de evento de tecla Enter
            if not send_clicked:
                try:
                    print("   Método JS: dispatch keyboard event...")
                    self.driver.execute_script("""
                        const promptArea = document.querySelector('textarea, div[contenteditable="true"], [role="textbox"]');
                        if (promptArea) {
                            promptArea.focus();
                            const event = new KeyboardEvent('keydown', {
                                key: 'Enter',
                                code: 'Enter',
                                keyCode: 13,
                                which: 13,
                                bubbles: true
                            });
                            promptArea.dispatchEvent(event);
                            
                            // Também tenta keypress e keyup
                            const event2 = new KeyboardEvent('keypress', {
                                key: 'Enter',
                                code: 'Enter',
                                keyCode: 13,
                                which: 13,
                                bubbles: true
                            });
                            promptArea.dispatchEvent(event2);
                            
                            const event3 = new KeyboardEvent('keyup', {
                                key: 'Enter',
                                code: 'Enter',
                                keyCode: 13,
                                which: 13,
                                bubbles: true
                            });
                            promptArea.dispatchEvent(event3);
                        }
                    """)
                    send_clicked = True
                    print("   ✅ Keyboard event dispatchado!")
                except Exception as e:
                    print(f"   ✗ JS keyboard falhou: {str(e)[:80]}")
            
            if not send_clicked:
                debug_failed = self.output_dir / f"debug_grok_send_failed_{scene_num}.png"
                self.driver.save_screenshot(str(debug_failed))
                print(f"   📸 Screenshot: {debug_failed}")
                raise Exception("Não foi possível clicar no botão enviar")
            
            # Screenshot após enviar
            time.sleep(3)
            debug_aposEnviar = self.output_dir / f"debug_grok_apos_enviar_{scene_num}.png"
            self.driver.save_screenshot(str(debug_aposEnviar))
            print(f"📸 Screenshot após enviar: {debug_aposEnviar}")
            
            # ============================================
            # ETAPA 6: AGUARDAR GERAÇÃO DO VÍDEO
            # ============================================
            print("\n⏳ ETAPA 6: Aguardando geração do vídeo...")
            print("   (Grok pode levar 2-5 minutos para gerar)")
            
            # IMPORTANTE: Salva URLs de vídeos ANTIGOS para ignorar
            old_video_urls = set()
            old_blob_urls = set()
            try:
                old_videos = self.driver.find_elements(By.TAG_NAME, "video")
                for v in old_videos:
                    src = v.get_attribute("src")
                    if src:
                        old_video_urls.add(src)
                        if src.startswith("blob:"):
                            old_blob_urls.add(src)
                # Também coleta blob URLs via JS
                old_blobs_js = self.driver.execute_script("""
                    const blobs = [];
                    document.querySelectorAll('video').forEach(v => {
                        if (v.src && v.src.startsWith('blob:')) blobs.push(v.src);
                        if (v.srcObject) {
                            try {
                                const url = URL.createObjectURL(v.srcObject);
                                blobs.push(url);
                            } catch(e) {}
                        }
                    });
                    return blobs;
                """) or []
                old_blob_urls.update(old_blobs_js)
                if old_video_urls:
                    print(f"   ℹ️  {len(old_video_urls)} vídeos antigos, {len(old_blob_urls)} blob URLs - aguardando NOVO...")
            except:
                pass
            
            video_found = False
            video_url = None
            max_wait_time = 300  # 5 minutos
            check_interval = 5   # Verifica a cada 5 segundos
            elapsed = 0
            
            while elapsed < max_wait_time and not video_found:
                # Calcula tempo restante
                remaining = max_wait_time - elapsed
                mins, secs = divmod(remaining, 60)
                print(f"\r   ⏱️  Aguardando... {mins:02d}:{secs:02d} restantes", end='', flush=True)
                
                try:
                    # Verifica se NOVO vídeo apareceu (múltiplos métodos)
                    videos = self.driver.find_elements(By.TAG_NAME, "video")
                    for video in videos:
                        src = video.get_attribute("src")
                        if src and len(src) > 10:
                            if src.startswith("blob:"):
                                if src not in old_blob_urls:
                                    video_found = True
                                    video_url = src
                                    print(f"\n✓ NOVO vídeo (blob) encontrado após {elapsed}s!")
                                    break
                            elif src not in old_video_urls:
                                video_found = True
                                video_url = src
                                print(f"\n✓ NOVO vídeo encontrado após {elapsed}s!")
                                break
                    
                    # Se não encontrou via <video>, verifica via JS por blob URLs
                    if not video_found:
                        new_blobs = self.driver.execute_script("""
                            const blobs = [];
                            document.querySelectorAll('video').forEach(v => {
                                if (v.src && v.src.startsWith('blob:') && !arguments[0].includes(v.src)) {
                                    blobs.push(v.src);
                                }
                                // Verifica também source elements
                                v.querySelectorAll('source').forEach(s => {
                                    if (s.src && s.src.startsWith('blob:') && !arguments[0].includes(s.src)) {
                                        blobs.push(s.src);
                                    }
                                });
                            });
                            return blobs;
                        """, list(old_blob_urls)) or []
                        
                        if new_blobs:
                            video_found = True
                            video_url = new_blobs[0]
                            print(f"\n✓ NOVO vídeo (via JS) encontrado após {elapsed}s!")
                    
                    # Verifica também se há botão de download de vídeo (indica que geração terminou)
                    if not video_found and elapsed > 30:
                        download_indicators = self.driver.find_elements(By.XPATH,
                            "//button[contains(., 'Baixar vídeo') or contains(., 'Download video')]"
                        )
                        if download_indicators:
                            print(f"\n   ℹ️  Botão de download encontrado - vídeo pode estar pronto")
                            # Ainda assim espera um pouco mais para o <video> aparecer
                except Exception as e:
                    pass
                
                if not video_found:
                    time.sleep(check_interval)
                    elapsed += check_interval
            
            if not video_found:
                # Screenshot final
                debug_final = self.output_dir / f"debug_grok_timeout_{scene_num}.png"
                self.driver.save_screenshot(str(debug_final))
                print(f"\n📸 Screenshot timeout: {debug_final}")
                
                # Lista o que há na página para debug
                print("   Debug: verificando elementos na página...")
                try:
                    all_videos = self.driver.find_elements(By.TAG_NAME, "video")
                    print(f"   - {len(all_videos)} elementos <video>")
                    for v in all_videos:
                        src = v.get_attribute("src")
                        print(f"     src: {src[:80] if src else 'None'}")
                    
                    # Verifica se há algo que pareça ser um player de vídeo
                    players = self.driver.find_elements(By.CSS_SELECTOR, 
                        "[class*='video'], [class*='player'], [data-testid*='video']"
                    )
                    print(f"   - {len(players)} possíveis players de vídeo")
                except:
                    pass
                
                raise Exception(f"Vídeo não foi gerado em {max_wait_time} segundos")
            
            # ============================================
            # ETAPA 7: DOWNLOAD DO VÍDEO
            # ============================================
            print("\n📥 ETAPA 7: Fazendo download do vídeo...")
            
            download_clicked = False
            try:
                # IMPORTANTE: Procurar especificamente por botão de VÍDEO (não imagem!)
                # Após o vídeo ser gerado, aparece botão "Baixar vídeo" ou "Download video"
                
                # Aguarda o botão de download aparecer (pode demorar após geração)
                print("   Aguardando botão de download aparecer...")
                time.sleep(5)
                
                # Tenta até 10 vezes (30 segundos total)
                for attempt in range(10):
                    download_buttons = self.driver.find_elements(By.XPATH, 
                        "//button[contains(., 'Baixar vídeo') or contains(., 'baixar vídeo') or contains(., 'Download video') or contains(., 'download video') or contains(., 'Baixar') or contains(., 'Download')] | "
                        "//a[contains(., 'Baixar vídeo') or contains(., 'baixar vídeo') or contains(., 'Download video') or contains(., 'download video') or contains(., 'Baixar') or contains(., 'Download')]"
                    )
                    
                    if attempt == 0:
                        print(f"   Encontrados {len(download_buttons)} botões de download")
                    
                    for btn in download_buttons:
                        if btn.is_displayed():
                            location = btn.location
                            # Ignora sidebar
                            if location['x'] < 200:
                                continue
                            
                            text = btn.text.strip()
                            
                            # Debug: mostra todos os botões
                            if attempt == 0:
                                print(f"   Botão encontrado: '{text}' @ X={location['x']}")
                            
                            # Prioridade 1: Botão com "vídeo" ou "video" no texto
                            if 'vídeo' in text.lower() or 'video' in text.lower():
                                btn.click()
                                download_clicked = True
                                print(f"   ✓ Botão de download de VÍDEO clicado: '{text}'")
                                break
                            
                            # Prioridade 2: Qualquer botão de download que NÃO seja de imagem
                            elif ('baixar' in text.lower() or 'download' in text.lower()) and \
                                 'imagem' not in text.lower() and 'image' not in text.lower():
                                btn.click()
                                download_clicked = True
                                print(f"   ✓ Botão de download clicado: '{text}'")
                                break
                    
                    if download_clicked:
                        break
                    
                    # Se não encontrou, aguarda mais um pouco
                    if attempt < 9:
                        time.sleep(3)
                        print(f"   Tentativa {attempt + 2}/10...")
                
                # Se não encontrou por texto específico, procura por ícone de download
                if not download_clicked:
                    print("   Procurando ícone de download de vídeo...")
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    
                    for btn in buttons:
                        if btn.is_displayed():
                            location = btn.location
                            if location['x'] < 200:
                                continue
                            
                            # Verifica se tem SVG que pode ser ícone de download
                            svgs = btn.find_elements(By.TAG_NAME, "svg")
                            if svgs:
                                # Verifica atributos do botão
                                aria_label = btn.get_attribute('aria-label') or ''
                                title = btn.get_attribute('title') or ''
                                
                                # Procura especificamente por VÍDEO
                                if (('video' in aria_label.lower() or 'vídeo' in aria_label.lower()) and \
                                   ('download' in aria_label.lower() or 'baixar' in aria_label.lower())) or \
                                   (('download' in aria_label.lower() or 'baixar' in aria_label.lower()) and \
                                   'image' not in aria_label.lower() and 'imagem' not in aria_label.lower()):
                                    print(f"   Encontrado por aria-label: '{aria_label}'")
                                    btn.click()
                                    download_clicked = True
                                    print("   ✓ Botão de download de vídeo clicado!")
                                    break
                                elif (('video' in title.lower() or 'vídeo' in title.lower()) and \
                                     ('download' in title.lower() or 'baixar' in title.lower())) or \
                                     (('download' in title.lower() or 'baixar' in title.lower()) and \
                                     'image' not in title.lower() and 'imagem' not in title.lower()):
                                    print(f"   Encontrado por title: '{title}'")
                                    btn.click()
                                    download_clicked = True
                                    print("   ✓ Botão de download de vídeo clicado!")
                                    break
                
                if download_clicked:
                    print("✓ Download iniciado via botão da interface")
                    time.sleep(5)  # Aguarda download começar
                    
                    # O Chrome está configurado para baixar em self.videos_dir
                    # Procura pelo arquivo de vídeo mais recente
                    print("   Procurando arquivo baixado...")
                    video_path = self.videos_dir / f"scene_{scene_num:03d}.mp4"
                    
                    # Aguarda até 30 segundos para o arquivo aparecer
                    for wait_time in range(30):
                        # Procura arquivos de vídeo recentes na pasta videos/
                        video_files = list(self.videos_dir.glob("*.mp4")) + list(self.videos_dir.glob("*.webm"))
                        
                        if video_files:
                            # Pega o mais recente
                            latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                            
                            # Verifica se foi modificado nos últimos 30 segundos
                            if time.time() - latest_video.stat().st_mtime < 30:
                                print(f"   ✓ Arquivo encontrado: {latest_video.name}")
                                
                                # Se o nome não for o esperado, renomeia
                                if latest_video != video_path:
                                    shutil.move(str(latest_video), str(video_path))
                                    print(f"   ✓ Renomeado para: {video_path.name}")
                                
                                # Validação
                                if self._validate_video(video_path):
                                    print(f"✓ Vídeo salvo: {video_path}")
                                    return str(video_path)
                                break
                        
                        time.sleep(1)
                    
                    # Se não encontrou, tenta o método antigo
                    print("   ⚠️ Arquivo não encontrado em output/videos/, tentando método direto...")
                
            except Exception as e:
                print(f"   ✗ Erro ao clicar no botão de download: {str(e)[:100]}")
            
            # FALLBACK: Se não conseguiu via botão, tenta download direto via URL
            if not download_clicked:
                print("   Tentando download direto via URL...")
                try:
                    # RE-BUSCA os vídeos (evita stale element)
                    videos = self.driver.find_elements(By.TAG_NAME, "video")
                    
                    if not videos:
                        raise Exception("Nenhum elemento de vídeo encontrado na página")
                    
                    for video in videos:
                        try:
                            src = video.get_attribute("src")
                            if src and len(src) > 10:  # URL válida
                                video_path = self.videos_dir / f"scene_{scene_num:03d}.mp4"
                                print(f"   📥 URL do vídeo: {src[:100]}...")
                                self._download_video(video, video_path)
                                
                                # Validação
                                if self._validate_video(video_path):
                                    print(f"✓ Vídeo salvo: {video_path}")
                                    
                                    # Incrementa contador de cenas processadas
                                    self.scenes_processed += 1
                                    
                                    return str(video_path)
                        except Exception as e:
                            print(f"   ✗ Erro com este vídeo: {str(e)[:100]}")
                            continue
                    
                except Exception as e:
                    print(f"   ✗ Erro no download direto: {str(e)[:100]}")
                    
                    # ÚLTIMO RECURSO: JavaScript para forçar download
                    print("   Tentando download via JavaScript...")
                    try:
                        downloaded = self.driver.execute_script("""
                            const video = document.querySelector('video');
                            if (!video || !video.src) return false;
                            
                            // Cria link de download
                            const a = document.createElement('a');
                            a.href = video.src;
                            a.download = 'grok_video.mp4';
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                            
                            return true;
                        """)
                        
                        if downloaded:
                            print("   ✓ Download iniciado via JavaScript")
                            time.sleep(5)
                            
                            # Procura arquivo baixado
                            for wait_time in range(30):
                                video_files = list(self.videos_dir.glob("*.mp4")) + list(self.videos_dir.glob("*.webm"))
                                
                                if video_files:
                                    latest_video = max(video_files, key=lambda p: p.stat().st_mtime)
                                    
                                    if time.time() - latest_video.stat().st_mtime < 30:
                                        video_path = self.videos_dir / f"scene_{scene_num:03d}.mp4"
                                        
                                        if latest_video != video_path:
                                            shutil.move(str(latest_video), str(video_path))
                                        
                                        if self._validate_video(video_path):
                                            print(f"✓ Vídeo salvo via JavaScript: {video_path}")
                                            
                                            # Incrementa contador de cenas processadas
                                            self.scenes_processed += 1
                                            
                                            return str(video_path)
                                        break
                                
                                time.sleep(1)
                    except Exception as js_error:
                        print(f"   ✗ JavaScript download falhou: {str(js_error)[:100]}")
            
            # FALLBACK FINAL: Tentar extrair vídeo via blob URL
            print("   🔄 FALLBACK FINAL: Extraindo vídeo via blob URL...")
            try:
                # Encontra o elemento <video> mais recente
                video_data = self.driver.execute_script("""
                    const videos = document.querySelectorAll('video');
                    let newest = null;
                    let newestTime = 0;
                    
                    for (const v of videos) {
                        const src = v.src || '';
                        if (src.startsWith('blob:')) {
                            // Pega o timestamp do objeto
                            const time = v.currentTime || 0;
                            if (time > newestTime || !newest) {
                                newest = v;
                                newestTime = time;
                            }
                        }
                    }
                    
                    if (!newest) return null;
                    
                    return {
                        src: newest.src,
                        duration: newest.duration,
                        readyState: newest.readyState
                    };
                """)
                
                if video_data and video_data.get('src'):
                    blob_url = video_data['src']
                    print(f"   📹 Blob URL encontrado: {blob_url[:80]}...")
                    print(f"   Duração: {video_data.get('duration', 'N/A')}s, ReadyState: {video_data.get('readyState', 'N/A')}")
                    
                    # Tenta converter blob para base64 via fetch
                    video_base64 = self.driver.execute_script("""
                        async function blobToBase64(url) {
                            try {
                                const response = await fetch(url);
                                const blob = await response.blob();
                                return new Promise((resolve) => {
                                    const reader = new FileReader();
                                    reader.onloadend = () => resolve(reader.result);
                                    reader.readAsDataURL(blob);
                                });
                            } catch(e) {
                                return null;
                            }
                        }
                        return await blobToBase64(arguments[0]);
                    """, blob_url)
                    
                    if video_base64 and video_base64.startswith('data:'):
                        # Decodifica base64 e salva
                        import base64
                        header, data = video_base64.split(',', 1)
                        video_bytes = base64.b64decode(data)
                        
                        video_path = self.videos_dir / f"scene_{scene_num:03d}.mp4"
                        with open(video_path, 'wb') as f:
                            f.write(video_bytes)
                        
                        print(f"   ✓ Vídeo extraído via blob: {len(video_bytes)} bytes")
                        
                        if self._validate_video(video_path):
                            print(f"✓ Vídeo salvo via blob extraction: {video_path}")
                            self.scenes_processed += 1
                            return str(video_path)
                    
                    # Se base64 falhou, tenta download via link
                    print("   Tentando download via link criado...")
                    downloaded = self.driver.execute_script("""
                        const video = document.querySelector('video[src^="blob:"]');
                        if (!video) return false;
                        
                        const a = document.createElement('a');
                        a.href = video.src;
                        a.download = 'grok_video_' + Date.now() + '.mp4';
                        a.style.display = 'none';
                        document.body.appendChild(a);
                        a.click();
                        
                        setTimeout(() => document.body.removeChild(a), 1000);
                        return true;
                    """)
                    
                    if downloaded:
                        print("   ✓ Download via link iniciado")
                        time.sleep(10)
                        
                        # Procura arquivo
                        for _ in range(20):
                            video_files = list(self.videos_dir.glob("*.mp4")) + list(self.videos_dir.glob("*.webm"))
                            if video_files:
                                latest = max(video_files, key=lambda p: p.stat().st_mtime)
                                if time.time() - latest.stat().st_mtime < 30:
                                    video_path = self.videos_dir / f"scene_{scene_num:03d}.mp4"
                                    if latest != video_path:
                                        shutil.move(str(latest), str(video_path))
                                    if self._validate_video(video_path):
                                        print(f"✓ Vídeo salvo via link: {video_path}")
                                        self.scenes_processed += 1
                                        return str(video_path)
                            time.sleep(1)
                
            except Exception as blob_error:
                print(f"   ✗ Blob extraction falhou: {str(blob_error)[:100]}")
            
            raise Exception("Não foi possível baixar o vídeo por nenhum método")
            
        except Exception as e:
            print(f"✗ Erro ao gerar vídeo: {e}")
            raise
    
    def _download_video(self, video_element, save_path: Path):
        """Baixa vídeo usando elemento ou fazendo download com cookies"""
        try:
            # Pega a URL do vídeo
            src = video_element.get_attribute("src")
            
            if not src:
                raise Exception("Vídeo sem URL (src)")
            
            print(f"   📥 URL do vídeo: {src[:80]}...")
            
            # Método 1: Tentar baixar com cookies do Selenium (evita 403)
            try:
                # Pega cookies do navegador
                selenium_cookies = self.driver.get_cookies()
                cookies_dict = {cookie['name']: cookie['value'] for cookie in selenium_cookies}
                
                # Headers necessários
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Referer': 'https://grok.com/',
                }
                
                print("   ⏬ Baixando vídeo com autenticação...")
                response = requests.get(src, cookies=cookies_dict, headers=headers, stream=True, timeout=120)
                response.raise_for_status()
                
                # Baixa o vídeo
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            # Mostra progresso a cada 1MB
                            if downloaded % (1024 * 1024) == 0:
                                mb_downloaded = downloaded / (1024 * 1024)
                                print(f"\r   ⏬ Baixado: {mb_downloaded:.1f}MB", end='', flush=True)
                
                print(f"\n   ✓ Vídeo baixado com sucesso!")
                return
                
            except Exception as e:
                print(f"\n   ✗ Erro ao baixar com cookies: {str(e)[:100]}")
            
            # Método 2: Tentar usar JavaScript para baixar via blob
            try:
                print("   Tentando método alternativo (blob)...")
                
                # Cria blob e baixa via JavaScript
                self.driver.execute_script("""
                    var video = arguments[0];
                    var url = video.src;
                    var a = document.createElement('a');
                    a.href = url;
                    a.download = arguments[1];
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                """, video_element, save_path.name)
                
                # Aguarda download (tempo variável)
                time.sleep(10)
                print("   ⚠️ Download via blob iniciado (verifique pasta de downloads)")
                
            except Exception as e2:
                print(f"   ✗ Método alternativo falhou: {str(e2)[:100]}")
                raise Exception(f"Todos os métodos de download falharam. Último erro: {e}")
                
        except Exception as e:
            print(f"   ✗ Erro ao baixar vídeo: {e}")
            raise
    
    def _validate_video(self, video_path: Path) -> bool:
        """Valida se o vídeo foi baixado corretamente"""
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                print("✗ Não foi possível abrir o vídeo")
                return False
            
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            duration = frame_count / fps if fps > 0 else 0
            
            cap.release()
            
            # Validações básicas
            if frame_count < 10:
                print("✗ Vídeo muito curto")
                return False
            
            print(f"✓ Vídeo validado: {duration:.2f}s, {frame_count} frames, {fps} FPS")
            return True
            
        except Exception as e:
            print(f"✗ Validação falhou: {e}")
            return False
    
    def extract_last_frame(self, video_path: str, scene_num: int) -> str:
        """Extrai o último frame do vídeo"""
        print(f"\n🖼️ Extraindo último frame da cena {scene_num}...")
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Vai para o último frame
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
            ret, frame = cap.read()
            
            if ret:
                frame_path = self.frames_dir / f"scene_{scene_num:03d}_last_frame.png"
                cv2.imwrite(str(frame_path), frame)
                print(f"✓ Frame extraído: {frame_path}")
                
                cap.release()
                return str(frame_path)
            else:
                raise Exception("Não foi possível ler o último frame")
                
        except Exception as e:
            print(f"✗ Erro ao extrair frame: {e}")
            raise
    
    def upscale_video(self, video_path: str, scene_num: int, scale: int = 2) -> str:
        """
        Faz upscaling do vídeo usando FFmpeg com filtros de IA
        
        Args:
            video_path: Caminho do vídeo original
            scene_num: Número da cena
            scale: Fator de escala (2 = 2x resolução, 4 = 4x resolução)
        
        Returns:
            Caminho do vídeo upscaled
        """
        print(f"\n🎨 Fazendo upscaling do vídeo (escala {scale}x)...")
        print(f"   📂 Vídeo original: {video_path}")
        
        try:
            import subprocess
            import shutil
            
            # Verifica se FFmpeg existe
            ffmpeg_path = shutil.which('ffmpeg')
            if not ffmpeg_path:
                print(f"   ⚠️ FFmpeg não encontrado no PATH!")
                print(f"   💡 Reinicie o terminal e tente novamente")
                print(f"   ⚠️ Mantendo vídeo original")
                return str(video_path)
            
            print(f"   ✓ FFmpeg encontrado: {ffmpeg_path}")
            
            # Caminho do vídeo HD
            hd_path = self.videos_hd_dir / f"scene_{scene_num:03d}_hd.mp4"
            print(f"   📂 Vídeo HD será salvo em: {hd_path}")
            
            # Comando FFmpeg com filtro Lanczos (melhor qualidade)
            cmd = [
                'ffmpeg',
                '-i', str(video_path),
                '-vf', f'scale=iw*{scale}:ih*{scale}:flags=lanczos',
                '-c:v', 'libx264',
                '-preset', 'slow',
                '-crf', '18',
                '-pix_fmt', 'yuv420p',
                '-y',
                str(hd_path)
            ]
            
            print(f"   🔧 Executando FFmpeg...")
            print(f"   ⏳ Isso pode levar 10-30 segundos...")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Verifica tamanho
                original_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                hd_size = os.path.getsize(hd_path) / (1024 * 1024)  # MB
                
                print(f"   ✓ Upscaling concluído!")
                print(f"   📊 Original: {original_size:.2f} MB → HD: {hd_size:.2f} MB")
                print(f"   📁 Vídeo HD: {hd_path}")
                
                return str(hd_path)
            else:
                print(f"   ❌ FFmpeg falhou!")
                print(f"   📋 Erro: {result.stderr[:200]}")
                print(f"   ⚠️ Mantendo vídeo original")
                return str(video_path)
                
        except FileNotFoundError as e:
            print(f"   ⚠️ FFmpeg não encontrado! ({e})")
            print(f"   💡 Instale com: winget install ffmpeg")
            print(f"   ⚠️ Mantendo vídeo original")
            return str(video_path)
        except Exception as e:
            print(f"   ❌ Erro inesperado no upscaling: {e}")
            print(f"   ⚠️ Mantendo vídeo original")
            return str(video_path)
    
    def process_roteiro(self, json_path: str):
        """Processa o roteiro completo"""
        print("\n" + "="*60)
        print("🎬 VIDEO GENERATOR - Iniciando processamento")
        print("="*60)
        
        start_time = datetime.now()
        
        try:
            # Carrega roteiro
            roteiro = self.load_roteiro(json_path)
            
            # Configura navegador
            self.setup_browser()
            
            # Processa cada cena
            for i, cena in enumerate(roteiro['cenas'], 1):
                print(f"\n{'='*60}")
                print(f"🎬 PROCESSANDO CENA {i}/{len(roteiro['cenas'])}")
                print(f"{'='*60}")
                
                # 1. Obter/gerar imagem inicial
                if cena.get('use_previous_frame', False) and self.last_frame:
                    print(f"🔄 Usando último frame da cena anterior")
                    image_path = self.last_frame
                else:
                    image_path = self.generate_image_dalle(
                        cena['dalle_prompt'], 
                        i
                    )
                
                # 2. Gerar vídeo no Grok
                video_path = self.generate_video_grok(
                    image_path,
                    cena['grok_movement'],
                    i
                )
                
                # 2.5 UPSCALING (se habilitado no roteiro)
                upscale_enabled = roteiro.get('upscale_videos', True)
                print(f"\n🔧 Verificando upscaling...")
                print(f"   upscale_videos = {upscale_enabled}")
                
                if upscale_enabled:
                    scale_factor = roteiro.get('upscale_factor', 2)
                    print(f"   upscale_factor = {scale_factor}x")
                    print(f"   ▶️ INICIANDO UPSCALING...")
                    video_path = self.upscale_video(video_path, i, scale_factor)
                else:
                    print(f"   ⏭️ Upscaling desabilitado no JSON")
                
                # 3. Extrair último frame
                self.last_frame = self.extract_last_frame(video_path, i)
                
                print(f"✅ Cena {i} concluída!")
                
                # 4. ESPERA ENTRE CENAS (exceto na última)
                if i < len(roteiro['cenas']):
                    print(f"\n⏸️  AGUARDANDO {self.wait_between_scenes // 60} MINUTOS ANTES DA PRÓXIMA CENA...")
                    print(f"   (Respeitando rate limits do DALL-E e Grok)")
                    print(f"   Cena {i} concluída | Próxima: Cena {i+1}")
                    
                    # Contador regressivo
                    remaining = self.wait_between_scenes
                    while remaining > 0:
                        mins, secs = divmod(remaining, 60)
                        print(f"\r   ⏱️  Tempo restante: {mins:02d}:{secs:02d}", end='', flush=True)
                        time.sleep(1)
                        remaining -= 1
                    
                    print(f"\n✅ Espera concluída! Iniciando cena {i+1}...")
            
            # Finalização
            elapsed = datetime.now() - start_time
            print("\n" + "="*60)
            print("🎉 PROCESSAMENTO CONCLUÍDO!")
            print(f"⏱️ Tempo total: {elapsed}")
            print(f"📁 Arquivos salvos em: {self.output_dir}")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ ERRO: {e}")
            print("\n⚠️ NAVEGADOR NÃO FOI FECHADO - você pode ver o que aconteceu!")
            print("   Feche manualmente quando terminar de investigar")
            raise
        # finally:
        #     if self.driver:
        #         self.driver.quit()
        #         print("\n✓ Navegador fechado")
    
    def create_summary(self):
        """Cria resumo dos arquivos gerados"""
        summary_path = self.output_dir / "summary.txt"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("RESUMO DA GERAÇÃO DE VÍDEOS\n")
            f.write("="*50 + "\n\n")
            
            f.write("IMAGENS GERADAS:\n")
            for img in sorted(self.images_dir.glob("*.png")):
                f.write(f"  - {img.name}\n")
            
            f.write("\nVÍDEOS GERADOS:\n")
            for vid in sorted(self.videos_dir.glob("*.mp4")):
                f.write(f"  - {vid.name}\n")
            
            f.write("\nFRAMES EXTRAÍDOS:\n")
            for frame in sorted(self.frames_dir.glob("*.png")):
                f.write(f"  - {frame.name}\n")
        
        print(f"📋 Resumo salvo em: {summary_path}")


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Video Generator - Automação de criação de vídeos'
    )
    parser.add_argument(
        'roteiro',
        help='Caminho para o arquivo roteiro.json'
    )
    parser.add_argument(
        '-o', '--output',
        default='./output',
        help='Diretório de saída (padrão: ./output)'
    )
    
    args = parser.parse_args()
    
    # Inicia processamento
    generator = VideoGenerator(output_dir=args.output)
    generator.process_roteiro(args.roteiro)
    generator.create_summary()


if __name__ == "__main__":
    main()
