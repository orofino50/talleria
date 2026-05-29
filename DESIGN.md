---
name: AltaPro
description: Sitio web premium de herramientas eléctricas portátiles
colors:
  primary: "#e94560"
  trust: "#2ecc71"
  neutral-bg: "#f5f5f7"
  neutral-bg-white: "#ffffff"
  neutral-bg-dark: "#1a1a2e"
  neutral-bg-dark-alt: "#16213e"
  neutral-text-primary: "#1d1d1f"
  neutral-text-secondary: "#6e6e73"
  neutral-text-inverse: "#ffffff"
  neutral-border: "#e8e8ed"
typography:
  display:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(3rem, 6vw, 5rem)"
    fontWeight: 900
    lineHeight: 1.05
    letterSpacing: "-3px"
  headline:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(2rem, 3vw, 2.5rem)"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.5px"
  title:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "1.125rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.3px"
  body:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "clamp(1rem, 1.1vw, 1.125rem)"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    letterSpacing: "0.12em"
    textTransform: "uppercase"
rounded:
  card: "16px"
  button: "8px"
  button-trust: "12px"
  input: "10px"
  spec: "12px"
  badge: "4px"
  header-cta: "6px"
spacing:
  section-mobile: "80px 24px"
  section-tablet: "120px 40px"
  section-desktop: "160px 80px"
  card-padding: "32px"
  grid-gap: "20px"
components:
  button-accent:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral-text-inverse}"
    rounded: "{rounded.button}"
    padding: "16px 40px"
  button-accent-hover:
    backgroundColor: "#d63851"
  button-trust:
    backgroundColor: "{colors.trust}"
    textColor: "{colors.neutral-text-inverse}"
    rounded: "{rounded.button-trust}"
    padding: "20px 64px"
  button-trust-hover:
    opacity: "0.95"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.neutral-text-inverse}"
    rounded: "{rounded.button}"
    padding: "14px 36px"
    border: "2px solid rgba(255,255,255,0.3)"
  card-default:
    backgroundColor: "{colors.neutral-bg-white}"
    textColor: "{colors.neutral-text-primary}"
    rounded: "{rounded.card}"
    border: "1px solid {colors.neutral-border}"
    padding: "{spacing.card-padding}"
  card-dark:
    backgroundColor: "{colors.neutral-bg-dark-alt}"
    textColor: "{colors.neutral-text-inverse}"
    rounded: "{rounded.card}"
    border: "1px solid rgba(255,255,255,0.06)"
    padding: "{spacing.card-padding}"
  header-cta:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.neutral-text-inverse}"
    rounded: "{rounded.header-cta}"
    padding: "8px 20px"
---

# Design System: AltaPro

## 1. Overview

**Creative North Star: "Luz de Estúdio"**

