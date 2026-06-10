# 🚀 Como Usar a Interface com Processamento Automático

## 📋 O que mudou?

Agora você pode **processar vídeos diretamente pela interface**! Não precisa mais usar linha de comando.

## 🎯 Fluxo Completo

### 1️⃣ Preparar Ambiente

```bash
# Instalar dependências (uma vez só)
pip install -r requirements.txt
pip install flask flask-cors
```

### 2️⃣ Iniciar o Servidor

```bash
# Abrir terminal na pasta do projeto
python server.py
```

Você verá:
```
🎬 VIDEO GENERATOR - Servidor Backend
================================================
📡 Servidor rodando em: http://localhost:5000
🌐 Abra seu navegador e acesse: http://localhost:5000
```

### 3️⃣ Usar a Interface

1. **Abra o navegador** em `http://localhost:5000`

2. **Importe seu JSON** ou crie manualmente:
   - Clique em "Importar JSON"
   - Selecione seu arquivo `roteiro.json`
   - ✅ Tudo será carregado automaticamente!

3. **Revise no Preview**:
   - Clique na aba "Preview"
   - Confira todas as cenas
   - Verifique se não há erros

4. **Criar Vídeo**:
   - Clique no botão verde **"Criar Vídeo"**
   - ⚠️ Certifique-se de estar logado em:
     - ChatGPT: https://chat.openai.com
     - Grok: https://x.ai/grok
   - Acompanhe o progresso em tempo real!

### 4️⃣ Acompanhar Processamento

A interface mostrará:
- ✅ Barra de progresso
- 📊 Estatísticas (cenas processadas, restantes)
- 📟 Console com logs em tempo real
- ⏱️ Status de cada etapa

### 5️⃣ Resultado

Quando finalizar:
- ✅ Mensagem de sucesso
- 📁 Arquivos em `./output/`
  - `/images` - Imagens geradas
  - `/videos` - Vídeos criados
  - `/frames` - Frames extraídos

---

## 🎨 Exemplo Completo

### Criar Roteiro na Interface

1. Clique em "Carregar Exemplo" (sidebar)
2. Ou crie manualmente:
   - Nome do projeto
   - Adicionar cenas
   - Preencher prompts

### Importar JSON Existente

```json
{
  "projeto": "Meu Vídeo",
  "descricao": "Descrição do projeto",
  "cenas": [
    {
      "numero": 1,
      "descricao": "Cena 1",
      "use_previous_frame": false,
      "dalle_prompt": "Beautiful landscape at sunset",
      "grok_movement": "Slow pan from left to right"
    }
  ]
}
```

1. Salve como `meu_roteiro.json`
2. Na interface, clique "Importar JSON"
3. Selecione o arquivo
4. ✅ Pronto! Clique em "Criar Vídeo"

---

## ⚙️ Arquitetura

```
┌─────────────┐         ┌──────────────┐         ┌────────────┐
│  Interface  │  HTTP   │    Flask     │  Python │   Video    │
│   (HTML)    │────────▶│   Server     │────────▶│ Generator  │
│             │◀────────│  (server.py) │◀────────│            │
└─────────────┘  JSON   └──────────────┘   Logs  └────────────┘
     │                                                   │
     │                                                   ├─▶ ChatGPT
     │                                                   └─▶ Grok
     └─ Poll status (1s)
```

---

## 🔧 Troubleshooting

### "Erro ao conectar com servidor"
**Solução**: Certifique-se de que `python server.py` está rodando

### "Imagem não gerada"
**Solução**: 
1. Verifique se está logado no ChatGPT
2. Abra chat.openai.com em outra aba

### "Vídeo não gerado"
**Solução**:
1. Verifique se está logado no Grok
2. Abra x.ai/grok em outra aba

### "CORS Error"
**Solução**: 
```bash
pip install flask-cors
```

---

## 💡 Dicas

### Velocidade
- Cada cena leva ~5-10 minutos
- DALL-E: ~15 segundos
- Grok: ~3-7 minutos por vídeo

### Monitoramento
- Não feche a aba do navegador
- Não feche o terminal do servidor
- Acompanhe os logs em tempo real

### Troubleshooting Rápido
- Se travar, recarregue a página
- Se der erro, verifique os logs no terminal
- Os arquivos já gerados ficam salvos

---

## 📦 Arquivos Necessários

```
projeto/
├── interface.html          # Interface web
├── server.py              # Servidor Flask
├── video_generator.py     # Processador principal
├── requirements.txt       # Dependências Python
└── roteiro.json           # Seu roteiro (opcional)
```

---

## 🎬 Começar Agora!

```bash
# 1. Instalar dependências
pip install -r requirements.txt
pip install flask flask-cors

# 2. Iniciar servidor
python server.py

# 3. Abrir navegador
# → http://localhost:5000

# 4. Importar JSON e clicar "Criar Vídeo"!
```

---

**Aproveite! 🎉**

Agora o processo é 100% visual e você pode acompanhar tudo em tempo real!
