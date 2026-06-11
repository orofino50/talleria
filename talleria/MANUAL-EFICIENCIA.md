# MANUAL DE EFICIÊNCIA — Como Pedir Coisas com Menos Tokens

## O Problema

Cada vez que eu leio um arquivo inteiro, gasto tokens. O CSS tem 4521 linhas (~25K tokens).
Se você pede "mude a cor do botão" e eu leio o CSS todo, gastei 25K tokens para uma mudança de 1 linha.

## A Solução

**Seja específico.** Quanto mais exato o pedido, menos eu preciso ler.

---

## Padrões de Pedido (do pior ao melhor)

### ❌ RUIM — Genérico (gasta ~30K tokens)
```
Mude o estilo da página do produto
```
**O que eu faço:** Ler producto.html (580 linhas) + CSS todo (4521 linhas) = ~30K tokens

### ⚠️ MÉDIO — Médio (gasta ~10K tokens)
```
Mude a cor do título do hero no produto
```
**O que eu faço:** grep "ap-hero__headline" → encontro linha 3860 → leio 30 linhas = ~3K tokens

### ✅ ÓTIMO — Específico (gasta ~2K tokens)
```
Em css/styles.css linha 3860, mude .ap-hero__headline color de white para #C5A55A
```
**O que eu faço:** Leio 5 linhas = ~500 tokens

---

## Fórmula do Pedido Eficiente

```
[ARQUIVO] [CLASSE/SEÇÃO] [O QUE MUDAR] [VALOR ATUAL] → [NOVO VALOR]
```

### Exemplos

| Pedido | Tokens gastos |
|--------|---------------|
| `"mude o hero"` | ~30,000 |
| `"mude o hero do produto"` | ~10,000 |
| `"mude .ap-hero__headline no CSS"` | ~3,000 |
| `"css linha 3860: color white → #C5A55A"` | ~500 |

---

## Atalhos de Pedido

### CSS — Mudanças de Cor
```
css: .ap-hero__headline color → #C5A55A
```

### CSS — Adicionar Propriedade
```
css: .ap-social-bar adicione gap: 32px
```

### CSS — Remover Regra
```
css: remova .ap-video--alt (linhas 4137-4147)
```

### HTML — Mudar Texto
```
html producto línea 88: "PaintPro." → "PaintPro™"
```

### HTML — Adicionar Elemento
```
html producto después de línea 177: agregar <div class="nuevo">...</div>
```

### JS — Mudar Comportamento
```
js: en countdown (línea 553), cambiar 23:59:59 → 12:00:00
```

### Deploy — Commit + Push
```
git commit "fix: corrigir cor do hero" && git push
```

---

## Referência Rápida de Classes

### Product Page (ap-* prefix)
| Classe | O que é | Linha CSS |
|--------|---------|-----------|
| `.ap-hero` | Hero section | 3820 |
| `.ap-hero__headline` | Título "PaintPro." | 3860 |
| `.ap-hero__price` | Bloco de preço | 3895 |
| `.ap-hero__price-current` | Preço atual €69,90 | 3903 |
| `.ap-hero__price-original` | Preço riscado | 3909 |
| `.ap-hero__price-badge` | Badge -32% | 3915 |
| `.ap-hero__hint` | "Envío gratis..." | 3883 |
| `.ap-carousel` | Carrossel de imagens | 3907 |
| `.ap-highlights` | 3 features | 3942 |
| `.ap-social-bar` | "+2.000 clientes" bar | 3996 |
| `.ap-video` | Seção de vídeo | 4034 |
| `.ap-video__headline` | "La pistola real..." | 4055 |
| `.ap-compare` | Tabela comparativa | 4130 |
| `.ap-cta-mid` | CTA do meio da página | 4177 |
| `.ap-specs` | Specs + Box contents | 4230 |
| `.ap-testimonials` | Depoimentos | 4298 |
| `.ap-trust` | "Compra con confianza" | 4372 |
| `.ap-cta` | CTA final | 4427 |
| `.ap-eyebrow` | Label de seção | 3808 |
| `.ap-section-headline` | Título de seção | 3801 |

### Homepage Classes
| Classe | O que é |
|--------|---------|
| `.brand-hero` | Hero da marca |
| `.stats-hero` | Barra de stats |
| `.manifesto` | Manifesto |
| `.history` | Nuestra historia |
| `.values` | 3 pilares |
| `.video-feature` | Vídeo destaque |
| `.products` | Grid de produtos |
| `.testimonials` | Depoimentos |
| `.brand-cta` | CTA da marca |

### Componentes Compartilhados
| Classe | O que é |
|--------|---------|
| `.btn` | Botão base |
| `.btn--accent` | Botão dourado |
| `.btn--trust` | Botão verde |
| `.product-nav` | Navegação |
| `.footer` | Rodapé |
| `.cta-sticky` | CTA fixo mobile |

---

## Fluxo de Trabalho Eficiente

### Para mudança visual (cor, tamanho, espaçamento):
```
1. Diga qual classe: "mude .ap-hero__headline"
2. Diga qual propriedade: "font-size"
3. Diga o valor novo: "de clamp(3rem,8vw,6rem) para 4rem"
```

### Para mudança de conteúdo (texto, imagem, link):
```
1. Diga a página: "producto.html"
2. Diga a linha ou seção: "línea 88" o "sección hero"
3. Diga o que mudar: "PaintPro." → "PaintPro™"
```

### Para adicionar nova seção:
```
1. Diga a página: "producto.html"
2. Diga onde: "después de la sección 4 (social proof)"
3. Diga o HTML: [cole o HTML]
4. Diga o CSS necessário: [descreva os estilos]
```

### Para bug fix:
```
1. Diga o sintoma: "o preço não aparece no mobile"
2. Diga onde achou: "producto.html línea 89-93"
3. Se souber a causa: "falta media query para .ap-hero__price"
```

---

## Comandos Úteis

```bash
# Encontrar classe no CSS
grep "ap-hero__headline" talleria/css/styles.css

# Encontrar classe no HTML
grep "ap-hero__headline" talleria/producto.html

# Ver linhas vizinhas
Read talleria/css/styles.css offset=3855 limit=20

# Sync + deploy
Copy-Item talleria\css\styles.css css\styles.css -Force
git add -A; git commit -m "fix: desc"; git push
```

---

## Economia de Tokens

| Ação | Tokens Antes | Tokens Agora | Economia |
|------|-------------|-------------|----------|
| Mudar cor de classe | 25,000 | 2,000 | 92% |
| Mudar texto no HTML | 15,000 | 1,500 | 90% |
| Adicionar seção | 40,000 | 5,000 | 87% |
| Bug fix simples | 30,000 | 3,000 | 90% |

**Regra de ouro:** Se você sabe qual arquivo e qual classe, me diga. Se não sabe, peça para eu grep primeiro (gasta ~500 tokens) antes de ler o arquivo inteiro.
