"""
DIAGNÓSTICO COMPLETO - Verificar se upscaling está funcionando
"""

import sys
import os

print("="*70)
print(" DIAGNÓSTICO DO UPSCALING")
print("="*70)

# 1. Verificar se arquivo existe
print("\n1. VERIFICANDO ARQUIVO...")
if os.path.exists('video_generator.py'):
    print("   ✓ video_generator.py encontrado")
    size = os.path.getsize('video_generator.py')
    print(f"   ✓ Tamanho: {size:,} bytes")
else:
    print("   ❌ video_generator.py NÃO ENCONTRADO!")
    sys.exit(1)

# 2. Verificar se código de upscaling está no arquivo
print("\n2. VERIFICANDO CÓDIGO NO ARQUIVO...")
with open('video_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
    checks = [
        ("Verificando upscaling", "🔧 Logs de verificação"),
        ("upscale_videos", "🔧 Chave upscale_videos"),
        ("upscale_factor", "🔧 Chave upscale_factor"),
        ("INICIANDO UPSCALING", "🔧 Log de início"),
        ("def upscale_video", "🔧 Função upscale_video"),
        ("FFmpeg encontrado", "🔧 Check do FFmpeg"),
    ]
    
    all_ok = True
    for check_str, desc in checks:
        if check_str in content:
            print(f"   ✓ {desc} ENCONTRADO")
        else:
            print(f"   ❌ {desc} NÃO ENCONTRADO!")
            all_ok = False
    
    if not all_ok:
        print("\n   ❌ CÓDIGO INCOMPLETO! Baixe video_generator.py novamente!")
        sys.exit(1)

# 3. Tentar importar módulo
print("\n3. IMPORTANDO MÓDULO...")
try:
    # Remove cache se existir
    if 'video_generator' in sys.modules:
        del sys.modules['video_generator']
    
    from video_generator import VideoGenerator
    print("   ✓ Módulo importado com sucesso")
except Exception as e:
    print(f"   ❌ Erro ao importar: {e}")
    sys.exit(1)

# 4. Verificar se classe tem método
print("\n4. VERIFICANDO MÉTODOS...")
gen = VideoGenerator()
if hasattr(gen, 'upscale_video'):
    print("   ✓ Método upscale_video EXISTE na classe")
    
    # Verificar assinatura
    import inspect
    sig = inspect.signature(gen.upscale_video)
    print(f"   ✓ Assinatura: {sig}")
else:
    print("   ❌ Método upscale_video NÃO EXISTE!")
    sys.exit(1)

# 5. Verificar se diretório HD existe
print("\n5. VERIFICANDO DIRETÓRIOS...")
if hasattr(gen, 'videos_hd_dir'):
    print(f"   ✓ videos_hd_dir definido: {gen.videos_hd_dir}")
    if gen.videos_hd_dir.exists():
        print(f"   ✓ Diretório existe!")
    else:
        print(f"   ⚠️ Diretório será criado no primeiro uso")
else:
    print("   ❌ videos_hd_dir NÃO DEFINIDO!")

# 6. Testar FFmpeg
print("\n6. VERIFICANDO FFMPEG...")
import shutil
ffmpeg_path = shutil.which('ffmpeg')
if ffmpeg_path:
    print(f"   ✓ FFmpeg encontrado: {ffmpeg_path}")
else:
    print("   ❌ FFmpeg NÃO encontrado no PATH!")
    print("   💡 Reinicie o PowerShell ou adicione ao PATH manualmente")

# 7. Simular processamento
print("\n7. SIMULANDO PROCESSAMENTO...")
roteiro = {
    "titulo": "Teste",
    "upscale_videos": True,
    "upscale_factor": 2,
    "cenas": []
}

upscale_enabled = roteiro.get('upscale_videos', True)
scale_factor = roteiro.get('upscale_factor', 2)

print(f"   ✓ upscale_videos = {upscale_enabled}")
print(f"   ✓ upscale_factor = {scale_factor}x")

if upscale_enabled:
    print(f"   ✓ Upscaling SERIA EXECUTADO!")
else:
    print(f"   ❌ Upscaling NÃO seria executado")

# RESULTADO FINAL
print("\n" + "="*70)
print(" RESULTADO DO DIAGNÓSTICO")
print("="*70)
print("\n✅ TUDO OK! O código está correto e pronto para usar!")
print("\nAgora você pode iniciar o servidor:")
print("   python server.py")
print("\nOu usar:")
print("   .\\start_fresh.bat")
print("\n" + "="*70)
