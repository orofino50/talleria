# 🎯 QUAL ARQUIVO EXECUTAR?

## 📂 Arquivos .BAT Disponíveis

### 1️⃣ `testar_instalacao.bat` ← COMECE POR AQUI!
**O que faz:** Verifica se tudo está funcionando
- ✅ Testa se Python está instalado
- ✅ Verifica arquivos do projeto
- ✅ Verifica dependências instaladas
- ✅ Mostra o que está faltando

**Quando usar:** Sempre antes de instalar ou quando algo não funciona

---

### 2️⃣ `instalar_windows.bat`
**O que faz:** Instala todas as dependências necessárias
- Atualiza pip
- Instala bibliotecas (selenium, opencv, etc)
- Instala Flask
- Não fecha automaticamente (você vê tudo)

**Quando usar:** Uma vez só, depois de baixar o projeto

---

### 3️⃣ `iniciar_servidor.bat`
**O que faz:** Inicia o servidor Flask
- Abre o servidor em http://localhost:5000
- Mantém janela aberta
- Não fecha sozinho

**Quando usar:** Toda vez que quiser usar o Video Generator

---

## 🚀 Ordem de Execução

```
PRIMEIRA VEZ:
1. testar_instalacao.bat    (ver o que falta)
2. instalar_windows.bat      (instalar tudo)
3. testar_instalacao.bat    (confirmar que está OK)
4. iniciar_servidor.bat      (usar o programa)

PRÓXIMAS VEZES:
1. iniciar_servidor.bat      (só isso!)
```

---

## 💡 Como Executar

### Método 1: Clique Duplo (Mais Fácil)
1. Localize o arquivo `.bat` no Windows Explorer
2. Clique duas vezes nele
3. Aguarde a janela abrir
4. Leia as mensagens

### Método 2: PowerShell
1. Abra PowerShell na pasta do projeto
2. Digite: `.\nome_do_arquivo.bat`
3. Pressione Enter

---

## 🐛 Se o Arquivo Abre e Fecha Rapidamente

**Significa que houve um erro!**

Os novos scripts BAT NÃO fecham automaticamente. Eles esperam você pressionar uma tecla.

**Se ainda assim fecha rápido:**

1. **Abra PowerShell na pasta do projeto**
2. **Execute manualmente:**
   ```powershell
   .\testar_instalacao.bat
   ```
3. **Você verá o erro completo**

---

## 📋 Checklist de Uso

```
☐ Baixei todos os arquivos do projeto
☐ Coloquei todos na mesma pasta
☐ Executei: testar_instalacao.bat
☐ Vi quais dependências faltam
☐ Executei: instalar_windows.bat
☐ Instalação concluiu sem erros
☐ Executei: testar_instalacao.bat novamente
☐ Tudo deu ✅ OK
☐ Executei: iniciar_servidor.bat
☐ Servidor iniciou (janela ficou aberta)
☐ Abri navegador em: http://localhost:5000
☐ Interface funcionando! 🎉
```

---

## 🆘 Troubleshooting Rápido

### ❌ "Python não encontrado"
```powershell
# Teste no PowerShell:
python --version

# Se não funcionar, tente:
py --version

# Se nenhum funcionar:
# Instale Python: https://www.python.org/downloads/
```

### ❌ "Arquivo não encontrado"
- Você está na pasta certa?
- Todos os arquivos estão juntos?
- Execute: `dir` para ver arquivos

### ❌ "Permissão negada"
- Clique com botão direito no PowerShell
- "Executar como administrador"

### ❌ Scripts não executam
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎬 Exemplo Visual

```
Sua Pasta do Projeto/
│
├── 📄 testar_instalacao.bat      ← 1. Execute primeiro
├── 📄 instalar_windows.bat       ← 2. Execute depois
├── 📄 iniciar_servidor.bat       ← 3. Execute para usar
│
├── 🐍 video_generator.py
├── 🐍 server.py
├── 🌐 interface.html
├── 📋 requirements.txt
└── 📚 outros arquivos...

```

---

## 📞 Comandos Úteis

```powershell
# Ver onde você está
pwd

# Listar arquivos
dir

# Navegar para pasta
cd C:\caminho\da\pasta

# Executar BAT
.\nome_do_arquivo.bat

# Ver logs de erro (se houver)
type error.log
```

---

## ✅ Tudo Funcionando?

Quando tudo estiver OK, você verá:

```
✅ Python encontrado
✅ Arquivos encontrados
✅ Dependências instaladas
✅ Flask instalado
✅ Porta 5000 disponível

STATUS: ✅ TUDO OK!
```

Aí é só executar `iniciar_servidor.bat` e usar! 🎉

---

**Dica:** Mantenha a janela do servidor aberta enquanto usar o programa!
