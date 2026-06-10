#!/usr/bin/env python3
"""
Setup e validação do ambiente Video Generator
"""

import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_chrome():
    """Verifica se Chrome está instalado"""
    print("\n🌐 Verificando Chrome...")
    
    system = platform.system()
    
    try:
        if system == "Windows":
            result = subprocess.run(
                ["reg", "query", "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon", "/v", "version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Chrome instalado")
                return True
        else:
            result = subprocess.run(
                ["google-chrome", "--version"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {version}")
                return True
    except:
        pass
    
    print("❌ Chrome não encontrado")
    print("   Instale o Google Chrome: https://www.google.com/chrome/")
    return False


def install_dependencies():
    """Instala dependências do requirements.txt"""
    print("\n📦 Instalando dependências...")
    
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso")
            return True
        else:
            print("❌ Erro ao instalar dependências")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def verify_imports():
    """Verifica se os módulos podem ser importados"""
    print("\n🔍 Verificando módulos...")
    
    modules = {
        "selenium": "Selenium WebDriver",
        "PIL": "Pillow (Imagens)",
        "cv2": "OpenCV (Vídeos)",
        "requests": "Requests (HTTP)"
    }
    
    all_ok = True
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} - não instalado")
            all_ok = False
    
    return all_ok


def create_directories():
    """Cria diretórios necessários"""
    print("\n📁 Criando diretórios...")
    
    dirs = ["output", "output/images", "output/videos", "output/frames"]
    
    for dir_name in dirs:
        Path(dir_name).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados")
    return True


def check_roteiro():
    """Verifica se existe arquivo de roteiro de exemplo"""
    print("\n📄 Verificando roteiro de exemplo...")
    
    if Path("roteiro_exemplo.json").exists():
        print("✅ roteiro_exemplo.json encontrado")
        return True
    else:
        print("⚠️  roteiro_exemplo.json não encontrado")
        print("   Crie um arquivo roteiro.json seguindo o README.md")
        return False


def print_summary(checks):
    """Imprime resumo da configuração"""
    print("\n" + "="*60)
    print("📊 RESUMO DA CONFIGURAÇÃO")
    print("="*60)
    
    all_passed = all(checks.values())
    
    for check, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 Ambiente configurado com sucesso!")
        print("\n📖 Próximos passos:")
        print("   1. Edite roteiro_exemplo.json ou crie seu próprio roteiro")
        print("   2. Execute: python video_generator.py roteiro.json")
        print("   3. Certifique-se de estar logado no ChatGPT e Grok")
    else:
        print("\n⚠️  Alguns problemas foram encontrados")
        print("   Corrija os itens marcados com ❌ antes de continuar")
    
    return all_passed


def main():
    """Execução principal"""
    print("="*60)
    print("🎬 VIDEO GENERATOR - Setup e Validação")
    print("="*60)
    
    checks = {
        "Python 3.8+": check_python_version(),
        "Google Chrome": check_chrome(),
        "Dependências": False,  # Será atualizado
        "Módulos Python": False,  # Será atualizado
        "Diretórios": create_directories(),
        "Roteiro exemplo": check_roteiro()
    }
    
    # Instala dependências se Python e Chrome OK
    if checks["Python 3.8+"] and checks["Google Chrome"]:
        checks["Dependências"] = install_dependencies()
        if checks["Dependências"]:
            checks["Módulos Python"] = verify_imports()
    
    # Imprime resumo
    success = print_summary(checks)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
