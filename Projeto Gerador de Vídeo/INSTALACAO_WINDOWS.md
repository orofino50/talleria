# 🪟 Guia de Instalação - Windows

## 🔧 Passo a Passo Completo

### 1️⃣ Verificar se Python está instalado

Abra o **PowerShell** ou **CMD** e digite:

```powershell
python --version
```

**Se aparecer algo como:** `Python 3.x.x` ✅ Python instalado!

**Se der erro:** ❌ Você precisa instalar o Python primeiro

---

## 📥 Instalar Python (se necessário)

### Opção A: Instalador Oficial

1. Acesse: https://www.python.org/downloads/
2. Clique em "Download Python 3.12" (ou versão mais recente)
3. **IMPORTANTE:** Na instalação, marque ✅ "Add Python to PATH"
4. Clique em "Install Now"
5. Aguarde a instalação
6. Reinicie o PowerShell

### Opção B: Microsoft Store

1. Abra a Microsoft Store
2. Pesquise "Python 3.12"
3. Clique em "Obter"
4. Aguarde a instalação

---

## 📦 Instalar Dependências

### Método 1: PowerShell (Recomendado)

```powershell
# Navegue até a pasta do projeto
cd C:\caminho\para\seu\projeto

# Instale as dependências
python -m pip install -r requirements.txt

# Instale as dependências do servidor
python -m pip install flask flask-cors
```

### Método 2: CMD (Prompt de Comando)

```cmd
cd C:\caminho\para\seu\projeto

python -m pip install -r requirements.txt

python -m pip install flask flask-cors
```

---

## 🚨 Problemas Comuns e Soluções

### ❌ Erro: "python não é reconhecido"

**Problema:** Python não está no PATH

**Soluções:**

**Opção 1 - Usar `py` ao invés de `python`:**
```powershell
py --version
py -m pip install -r requirements.txt
```

**Opção 2 - Adicionar Python ao PATH manualmente:**

1. Encontre onde o Python foi instalado (geralmente):
   - `C:\Users\SeuNome\AppData\Local\Programs\Python\Python312\`
   - `C:\Python312\`

2. Adicione ao PATH:
   - Abra: **Configurações do Sistema** → **Variáveis de Ambiente**
   - Em "Variáveis do Sistema", encontre "Path"
   - Clique em "Editar"
   - Adicione o caminho do Python
   - Adicione também: `C:\...\Python312\Scripts\`
   - Reinicie o PowerShell

**Opção 3 - Reinstalar Python:**
- Desinstale o Python atual
- Reinstale marcando ✅ "Add Python to PATH"

---

### ❌ Erro: "Execution Policy"

Se aparecer erro sobre política de execução no PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente novamente.

---

### ❌ Erro: "pip não é reconhecido"

**Solução 1 - Usar python -m pip:**
```powershell
python -m pip install -r requirements.txt
```

**Solução 2 - Instalar/atualizar pip:**
```powershell
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

---

### ❌ Erro: "Could not find a version that satisfies..."

**Problema:** Pacote não disponível para sua versão do Python

**Solução:**
```powershell
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Tentar instalar novamente
python -m pip install -r requirements.txt
```

---

### ❌ Erro: "Permission denied" ou "Access denied"

**Solução - Executar como Administrador:**

1. Feche o PowerShell
2. Clique com botão direito no PowerShell
3. Selecione "Executar como administrador"
4. Tente novamente

**OU use o flag --user:**
```powershell
python -m pip install --user -r requirements.txt
```

---

### ❌ Erro: "No module named 'pip'"

**Solução:**
```powershell
python -m ensurepip --default-pip
```

---

## ✅ Verificar Instalação

Após instalar, verifique se está tudo OK:

```powershell
# Verificar Python
python --version

# Verificar pip
python -m pip --version

# Verificar pacotes instalados
python -m pip list
```

Você deve ver na lista:
- selenium
- Pillow
- opencv-python
- requests
- flask
- flask-cors

---

## 🚀 Iniciar o Servidor

Depois de instalar tudo:

```powershell
# Navegue até a pasta do projeto
cd C:\caminho\para\seu\projeto

# Inicie o servidor
python server.py
```

Se tudo estiver OK, você verá:

```
🎬 VIDEO GENERATOR - Servidor Backend
================================================
📡 Servidor rodando em: http://localhost:5000
```

---

## 📝 Comandos Resumidos (Copiar e Colar)

### Se `python` funciona:

```powershell
cd C:\caminho\para\seu\projeto
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install flask flask-cors
python server.py
```

### Se só `py` funciona:

```powershell
cd C:\caminho\para\seu\projeto
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m pip install flask flask-cors
py server.py
```

---

## 🎯 Alternativa: Ambiente Virtual (Recomendado)

Para evitar conflitos, use um ambiente virtual:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\Activate

# Agora instale as dependências
pip install -r requirements.txt
pip install flask flask-cors

# Para desativar depois
deactivate
```

Com ambiente virtual ativado, você verá `(venv)` no início da linha do PowerShell.

---

## 📋 Checklist Final

- [ ] Python instalado (`python --version` funciona)
- [ ] pip instalado (`python -m pip --version` funciona)
- [ ] requirements.txt na pasta do projeto
- [ ] Dependências instaladas (`python -m pip install -r requirements.txt`)
- [ ] Flask instalado (`python -m pip install flask flask-cors`)
- [ ] Servidor inicia sem erros (`python server.py`)
- [ ] Navegador abre em http://localhost:5000

---

## 🆘 Ainda com Problemas?

### Opção 1: Use o instalador de tudo de uma vez

Crie um arquivo `instalar.bat` na pasta do projeto:

```batch
@echo off
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install flask flask-cors
echo.
echo Instalacao concluida!
echo.
pause
```

Clique duas vezes no arquivo `instalar.bat`

### Opção 2: Instale pacote por pacote

```powershell
python -m pip install selenium
python -m pip install Pillow
python -m pip install opencv-python
python -m pip install requests
python -m pip install flask
python -m pip install flask-cors
```

---

## 💡 Dicas Extras

### PowerShell vs CMD

- **PowerShell** (recomendado): Mais moderno, colorido
- **CMD**: Mais simples, mas menos recursos

Ambos funcionam! Use o que preferir.

### Navegação de Pastas

```powershell
# Ver onde você está
pwd

# Listar arquivos
ls

# Ir para pasta
cd nome_da_pasta

# Voltar uma pasta
cd ..

# Ir para disco diferente (exemplo: D:)
D:
cd D:\meus_projetos
```

---

**Pronto! Agora você está preparado para usar o Video Generator no Windows! 🎉**
