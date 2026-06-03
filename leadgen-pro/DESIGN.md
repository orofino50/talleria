# LeadGen Pro — Design System

> Sistema visual do site one-pager LeadGen Pro. Versão: 2026-06-02.

## 1. North Star

**Terminal comercial.** A página deve evocar a precisão de uma mesa de operações B2B: tipo limpa, dados visíveis, sem decoração gratuita. O usuário chega, vê números, entende em 5 segundos o que o produto faz, e age. Não é uma landing page "fofa" — é a home de uma ferramenta que times de vendas usam para fechar mais.

## 2. Color

**Estratégia:** Committed dark com seções claras de contraste (não cream/beige genérico).

### Dark (dominante — hero, módulos-produto, pricing, CTA final)
| Token | Valor | Uso |
|---|---|---|
| `--ink-900` | `#0a0a0f` | Background principal |
| `--ink-800` | `#13131a` | Surface de cards |
| `--ink-700` | `#1c1c25` | Surface raised (hover) |
| `--ink-600` | `#2a2a35` | Border |
| `--ink-100` | `#f5f5f7` | Texto principal |
| `--ink-300` | `#a1a1aa` | Texto muted |
| `--ink-400` | `#71717a` | Texto terciário |
| `--accent` | `#6366f1` | Accent primário (indigo 500) |
| `--accent-2` | `#4f46e5` | Accent hover (indigo 600) |
| `--accent-glow` | `rgba(99,102,241,.35)` | Glow sob CTAs e hero |
| `--success` | `#10b981` | Status "live" / "ativo" |
| `--warning` | `#f59e0b` | Atrasos, alertas |
| `--gradient-hero` | `radial-gradient(ellipse 80% 60% at 50% 0%, #1e1b4b 0%, #0a0a0f 70%)` | Background do hero |

### Light (seções de conteúdo — módulos, cadences, makecash, analytics, FAQ)
| Token | Valor | Uso |
|---|---|---|
| `--bg-light` | `#f5f5f7` | Background |
| `--surface-light` | `#ffffff` | Cards |
| `--text-light` | `#1d1d1f` | Texto principal |
| `--text-muted-light` | `#6e6e73` | Texto muted |
| `--border-light` | `#e8e8ed` | Borders |
| `--accent-light` | `#4f46e5` | Accent em fundos claros |

**Contraste mínimo:** body 4.5:1, large text 3:1. Verificado com calculator.

## 3. Typography

**Família única:** Manrope (Google Fonts). Escolha consciente — Inter e DM Sans estão saturados no design SaaS. Manrope é geométrica com calor humanista, moderna sem ser fria.

Pesos usados: 400, 500, 600, 700, 800.

```css
--fs-display: clamp(56px, 9vw, 112px);  /* 900, -0.04em, 1.0 */
--fs-h2: clamp(40px, 5.5vw, 72px);       /* 800, -0.03em, 1.05 */
--fs-h3: clamp(24px, 2.5vw, 32px);       /* 700, -0.02em, 1.2 */
--fs-lead: 21px;                          /* 400, 1.5 */
--fs-body: 17px;                          /* 400, 1.6 */
--fs-data: 14px;                          /* 500, 0.02em, uppercase opcional */
--fs-code: 13px;                          /* 600, mono-ish, para labels de seção */
--fs-small: 14px;                         /* 400, 1.5 */
```

**Letter-spacing:** negativo em todos os títulos (compacção óptica). Zero tracking em body.

**Line length:** 65–75ch. Headlines com `text-wrap: balance`.

## 4. Spacing & rhythm

```css
--space-section: clamp(80px, 12vh, 160px);
--space-container: 1240px;
--space-gutter: clamp(20px, 4vw, 40px);
--space-card-padding: clamp(24px, 3vw, 40px);
```

Seções respiram como Apple. Containers com `max-width` e padding lateral. Cards com `border-radius: 20px`.

## 5. Components

### Buttons
- **Primary:** bg `--accent` solid, text white, weight 700, padding `14px 28px`, radius `12px`. Hover: `bg --accent-2` + glow.
- **Primary-large:** padding `18px 36px`, fs 17px. Para hero CTAs.
- **Ghost-dark:** border 1px `rgba(255,255,255,0.2)`, text white. Hover: border white.
- **Ghost-light:** border 1px `--text-light`, text `--text-light`. Hover: bg preto.
- **Link:** text accent com underline offset 4px. Hover: opacity 1.

### Cards
- Bg `--surface` (dark) ou `--surface-light` (light)
- Border 1px `--ink-600` (dark) ou `--border-light` (light)
- Radius 20px
- Padding `--space-card-padding`
- Hover: `translateY(-4px)` em 300ms ease-out

### Section labels (cadência)
Em vez de "eyebrow" genérico, uso labels de componente no estilo de código:
`<LeadGen />`, `<Engage />`, `<MakeCash />`, `<Pipeline />`, `<Analytics />`, `<Extensions />`.

```html
<span class="section-label">&lt;LeadGen /&gt;</span>
```

CSS: font mono-ish (Manrope 600), fs 13px, color accent, letter-spacing 0.02em.

Aparece apenas em seções que SÃO componentes de produto. Pricing, FAQ, hero, CTA final não têm label.

### Nav
- Fixed top, z-index 100
- Transparente no topo, `bg: rgba(10,10,15,0.7) + backdrop-filter: blur(20px)` ao scrollar
- Logo: "LeadGen" branco + "Pro" accent
- Links âncora, fs 14px, weight 500, opacity 0.7 → 1 hover
- CTA "Começar grátis" primary-small à direita
- Mobile: hamburger + drawer

### FAQ accordion
- Item: border-bottom 1px
- Question: weight 600, fs 17px, padding 20px 0
- "+" icon que rotaciona 45° ao abrir
- Answer: max-height 0 → 300px animado, 300ms ease

## 6. Motion

- Scroll reveal: opacity 0 + translateY 24px → 1 + 0, 600ms `cubic-bezier(0.16, 1, 0.3, 1)` (ease-out-quint)
- IntersectionObserver com `threshold: 0.1`
- Nav blur: trigger a 50px de scroll
- Hover lifts: 300ms ease-out
- CTA glow: animate 3s linear infinite
- `@media (prefers-reduced-motion: reduce)`: desativa reveals e anima glow, mantém apenas transições instant

## 7. Mockups (CSS-only)

Para mostrar o produto sem screenshots reais, construir inline em CSS:

- **Prospecção:** input + chips + grid de 4-6 cards de empresa
- **Cadences:** timeline horizontal com 6 nós conectados
- **Pipeline:** kanban 4 colunas, 2-3 cards cada
- **Analytics:** 3 mini-cards com sparklines
- **Extensions:** imagens geradas (extension-whatsapp.webp, extension-linkedin.webp)

Todos com border тонk, dados fictícios realistas (nomes genéricos, números plausíveis).

## 8. Banned

- ❌ Sombra em qualquer elemento
- ❌ Glassmorphism decorativo
- ❌ Texto gradiente
- ❌ Purple-to-blue genérico
- ❌ Eyebrow tracked-uppercase em toda seção
- ❌ Cards aninhados
- ❌ Border-left/right como accent
- ❌ Em dash (`—`) no body copy
- ❌ Buzzwords: "empoderar", "revolucionar", "transformar", "seamless", "world-class"
- ❌ Números 01/02/03 como scaffold

## 9. Performance budget

- HTML ≤ 30KB
- CSS ≤ 25KB
- JS ≤ 4KB
- Total página (com imagens) ≤ 500KB
- LCP < 2.5s em 3G mid-tier
- 60fps em scroll
