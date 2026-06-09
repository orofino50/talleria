# Design Context

## Design System

- **North Star:** Luz de Estúdio
- **Register:** Brand (landing page de produto físico — Talleria multi-tool)
- **Personalidade:** Profissional, premium, confiável
- **Fonte:** Inter (monofamília, pesos 400/600/700/900)
- **Paleta v2:** Light-first (#f5f5f7 bg, #ffffff cards, #1d1d1f text) — Apple-inspired
- **Accent:** Coral Elétrico (#e94560) — uso ≤10% da tela
- **Trust:** Verde Garantia (#2ecc71) — CTAs finais e badges
- **Elevação:** Sem sombras (profundidade tonal + thin borders #e8e8ed + hover lift)
- **Bordas:** #e8e8ed, radius 16px
- **Interações:** Scroll reveal (IntersectionObserver), navbar transparent→white blur, FAQ accordion, hover lift
- **Arquivos:** `PRODUCT.md` (estratégia), `DESIGN.md` (sistema visual), `.impeccable/design.json` (tokens)

## Progress

- v2 completa: 5 páginas (index, producto, sobre, faq, contacto) com CSS de 20KB + JS 2.7KB
- Imagens reais do produto via Shopify CDN, baixadas para `images/`
- Audit score: 19/20 | Critique UX: 33/40
- Publicado em: https://orofino50.github.io/talleria/
- Repo: https://github.com/orofino50/talleria

## Comandos disponíveis

- `/impeccable audit <alvo>` — Verificação técnica (a11y, perf, responsivo)
- `/impeccable critique <alvo>` — Revisão UX com scoring
- `/impeccable polish <alvo>` — Passada final de qualidade
- `/impeccable distill <alvo>` — Simplificar e remover complexidade
- `/impeccable live` — Iteração visual no navegador

## Imagens locais (`images/`)

- `hastahoy.webp` — Herói principal do produto (236KB)
- `thc_3.webp` — Detalhe do controle de fluxo (593KB)
- `accesorios.webp` — Acessórios incluídos (186KB)
- `superficies.webp` — Tipos de superfície compatíveis (196KB)
- `testimonial-augusto.webp` — Depoimento (41KB)
- `testimonial-luis.webp` — Depoimento (36KB)
