# LeadGen Pro — Landing Page Design

**Data:** 2026-06-02
**Status:** Aprovado (aguardando sign-off final)
**Tipo:** Site de marketing one-pager estilo Apple.com

---

## 1. Objetivo

Criar um site de marketing one-pager para o **LeadGen Pro** (SaaS B2B de inteligência comercial e automação de prospecção) no estilo visual e narrativo de apple.com. O site deve comunicar a proposta de valor, demonstrar as funcionalidades principais, apresentar preços e converter visitantes em leads/cadastros.

**Público-alvo primário:** Gestores comerciais e donos de empresas B2B que vendem para indústrias, distribuidoras e empresas de médio/grande porte no Brasil.

**Tom de voz:** Direto, confiante, focado em resultados. Números concretos. Sem jargão excessivo.

---

## 2. Arquitetura

### 2.1 Localização
```
C:\Users\Lucas Pietro\Desktop\Projeto\leadgen-pro\
```

Convive com o site AltaPro existente no mesmo repo. Cada site é independente.

### 2.2 Estrutura de arquivos

```
leadgen-pro/
├── index.html              # ~25KB, 10 seções semânticas
├── css/
│   └── styles.css          # ~22KB, tokens + componentes + seções
├── js/
│   └── main.js             # ~3KB, scroll reveal + nav + FAQ
├── images/
│   ├── hero-dashboard.webp     # Gerada via Z-Image Turbo (1920x1080)
│   ├── extension-whatsapp.webp # Mockup da sidebar WhatsApp
│   ├── extension-linkedin.webp # Mockup da sidebar LinkedIn
│   └── favicon.svg
├── DESIGN.md               # Tokens e decisões visuais
└── PRODUCT.md              # Resumo estratégico do produto
```

### 2.3 Stack
- HTML semântico + ARIA
- CSS com custom properties + BEM-lite
- JS vanilla (IntersectionObserver, sticky nav, accordion)
- Inter via Google Fonts com preconnect
- Sem build step
- Sem framework

---

## 3. Estrutura da página (10 seções com âncoras)

| # | Âncora | Tema | Conteúdo principal |
|---|---|---|---|
| 1 | `#hero` | dark | Proposta de valor + 2 CTAs + dashboard hero |
| 2 | `#modules` | light | LeadGen + Engage lado a lado |
| 3 | `#prospecção` | dark | Busca por setor, ICP, bulk import |
| 4 | `#cadences` | light | Cadências multicanal (timeline) |
| 5 | `#extensions` | dark | Extensões Chrome (WhatsApp + LinkedIn) |
| 6 | `#makecash` | light | MakeCash IA (3 features) |
| 7 | `#pipeline` | dark | CRM visual (kanban) |
| 8 | `#analytics` | light | Dashboards |
| 9 | `#pricing` | dark | 3 tiers de preço |
| 10 | `#faq` | light→dark | 6 FAQs + CTA final |

Navegação âncora fixa no topo (transparente → blur ao scrollar).

---

## 4. Sistema visual

### 4.1 Paleta

| Token | Valor (dark) | Valor (light) |
|---|---|---|
| `--bg` | `#0a0a0f` | `#f5f5f7` |
| `--surface` | `#13131a` | `#ffffff` |
| `--surface-2` | `#1c1c25` | `#fafafc` |
| `--text` | `#f5f5f7` | `#1d1d1f` |
| `--text-muted` | `#a1a1aa` | `#6e6e73` |
| `--border` | `#26262f` | `#e8e8ed` |
| `--accent` | `#6366f1` (indigo 500) | `#4f46e5` (indigo 600) |
| `--accent-glow` | `rgba(99,102,241,.35)` | — |
| `--success` | `#10b981` (emerald) | `#059669` |
| `--gradient-hero` | `radial-gradient(ellipse at top, #1e1b4b 0%, #0a0a0f 60%)` | — |

### 4.2 Tipografia (Inter, monofamília)

| Token | Valor |
|---|---|
| `--fs-display` | `clamp(56px, 9vw, 112px)` / 900 / -0.04em / line-height 1.02 |
| `--fs-h2` | `clamp(40px, 5.5vw, 72px)` / 800 / -0.03em |
| `--fs-h3` | `clamp(24px, 2.5vw, 32px)` / 700 |
| `--fs-lead` | 21px / 400 / 1.4 |
| `--fs-body` | 17px / 400 / 1.55 |
| `--fs-eyebrow` | 13px / 700 / 0.12em uppercase |

### 4.3 Componentes base
- **Buttons:** `.btn-primary` (indigo gradient → emerald on hover), `.btn-ghost`, `.btn-link` (com seta →)
- **Cards:** `border-radius: 20px`, thin border + hover lift 4px
- **Section spacing:** `padding: clamp(80px, 12vh, 160px) 0`
- **Container:** `max-width: 1240px`
- **Borders:** 1px, sem sombras (profundidade tonal)

