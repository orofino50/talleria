# 🚀 INSTALACAO RAPIDA - 3 PASSOS

## 📦 Arquivos Necessarios

Baixe TODOS os arquivos acima e coloque na MESMA PASTA:

### Arquivos Principais (OBRIGATORIOS):
1. ✅ **video_generator.py** - Motor principal
2. ✅ **server.py** - Servidor Flask
3. ✅ **interface.html** - Interface web
4. ✅ **requirements.txt** - Lista de dependencias

### Scripts BAT para Windows (OBRIGATORIOS):
5. ✅ **testar_instalacao.bat** - Testa se esta tudo OK
6. ✅ **instalar_windows.bat** - Instala tudo automaticamente
7. ✅ **iniciar_servidor.bat** - Inicia o servidor

### Arquivos Extras (OPCIONAIS):
8. validate_roteiro.py - Validador de JSON
9. setup.py - Setup alternativo
10. roteiro_exemplo.json - Exemplo de roteiro

### Documentacao (RECOMENDADO):
11. README.md - Documentacao completa
12. INICIO_RAPIDO_WINDOWS.md - Guia rapido
13. INSTALACAO_WINDOWS.md - Guia detalhado
14. QUAL_ARQUIVO_EXECUTAR.md - Ordem de execucao

---

## 🎯 INSTALACAO EM 3 PASSOS

### 1️⃣ TESTAR
```
Clique 2x em: testar_instalacao.bat
```

**O que vai mostrar:**
- [OK] Python instalado
- [OK] pip funciona
- [OK] Arquivos encontrados
- [FALTA] Dependencias faltando

### 2️⃣ INSTALAR
```
Clique 2x em: instalar_windows.bat
```

**O que vai fazer:**
- Atualizar pip
- Instalar selenium, Pillow, opencv-python, requests
- Instalar Flask e flask-cors
- Confirmar instalacao

**Tempo:** 2-5 minutos

### 3️⃣ USAR
```
Clique 2x em: iniciar_servidor.bat
```

**O que vai fazer:**
- Iniciar servidor Flask
- Abrir em: http://localhost:5000
- Manter janela aberta

**Depois:**
- Abra navegador
- Digite: http://localhost:5000
- Use a interface!

---

## 📁 Estrutura da Pasta

Sua pasta deve ficar assim:

```
video-generator/
│
├── 📄 testar_instalacao.bat
├── 📄 instalar_windows.bat
├── 📄 iniciar_servidor.bat
│
├── 🐍 video_generator.py
├── 🐍 server.py
├── 🌐 interface.html
├── 📋 requirements.txt
│
├── 📚 README.md
├── 📚 INICIO_RAPIDO_WINDOWS.md
└── 📚 outros guias...
```

---

## ✅ Checklist Rapido

```
☐ Baixei TODOS os arquivos
☐ Coloquei TODOS na mesma pasta
☐ Executei: testar_instalacao.bat
☐ Vi os resultados (quais [OK] e [FALTA])
☐ Executei: instalar_windows.bat
☐ Aguardei instalacao completa
☐ Executei: testar_instalacao.bat novamente
☐ Agora tudo deu [OK]
☐ Executei: iniciar_servidor.bat
☐ Servidor iniciou (janela aberta)
☐ Abri: http://localhost:5000
☐ Interface funcionando! 🎉
```

---

## 🆘 Problemas?

### Python nao encontrado
```
Instale: https://www.python.org/downloads/
Marque: "Add Python to PATH"
```

### Arquivos nao encontrados
```
Verifique se TODOS estao na mesma pasta
Use: dir (para ver arquivos)
```

### Porta 5000 ocupada
```
Feche outros servidores
Ou mude a porta no server.py
```

### Dependencias nao instalam
```
Execute manualmente:
python -m pip install Pillow opencv-python flask flask-cors
```

---

## 💡 Comandos Uteis

### Ver arquivos na pasta:
```powershell
dir
```

### Testar Python:
```powershell
python --version
```

### Instalar manualmente:
```powershell
python -m pip install -r requirements.txt
python -m pip install flask flask-cors
```

### Iniciar servidor manualmente:
```powershell
python server.py
```

---

## 🎬 Pronto para Usar!

Depois de instalado:

1. **Sempre que quiser usar:**
   - Execute: `iniciar_servidor.bat`
   - Abra: `http://localhost:5000`

2. **Para criar videos:**
   - Importe seu JSON
   - Ou crie roteiro manualmente
   - Clique "Criar Video"

3. **Videos ficam em:**
   - `output/videos/`
   - `output/images/`
   - `output/frames/`

---

**Comece agora! Baixe todos os arquivos e execute testar_instalacao.bat! 🚀**