Como um estúdio fotográfico profissional — fundo claro e neutro (#f5f5f7) onde o produto é a estrela, com holofotes escuros (#1a1a2e) direcionados apenas para hero e CTA final. O coral elétrico (#e94560) funciona como ponteiro visual preciso: ≤10% da tela, nunca competindo consigo mesmo. As bordas finas (#e8e8ed) e o radius generoso (16px) criam uma sensação Apple de precisão industrial sem recorrer a sombras ou glassmorphism.

O sistema rejeita explicitamente: gradientes purple-to-blue, cards aninhados, temas escuros genéricos sem personalidade, excesso de badges, tom de "vendedor de TV". A qualidade se percebe no espaço negativo, na tipografia limpa e nas transições sutis.

**Key Characteristics:**
- Light-first: fundo #f5f5f7 como padrão, cards brancos (#ffffff), escuro (#1a1a2e) só para seções de alto impacto
- Apple-inspired: bordas finas (#e8e8ed), radius 16px, letter-spacing negativo em títulos, sem sombras
- Multi-página consistente: header fixo, footer, tipografia e ritmo visual idênticos em todas as 5 páginas
- Coral Elétrico como único accent visual — usado exclusivamente para CTAs, labels de seção e ícones
- Scroll reveal com ease-out quart, navbar transparente→branca com blur no scroll
- Zero glassmorphism, zero gradientes decorativos, zero cards aninhados

## 2. Colors

A paleta é deliberadamente restrita: tons claros e neutros para o fundo (estúdio), azuis escuros para impacto dramático (holofote), e dois pontos de cor precisos para ação.

### Primary
- **Coral Elétrico** (#e94560): O accent único. Usado exclusivamente para CTAs primárias, labels de seção, ícones de card, e o botão "Comprar" no header. Sua saturação é proposital — deve ser o único elemento que compete por atenção.

### Secondary (Trust)
- **Verde Garantía** (#2ecc71): Usado para o CTA final de compra (seção de checkout) e links de WhatsApp na página de contato. Exclusivo para momentos de decisão/confirmação.

### Neutral
- **Blanco Estudio** (#f5f5f7): Background principal do body e seções padrão. Equivalente ao #f5f5f7 da Apple.
- **Blanco Puro** (#ffffff): Background de cards, formulários e containers internos. Cria contraste sutil com o fundo.
- **Noche Azul** (#1a1a2e): Background do hero e da seção CTA final. Usado exclusivamente para as duas seções de alto impacto.
- **Azul Profundo** (#16213e): Background alternativo para seções escuras (galeria de produto, vídeo). Variação sutil da Noche Azul.
- **Casi Negro** (#1d1d1f): Texto primário em fundos claros — quase preto, não #000000. Equivalente ao #1d1d1f da Apple.
- **Gris Medio** (#6e6e73): Texto secundário, subtítulos, labels de especificação, metadados. Equivalente ao #6e6e73 da Apple.
- **Blanco** (#ffffff): Texto sobre fundos escuros (hero, CTA final, seções dark).
- **Gris Borde** (#e8e8ed): Bordas de cards, inputs, separadores, footer. Equivalente ao #e8e8ed da Apple.

### Named Rules
**The Single Accent Rule.** O Coral Elétrico aparece em ≤10% de qualquer tela. Sua raridade é o que o faz funcionar. Nunca competir com ele mesmo — um só CTA por viewport.

## 3. Typography

**Display & Body Font:** Inter (monofamília com fallback system-ui)

**Character:** Monotipia intencional. Uma só família em pesos estratégicos (400/600/700/900) cria contraste máximo sem precisar de múltiplos tipos. A voz é precisa, industrial, limpa — como as ferramentas que a marca vende. Letter-spacing negativo em títulos (até -3px no display) para compactação óptica Apple-style.

### Hierarchy
- **Display** (900, clamp(3rem, 6vw, 5rem), 1.05, -3px): Hero headline. Máximo impacto, usado exclusivamente na página inicial.
- **Headline** (700, clamp(2rem, 3vw, 2.5rem), 1.2, -0.5px): Títulos de seção. Em todas as páginas.
- **Title** (700, 1.125rem, 1.3, -0.3px): Títulos de cards, especificações e destaques internos.
- **Body** (400, clamp(1rem, 1.1vw, 1.125rem), 1.7): Parágrafos, descrições. Line length controlado por max-width (600–700px).
- **Label** (700, 0.75rem, 0.12em uppercase): Badges, labels de seção (ex: "PAINTPRO"), metadados. Sempre em caixa alta.
- **Small** (400, 0.938rem, 1.6): Texto auxiliar em cards, depoimentos, FAQ.

### Named Rules
**The Single Voice Rule.** Inter em todas as variantes. Nunca adicionar uma segunda fonte. O contraste vem do weight e do letter-spacing, não da família.

## 4. Elevation

O sistema não usa sombras. Zero `box-shadow` em todo o design. A hierarquia visual é criada por:
- **Bordas finas** (#e8e8ed, 1px) separando superfícies claras
- **Espaço negativo generoso** entre elementos
- **Hover lift** como única resposta de profundidade: cards sobem 4px (`translateY(-4px)`) com transição de 300ms ease

Em fundos escuros (Noche Azul, Azul Profundo), a distinção entre seções vem do tom da camada, não de bordas ou sombras. A transição hero → seção clara é abrupta e intencional: o contraste entre escuro e claro substitui qualquer necessidade de elevação.

### Named Rules
**The No-Shadow Rule.** Box-shadows são proibidos em qualquer estado. Profundidade é criada por contraste tonal, bordas finas e espaço negativo.

## 5. Components

### Buttons

- **Shape:** Cantos suavemente retos — 8px (primário, ghost), 12px (trust/CTA final), 6px (header CTA)
- **Accent (Primary):** Coral Elétrico (#e94560) sólido, texto branco, peso 700, padding 16px 40px. Hover: opacidade 0.9 em 200ms ease.
- **Trust (Final):** Verde Garantía (#2ecc71) sólido, texto branco, peso 700, padding 20px 64px, letter-spacing 0.02em. Hover: opacidade 0.95 em 200ms ease.
- **Ghost (Dark bg):** Transparente, texto branco, borda 2px rgba(255,255,255,0.3), padding 14px 36px. Hover: borda mais clara.
- **Outline (Light bg):** Transparente, texto Casi Negro, borda 2px Gris Borde, padding 14px 36px. Hover: borda Casi Negro.
- **Link (Dark bg):** Texto branco, underline com offset 4px, opacidade 0.7 → 1 no hover.
- **Header CTA:** Coral Elétrico, texto branco, peso 700, padding 8px 20px, radius 6px. Aparece como botão no desktop, dentro do menu mobile.
- **States:** Nenhum botão usa sombras ou escalas. Transições são exclusivamente de opacidade e cor (200ms ease).

### Navigation

- **Style:** Header fixo no topo (z-index 100), transparente no topo da página, transiciona para branco com blur (rgba(255,255,255,0.9) + backdrop-filter: blur(12px)) ao scrollar.
- **Logo:** AltaPro, peso 900, 1.25rem, letter-spacing -0.5px. "Alta" em branco (inverso) ou Casi Negro (scrolled), "Pro" em Coral Elétrico.
- **Links:** 0.875rem, peso 500, cor rgba(255,255,255,0.7) → branco no hover (dark bg). No scroll: Gris Medio → Casi Negro no hover.
- **Active:** Peso 600, cor branca (dark) ou Casi Negro (scrolled).
- **Mobile:** Hamburger icon (3 linhas, 22px, animação X ao abrir). Menu slide-down com fundo branco, links peso normal.
- **Breakpoint:** Mobile < 768px.

### Cards / Containers

- **Corner Style:** Arredondamento grande (16px radius).
- **Background:** Blanco Puro (#ffffff) em fundos claros; Azul Profundo (#16213e) em seções escuras (`.card--dark`).
- **Border:** 1px sólido Gris Borde (#e8e8ed) nos claros; 1px rgba(255,255,255,0.06) nos escuros.
- **Shadow:** Nenhum.
- **Internal Padding:** 32px.
- **Hover:** translateY(-4px) em 300ms ease.
- **Layout:** Grid responsivo (1 → 2 → 3→4 colunas via classes `.cards-grid--2/3/4`).

### Spec Items

- **Corner Style:** Arredondamento médio (12px radius).
- **Background:** Blanco Puro (#ffffff).
- **Border:** 1px sólido Gris Borde (#e8e8ed).
- **Internal Padding:** 24px 20px.
- **Label:** Label style (0.688rem, 700, uppercase, 0.08em), sempre Coral Elétrico.
- **Layout:** Grid 2 colunas mobile → 5 colunas desktop.

### Inputs / Fields

- **Style:** Blanco Puro (#ffffff), borda 1px Gris Borde (#e8e8ed), radius 10px, padding 14px 16px.
- **Label:** 0.813rem, peso 700, Gris Medio, letter-spacing 0.02em.
- **Focus:** outline none, borda muda para Coral Elétrico em 200ms ease.
- **Placeholder:** Gris Medio com opacidade 0.5.
- **Textarea:** min-height 120px, resize vertical.

### FAQ Accordion

- **Structure:** Itens separados por borda horizontal (1px Gris Borde, superior no primeiro, inferior no último).
- **Question:** 1rem, peso 600, Casi Negro. Hover: Coral Elétrico. Padding 20px 0.
- **Icon:** Símbolo "+" (1.25rem, Gris Medio), rotaciona 45° ao abrir (state `.is-open`).
- **Answer:** max-height animado (0 → 300px) em 300ms ease, texto Gris Medio 0.938rem.

### Gallery Items

- **Corner Style:** 16px.
- **Background:** Azul Profundo (#16213e) com borda sutil rgba(255,255,255,0.06).
- **Aspect Ratio:** 4:3.
- **Content:** Ícone grande (3rem, opacidade 0.3) + label (0.813rem, 600, uppercase, opacidade 0.5).

## 6. Do's and Don'ts

### Do:
- **Do** usar #f5f5f7 como fundo padrão e #ffffff para cards — o contraste sutil cria hierarquia sem esforço.
- **Do** reservar o fundo escuro (#1a1a2e) exclusivamente para hero e CTA final — o impacto vem da raridade.
- **Do** usar Coral Elétrico como o único ponteiro visual para ação. Máximo 10% da tela.
- **Do** manter botões com padding generoso (16px 40px no mínimo) para alvos de toque confortáveis.
- **Do** incluir hover lift (translateY -4px, 300ms ease) em cards — é a única resposta de profundidade do sistema.
- **Do** usar letter-spacing negativo em títulos (-3px display, -0.5px headline) para compactação óptica.
- **Do** manter consistência de header, footer e tipografia nas 5 páginas.
- **Do** usar prefers-reduced-motion para desligar animações quando solicitado.

### Don't:
- **Don't** usar sombras (box-shadow) em nenhum elemento. A profundidade é tonal e espacial, não luminosa.
- **Don't** adicionar uma segunda fonte. Inter em pesos 400/600/700/900 é o sistema completo.
- **Don't** usar glassmorphism, gradientes decorativos ou purple-to-blue gradients (anti-reference: diseño genérico de IA).
- **Don't** usar cards aninhados ou side-stripe borders (border-left/border-right como accent).
- **Don't** usar texto gradiente com background-clip: text.
- **Don't** usar grey text on colored backgrounds — o Gris Medio (#6e6e73) só aparece sobre fundos claros ou brancos.
- **Don't** adicionar eyebrow tracking (tiny uppercase label acima de seções). O label de seção já é auto-suficiente.
- **Don't** usar bounce ou elastic easing. Todas as transições usam ease-out (200–600ms).
- **Don't** criar temas escuros genéricos sem personalidade (anti-reference: templates de IA que parecem "vibecoding").
- **Don't** adicionar emojis como ícones. Use SVGs inline para ícones de card, contato e valores.