### 4.4 Efeitos
- Nav transparente → `backdrop-filter: blur(20px)` + bg escuro translúcido ao scrollar
- Scroll reveal (fade + translateY 24px → 0, 600ms cubic-bezier)
- Hover lift em cards (translateY(-4px))
- CTA com gradient shift animado (indigo→emerald em 3s loop)
- Imagens com `mask-image` radial fade

---

## 5. Conteúdo das seções

### 5.1 Hero (dark)
- Eyebrow: "INTELIGÊNCIA COMERCIAL B2B"
- H1: "Encontre. Engaje. Converta."
- Sub: "A plataforma que une prospecção, CRM e cadências multicanal em um só lugar. Feita para times de vendas B2B no Brasil."
- CTAs: `Começar grátis` · `▶ Ver demonstração`
- Visual: hero-dashboard.webp centralizado, mask radial, glow indigo

### 5.2 Módulos (light)
- H2: "Dois módulos. Um sistema completo."
- Card LeadGen: "Encontre as empresas certas e identifique os decisores que vão comprar de você."
- Card Engage: "Gerencie pipeline, execute cadências e feche mais negócios com menos esforço."
- Conexão SVG entre os cards

### 5.3 Prospecção (dark)
- H2: "Empresas certas, no momento certo."
- Sub: "Busque até 200 empresas por pesquisa, qualificadas por IA, com decisores já mapeados."
- Visual: mockup CSS de busca
- Bullets: até 200 empresas/busca · filtro B2B automático · decisores via LinkedIn · ICP com IA

### 5.4 Cadências (light)
- H2: "A abordagem certa, no canal certo, no tempo certo."
- Visual: timeline horizontal com 6 passos
- Bullets: multicanal · templates com variáveis · IA gera sequência · Painel Hoje

### 5.5 Extensões Chrome (dark)
- H2: "Seu CRM, dentro do WhatsApp e do LinkedIn."
- Split 50/50: WhatsApp + LinkedIn sidebars
- Bullets: detecção automática · tarefas sem sair da aba · mensagens com IA · API revogável

### 5.6 MakeCash IA (light)
- H2: "Sua copiloto de vendas."
- 3 cards: Análise de Contato · Geração de Mensagens · Insights do Time
- Badge "✨ MakeCash IA" pulsando

### 5.7 Pipeline (dark)
- H2: "Do lead ao fechamento, em um piscar de olhos."
- Visual: kanban 4 colunas
- Bullets: múltiplos pipelines · estágios personalizáveis · campos por estágio · motivo de perda

### 5.8 Analytics (light)
- H2: "Decisões que vêm dos números."
- Visual: 3 mini-cards
- Bullets: dashboard gerente · relatório SDR · análise pipeline · insights IA

### 5.9 Preços (dark)
- H2: "Comece grátis. Cresça sem limites."
- Starter R$ 0 (1 user, 100 leads/mês)
- Pro R$ 197/mês (MAIS POPULAR — badge emerald, 5 users, leads ilimitados)
- Enterprise sob consulta (multi-org, SSO, SLA)

### 5.10 FAQ + CTA Final (light → dark)
- 6 FAQs: cartão · segmento · extensões · segurança · garantia · cancelamento
- CTA dark final: "Pronto para encontrar seus próximos 100 clientes?"

---

## 6. Critérios de aceite

| # | Critério | Métrica |
|---|---|---|
| 1 | Performance | Lighthouse ≥ 90 (mobile + desktop) |
| 2 | Acessibilidade | WCAG AA completo |
| 3 | Responsivo | 360px, 768px, 1024px, 1440px |
| 4 | SEO | title, meta, OG, JSON-LD SoftwareApplication, sitemap, robots |
| 5 | Tamanho | HTML ≤30KB, CSS ≤25KB, JS ≤4KB, página ≤500KB |
| 6 | Compatibilidade | Chrome/Edge/Firefox/Safari últimos 2, iOS Safari 15+ |
| 7 | Interações | Scroll reveal, nav blur, FAQ accordion, hovers |
| 8 | Fidelidade Apple | Tipografia massiva, respiração, dark/light alternados |

---

## 7. Entregáveis

1. Site funcional em `/leadgen-pro/`
2. 3 hero images geradas (Z-Image Turbo)
3. Mockups CSS inline (kanban, timeline, mini-dashboards)
4. `DESIGN.md` + `PRODUCT.md`
5. Servidor local: `python -m http.server` na pasta
6. Auditoria final (audit + critique + polish)

---

## 8. Riscos

- **Sem screenshots reais do SaaS** → mockups CSS estilizados (Apple também usa mockups)
- **Imagens geradas podem ter artefatos** → gerar 3-4 candidatas por conceito, escolher a melhor
- **Texto longo do product doc** → destilado para claims de impacto

---

## 9. Fora de escopo (v1)

- Backend funcional / login real
- Formulário de contato (placeholder mailto:)
- Blog / docs
- Gateway de pagamento
- i18n (PT-BR only)
- Analytics (GA, etc.)
