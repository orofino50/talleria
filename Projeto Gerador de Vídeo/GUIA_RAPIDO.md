# 🚀 Guia Rápido - Video Generator

## Instalação em 3 Passos

### 1️⃣ Preparar Ambiente
```bash
# Clone ou baixe os arquivos
cd video-generator

# Execute o setup
python setup.py
```

### 2️⃣ Login nos Serviços
Certifique-se de estar logado em:
- ✅ **ChatGPT**: https://chat.openai.com
- ✅ **Grok/X.AI**: https://x.ai/grok

### 3️⃣ Executar
```bash
# Validar roteiro
python validate_roteiro.py roteiro_exemplo.json

# Gerar vídeos
python video_generator.py roteiro_exemplo.json
```

---

## 📝 Criar Seu Roteiro

### Modelo Básico
```json
{
  "projeto": "Meu Projeto",
  "cenas": [
    {
      "use_previous_frame": false,
      "dalle_prompt": "Descrição da imagem para DALL-E",
      "grok_movement": "Descrição do movimento"
    }
  ]
}
```

### Campos Importantes

**use_previous_frame**
- `false` = Gera nova imagem com DALL-E
- `true` = Usa último frame da cena anterior

**dalle_prompt** (obrigatório se use_previous_frame = false)
- Descrição detalhada da imagem
- Incluir: estilo, iluminação, qualidade
- Exemplo: "Photorealistic sunset over ocean, golden hour, 4K"

**grok_movement** (sempre obrigatório)
- Descrição do movimento/animação
- Incluir: tipo, velocidade, direção
- Exemplo: "Slow pan from left to right, smooth transition"

---

## 🎯 Comandos Úteis

### Validar Roteiro
```bash
python validate_roteiro.py meu_roteiro.json
```

### Gerar Vídeos
```bash
# Diretório padrão (./output)
python video_generator.py meu_roteiro.json

# Diretório customizado
python video_generator.py meu_roteiro.json -o ./meu_projeto
```

### Ver Ajuda
```bash
python video_generator.py --help
```

---

## 📁 Onde Encontrar os Arquivos

Após processar, os arquivos estarão em:

```
output/
├── images/          # Imagens geradas pelo DALL-E
├── videos/          # Vídeos gerados pelo Grok
├── frames/          # Últimos frames extraídos
└── summary.txt      # Resumo de tudo gerado
```

---

## 💡 Dicas Rápidas

### Para Melhores Resultados

**Prompts DALL-E:**
- Seja específico sobre o estilo
- Inclua qualidade: "4K", "high detail"
- Descreva iluminação: "golden hour", "soft light"

**Prompts Grok:**
- Descreva tipo de movimento: "pan", "zoom", "orbit"
- Adicione velocidade: "slow", "smooth", "fast"
- Especifique direção: "left to right", "forward"

### Continuidade Entre Cenas

```json
// Cena 1: Gera imagem nova
{
  "use_previous_frame": false,
  "dalle_prompt": "Forest scene...",
  "grok_movement": "Move forward..."
}

// Cena 2: Continua de onde parou
{
  "use_previous_frame": true,
  "dalle_prompt": "",
  "grok_movement": "Continue moving..."
}
```

---

## ⚠️ Problemas Comuns

### "Imagem não encontrada"
→ Verifique se está logado no ChatGPT

### "Vídeo não gerado"
→ Verifique se está logado no Grok/X.AI

### "JSON inválido"
→ Execute: `python validate_roteiro.py seu_roteiro.json`

### "Chrome não encontrado"
→ Instale Google Chrome: https://www.google.com/chrome/

---

## 📊 Exemplo de Sessão

```bash
$ python setup.py
✅ Python 3.10
✅ Chrome instalado
✅ Dependências instaladas
🎉 Ambiente configurado!

$ python validate_roteiro.py roteiro.json
✅ Roteiro VÁLIDO e sem problemas!

$ python video_generator.py roteiro.json
🎬 VIDEO GENERATOR - Iniciando
📖 Carregando roteiro: roteiro.json
✓ Roteiro validado: 5 cenas

PROCESSANDO CENA 1/5
🎨 Gerando imagem...
✓ Imagem salva
🎬 Gerando vídeo...
✓ Vídeo salvo
✓ Cena 1 concluída!

[... processa todas as cenas ...]

✅ PROCESSAMENTO CONCLUÍDO!
⏱️ Tempo total: 0:15:32
📁 Arquivos salvos em: output
```

---

## 🆘 Precisa de Ajuda?

Consulte o **README.md** completo para:
- Documentação detalhada
- Troubleshooting avançado
- Exemplos de prompts
- Configurações personalizadas

---

**Feito com ❤️ para automatizar criação de vídeos**
