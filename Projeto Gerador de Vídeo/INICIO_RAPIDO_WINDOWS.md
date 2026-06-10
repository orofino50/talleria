# 🚀 INÍCIO RÁPIDO - WINDOWS

## 📦 Opção 1: Instalação Automática (MAIS FÁCIL!)

### Passo 1: Instalar Tudo
1. Clique duas vezes em: **`instalar_windows.bat`**
2. Aguarde a instalação (pode levar alguns minutos)
3. Quando aparecer "Instalação Concluída", pressione qualquer tecla

### Passo 2: Iniciar Servidor
1. Clique duas vezes em: **`iniciar_servidor.bat`**
2. Aguarde aparecer "Servidor rodando em: http://localhost:5000"
3. **NÃO FECHE** esta janela!

### Passo 3: Usar a Interface
1. Abra seu navegador (Chrome, Edge, Firefox)
2. Digite na barra de endereço: **`http://localhost:5000`**
3. Pronto! Use a interface! 🎉

---

## ⌨️ Opção 2: Instalação Manual (PowerShell)

### Passo 1: Abrir PowerShell
1. Pressione `Windows + X`
2. Escolha "Windows PowerShell" ou "Terminal"

### Passo 2: Navegar até a Pasta
```powershell
cd C:\caminho\para\seu\projeto
```
*Substitua pelo caminho real onde estão os arquivos*

**Dica:** Arraste a pasta para o PowerShell para obter o caminho automaticamente!

### Passo 3: Instalar
```powershell
python -m pip install -r requirements.txt
python -m pip install flask flask-cors
```

### Passo 4: Iniciar
```powershell
python server.py
```

---

## 🆘 Problemas Comuns

### ❌ "python não é reconhecido"

**Solução Rápida:**
```powershell
py -m pip install -r requirements.txt
py -m pip install flask flask-cors
py server.py
```

**Solução Definitiva:**
1. Instale Python: https://www.python.org/downloads/
2. ✅ Marque "Add Python to PATH"
3. Reinicie o PowerShell

---

### ❌ "Execution Policy"

No PowerShell, digite:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### ❌ "pip não encontrado"

```powershell
python -m ensurepip --default-pip
python -m pip install --upgrade pip
```

---

### ❌ "Acesso negado"

Execute o PowerShell **como Administrador**:
1. Pesquise "PowerShell" no menu iniciar
2. Clique com botão direito
3. "Executar como administrador"

---

## 📱 Como Usar Depois de Instalado

### Sempre que quiser usar:

**Opção A - Scripts BAT:**
1. Clique em: `iniciar_servidor.bat`
2. Abra navegador em: `http://localhost:5000`

**Opção B - PowerShell:**
1. Abra PowerShell na pasta do projeto
2. Execute: `python server.py`
3. Abra navegador em: `http://localhost:5000`

---

## 🎬 Fluxo de Uso

```
1. Instalar (uma vez só)
   ↓
2. Iniciar servidor (sempre que usar)
   ↓
3. Abrir http://localhost:5000
   ↓
4. Importar JSON ou criar roteiro
   ↓
5. Clicar "Criar Vídeo"
   ↓
6. Aguardar processamento
   ↓
7. Vídeos prontos em ./output/
```

---

## 📋 Checklist de Instalação

```
☐ Python instalado
☐ Arquivos do projeto baixados
☐ Cliquei em instalar_windows.bat
☐ Instalação concluída sem erros
☐ Cliquei em iniciar_servidor.bat
☐ Servidor rodando (janela aberta)
☐ Navegador abriu em localhost:5000
☐ Interface funcionando
☐ Pronto para usar! 🎉
```

---

## 💡 Dicas Importantes

### Durante o Uso:
- ✅ Mantenha a janela do servidor aberta
- ✅ Esteja logado no ChatGPT e Grok
- ✅ Não feche o navegador durante processamento

### Localização dos Arquivos:
- Vídeos gerados: `output/videos/`
- Imagens geradas: `output/images/`
- Frames extraídos: `output/frames/`

### Para Parar o Servidor:
- Pressione `Ctrl + C` na janela do servidor
- Ou simplesmente feche a janela

---

## 🎯 Comandos Úteis

### Ver versão do Python:
```powershell
python --version
```

### Ver pacotes instalados:
```powershell
python -m pip list
```

### Atualizar um pacote:
```powershell
python -m pip install --upgrade nome_do_pacote
```

### Desinstalar tudo (para recomeçar):
```powershell
python -m pip uninstall -y -r requirements.txt
python -m pip uninstall -y flask flask-cors
```

---

## 📞 Precisa de Ajuda?

Leia o arquivo: **`INSTALACAO_WINDOWS.md`** para guia completo!

---

**Comece agora! É só clicar em `instalar_windows.bat`! 🚀**
