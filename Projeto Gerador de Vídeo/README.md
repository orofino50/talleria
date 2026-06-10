# 🎬 Video Generator

Aplicação automatizada para geração de vídeos a partir de roteiros JSON, integrando DALL-E (ChatGPT) e Grok Imagine.

## 📋 Fluxo de Trabalho

```
INÍCIO
│
├─ Ler roteiro.json
├─ Validar estrutura
│
└─ Para cada CENA:
    │
    ├─ Se use_previous_frame = false:
    │   ├─ Abrir ChatGPT
    │   ├─ Enviar dalle_prompt
    │   ├─ Baixar imagem
    │   └─ Validar imagem (menu completo)
    │
    ├─ Se use_previous_frame = true:
    │   └─ Usar último frame da cena anterior
    │
    ├─ Abrir Grok Imagine
    ├─ Upload da imagem
    ├─ Enviar grok_movement
    ├─ Aguardar geração
    ├─ Baixar vídeo
    ├─ Validar vídeo (menu completo)
    ├─ Extrair último frame
    │
    └─ Salvar tudo organizado
│
FIM
```

## 🚀 Instalação

### 1. Requisitos do Sistema

- Python 3.8+
- Google Chrome instalado
- ChromeDriver (instalado automaticamente via webdriver-manager)

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar Credenciais

Você precisará estar logado em:
- **ChatGPT** (https://chat.openai.com) - para DALL-E
- **Grok/X.AI** (https://x.ai/grok) - para Grok Imagine

A aplicação abrirá o navegador onde você deverá estar logado nestes serviços.

## 📝 Estrutura do Roteiro JSON

```json
{
  "projeto": "Nome do Projeto",
  "descricao": "Descrição do projeto",
  "cenas": [
    {
      "numero": 1,
      "descricao": "Descrição da cena",
      "use_previous_frame": false,
      "dalle_prompt": "Prompt detalhado para DALL-E gerar a imagem",
      "grok_movement": "Descrição do movimento/animação para o Grok"
    },
    {
      "numero": 2,
      "descricao": "Segunda cena",
      "use_previous_frame": true,
      "dalle_prompt": "",
      "grok_movement": "Movimento para esta cena"
    }
  ]
}
```

### Campos Obrigatórios

- **use_previous_frame**: `true` ou `false`
  - `false`: Gera nova imagem com DALL-E usando `dalle_prompt`
  - `true`: Usa o último frame da cena anterior

- **dalle_prompt**: Texto para gerar imagem (obrigatório se `use_previous_frame = false`)

- **grok_movement**: Descrição do movimento/animação para o vídeo

## 🎯 Uso

### Comando Básico

```bash
python video_generator.py roteiro.json
```

### Com Diretório de Saída Customizado

```bash
python video_generator.py roteiro.json -o ./meu_projeto
```

### Exemplo Completo

```bash
# Usar o roteiro de exemplo incluído
python video_generator.py roteiro_exemplo.json
```

## 📁 Estrutura de Saída

Após a execução, os arquivos serão organizados em:

```
output/
├── images/
│   ├── scene_001.png
│   ├── scene_002.png
│   └── scene_003.png
├── videos/
│   ├── scene_001.mp4
│   ├── scene_002.mp4
│   └── scene_003.mp4
├── frames/
│   ├── scene_001_last_frame.png
│   ├── scene_002_last_frame.png
│   └── scene_003_last_frame.png
└── summary.txt
```

## ✅ Validações Automáticas

### Validação de Imagens
- ✓ Dimensões mínimas (100x100px)
- ✓ Integridade do arquivo
- ✓ Formato válido

### Validação de Vídeos
- ✓ Vídeo pode ser aberto
- ✓ Contém frames suficientes (mínimo 10)
- ✓ FPS e duração válidos
- ✓ Integridade do arquivo

## 🔧 Configurações Avançadas

### Timeouts

Você pode ajustar os tempos de espera no código:

```python
# Em video_generator.py
time.sleep(15)  # Espera geração DALL-E
time.sleep(60)  # Espera geração Grok
```

### Downloads

Os downloads são salvos automaticamente. Certifique-se de que o Chrome tem permissões para baixar arquivos.

## 🎨 Dicas para Prompts

### DALL-E (Imagens)
- Seja específico sobre estilo: "photorealistic", "oil painting", "3D render"
- Inclua detalhes de iluminação: "golden hour", "studio lighting"
- Defina qualidade: "4K", "high detail", "cinematic"
- Especifique composição: "wide angle", "close-up", "bird's eye view"

### Grok Imagine (Movimento)
- Descreva o tipo de movimento: "pan", "zoom", "dolly", "orbit"
- Indique velocidade: "slow", "smooth", "fast"
- Especifique direção: "left to right", "forward", "upward"
- Adicione detalhes: "with depth of field", "following the subject"

## ⚠️ Troubleshooting

### Problema: Navegador não abre
**Solução**: Instale/atualize o Chrome e execute:
```bash
pip install --upgrade selenium webdriver-manager
```

### Problema: Imagens não são encontradas
**Solução**: Verifique se está logado no ChatGPT e se a sessão está ativa

### Problema: Vídeos não são gerados
**Solução**: Verifique se está logado no Grok/X.AI e se tem acesso ao Grok Imagine

### Problema: Downloads não funcionam
**Solução**: Verifique permissões de download no Chrome e desative bloqueadores de pop-up

## 📊 Exemplo de Saída

```
==============================================================
🎬 VIDEO GENERATOR - Iniciando processamento
==============================================================

📖 Carregando roteiro: roteiro.json
✓ Roteiro validado: 5 cenas
✓ Navegador configurado

==============================================================
PROCESSANDO CENA 1/5
==============================================================

🎨 Gerando imagem para cena 1...
Prompt: A breathtaking mountain landscape at dawn...
⏳ Aguardando geração da imagem...
✓ Imagem validada: 1024x1024px
✓ Imagem salva: output/images/scene_001.png

🎬 Gerando vídeo para cena 1...
Movimento: Slow camera pan from left to right...
📤 Fazendo upload da imagem...
⏳ Aguardando geração do vídeo...
✓ Vídeo validado: 5.00s, 150 frames, 30 FPS
✓ Vídeo salvo: output/videos/scene_001.mp4

🖼️ Extraindo último frame da cena 1...
✓ Frame extraído: output/frames/scene_001_last_frame.png
✓ Cena 1 concluída!

==============================================================
✅ PROCESSAMENTO CONCLUÍDO!
⏱️ Tempo total: 0:15:32
📁 Arquivos salvos em: output
==============================================================
```

## 🤝 Contribuindo

Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é de código aberto para uso pessoal e educacional.

## ⚡ Próximas Melhorias

- [ ] Interface gráfica (GUI)
- [ ] Suporte a múltiplos provedores de IA
- [ ] Edição de vídeo (concatenação automática)
- [ ] Adição de áudio/narração
- [ ] Preview em tempo real
- [ ] Retry automático em caso de falhas
- [ ] Modo batch para múltiplos roteiros
