# ⏱️ RATE LIMITING - Processamento 24/7

## 🎯 Objetivo

Processar vídeos continuamente sem bater nos limites do DALL-E e Grok Imagine.

---

## 📊 Limites Conhecidos

### DALL-E (ChatGPT Plus)
- **Limite:** ~50 imagens por dia
- **Intervalo seguro:** 1 imagem a cada 30 minutos
- **Cálculo:** 24h = 48 imagens/dia

### Grok Imagine
- **Limite:** Desconhecido (conservadoramente estimado)
- **Intervalo seguro:** 1 vídeo a cada 3 minutos
- **Cálculo:** 20 vídeos/hora = 480 vídeos/dia

---

## ⚙️ Configuração Atual

**Padrão:** 3 minutos (180 segundos) entre cenas

```python
# No código:
wait_between_scenes = 180  # 3 minutos
```

### Com esta configuração:
- ✅ **20 cenas por hora**
- ✅ **480 cenas por dia**
- ✅ **Roda 24/7 sem problemas**
- ✅ **Nunca bate limite do DALL-E**
- ✅ **Nunca bate limite do Grok**

---

## 🔧 Como Ajustar

### Para processar mais rápido (ARRISCADO):
```python
wait_between_scenes = 60  # 1 minuto
# Resultado: 60 cenas/hora, mas pode bater limites!
```

### Para ser mais conservador (SUPER SEGURO):
```python
wait_between_scenes = 300  # 5 minutos
# Resultado: 12 cenas/hora = 288 cenas/dia
```

### Para máxima velocidade SEM DALL-E (usando previous_frame):
Se todas as cenas usarem `"use_previous_frame": true` (exceto a primeira):
```python
wait_between_scenes = 60  # 1 minuto é seguro
# Apenas 1 imagem DALL-E, resto é Grok apenas
```

---

## 📈 Exemplos de Produção

### Vídeo de 10 cenas (3 min de vídeo)
- **Tempo total:** ~40 minutos
  - 10 cenas × 3 min espera = 30 min
  - + ~10 min processamento real
- **Por dia:** ~36 vídeos

### Vídeo de 30 cenas (10 min de vídeo)
- **Tempo total:** ~2 horas
  - 30 cenas × 3 min espera = 90 min
  - + ~30 min processamento real
- **Por dia:** ~12 vídeos

### Vídeo de 100 cenas (30+ min de vídeo)
- **Tempo total:** ~6 horas
  - 100 cenas × 3 min espera = 5 horas
  - + ~1 hora processamento real
- **Por dia:** ~4 vídeos

---

## 💡 Dicas Pro

### 1. Use `use_previous_frame` para acelerar
```json
{
  "cenas": [
    {
      "dalle_prompt": "...",
      "use_previous_frame": false  // Primeira cena: gera imagem
    },
    {
      "dalle_prompt": "",
      "use_previous_frame": true   // Cenas seguintes: usa frame anterior
    }
  ]
}
```

### 2. Processe à noite
- Deixe rodando durante a noite
- Acorde com dezenas de vídeos prontos!

### 3. Monitore o terminal
O contador regressivo mostra exatamente quanto falta:
```
⏸️  AGUARDANDO 3 MINUTOS ANTES DA PRÓXIMA CENA...
   ⏱️  Tempo restante: 02:45
```

---

## 🚨 Se Bater Limite

Se você ver erros como:
- "Rate limit exceeded"
- "Too many requests"
- DALL-E não gera mais imagens

**Solução:**
1. Pare o processamento (Ctrl+C)
2. Aguarde 30-60 minutos
3. Aumente `wait_between_scenes` para 300 (5 min)
4. Continue processando

---

## 📊 Tabela de Referência

| Tempo entre cenas | Cenas/hora | Cenas/dia | Seguro? |
|-------------------|------------|-----------|---------|
| 1 min (60s)       | 60         | 1440      | ⚠️ Arriscado |
| 2 min (120s)      | 30         | 720       | ⚠️ Limite |
| 3 min (180s)      | 20         | 480       | ✅ Recomendado |
| 5 min (300s)      | 12         | 288       | ✅ Conservador |
| 10 min (600s)     | 6          | 144       | ✅ Super seguro |

---

## 🎬 Modo Produção 24/7

Para rodar ininterruptamente:

```bash
# 1. Inicie o servidor
python server.py

# 2. Configure seu roteiro com muitas cenas
# 3. Clique "Criar Vídeo"
# 4. Vá dormir / trabalhar / viver sua vida
# 5. Volte horas depois com tudo pronto!
```

**O sistema cuida de tudo:**
- ✅ Aguarda automaticamente entre cenas
- ✅ Mostra contador regressivo
- ✅ Respeita limites do DALL-E e Grok
- ✅ Pode rodar 24h sem supervisão

---

## 🔄 Reiniciando Após Erro

Se algo der errado no meio:

1. O navegador fica aberto (não fecha automaticamente)
2. Você vê exatamente onde parou
3. Pode continuar de onde parou manualmente
4. Ou ajustar configurações e recomeçar

---

**Com estas configurações, você pode processar centenas de vídeos por dia de forma totalmente automatizada!** 🚀
