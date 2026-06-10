# Critique — LeadGen Pro Landing Page

**Data:** 2026-06-02 · **Target:** `leadgen-pro/index.html` · **Slug:** `leadgen-pro-index-html`

---

## Design Health Score

| # | Heurística | Score | Achado |
|---|---|---|---|
| 1 | Visibility of System Status | **2/4** | Nav active state não renderiza (JS adiciona `.is-active`, CSS não tem regra) |
| 2 | Match System / Real World | **3/4** | Vocabulário B2B correto (pipeline, cadência, ICP, decisor). `<MakeCash />` é dev-speak |
| 3 | User Control and Freedom | **3/4** | Sticky nav + drawer mobile + accordion single-open. Sem atalho para pricing |
| 4 | Consistency and Standards | **3/4** | Cards, botões e ritmo consistentes. Glyphos diferentes para mesma semântica (✓ vs •) |
| 5 | Error Prevention | **3/4** | Sem forms = baixo risco. Anchor links evitam 404. `og:image` aponta para arquivo deletado |
| 6 | Recognition Rather than Recall | **3/4** | Tudo visível no nav. Sem tooltips em elementos de UI mockup |
| 7 | Flexibility and Efficiency | **2/4** | Sem atalhos de teclado, sem "pular para pricing", jornada rígida de 10 seções |
| 8 | Aesthetic and Minimalist Design | **3/4** | Foco claro em cada seção. Mas 10 seções + 5+ CTAs "Começar agora" competem |
| 9 | Error Recovery | **3/4** | FAQ atualizada e honesta. Sem contato humano além de email no footer |
| 10 | Help and Documentation | **2/4** | FAQ com 6 perguntas. Sem docs, sem chat, sem contato visível |
| **Total** | | **27/40** | **Acceptable** — base sólida, precisa de polimento de jornada |

---

## Anti-Patterns Verdict

**LLM:** Não parece AI-generated. Tem voz (terminal-native, `<ComponentName />` labels, mockups CSS detalhados, paleta dark indigo com green de sucesso). Mas há um tell sutil: a **densidade de seções** (10) + **repetição de CTAs idênticos** + **falta de prova social real** formam o "tudo certinho mas nada convence" que é o AI default.

**Deterministic scan:** 2 findings, ambos parciais falso-positivo:
- `single-font` (warning) — Manrope em 5 pesos é escolha deliberada; detector não entende "single family well-tuned"
- `numbered-section-markers` (advisory) — 01/02/03 aparecem só dentro de UMA seção (MakeCash) que É uma sequência de 3 features. Não é scaffold. Detector over-broad.

**Visual overlays:** não executado (sem browser automation disponível nesta sessão).

---

## Overall Impression

O site tem **vocabulário visual próprio** (escuro, técnico, mockups inline, labels estilo código) e **fundação técnica sólida** (a11y, performance, theming). Mas a **jornada é plana e a página é longa demais** para a decisão que o usuário precisa tomar: "isso é para mim e cabe no bolso?"

O **maior gap** é a ausência de **narrativa emocional** e **prova social real**. A página descreve features com confiança técnica, mas não constrói confiança humana. Para um SaaS B2B que quer vender para gerentes comerciais conservadores, isso é um problema.

**Single biggest opportunity:** Inserir uma camada de **prova social crível** (depoimento real, logo de cliente, screenshot de resultado mensurável) entre o hero e o pricing. Isso fecha a lacuna "técnico sim, confiável não".

---

## What's Working

1. **Mockups CSS-only** (produto no hero, kanban do pipeline, dashboard de analytics) mostram o produto real em ação, sem o ruído de screenshot mal cortado. É o ativo visual mais forte da página.
2. **`<ComponentName />` labels** dão identidade técnica coerente (viram parte do sistema de design, não scaffold). Diferencia de SaaS genérico.
3. **Hero "Encontre. Engaje. Converta."** em 3 pesos diferentes com 3 cores — é uma assinatura visual que comunica a promessa em 2 segundos. Funciona como tag de marca.
4. **FAQ atualizada e honesta** ("Sim, precisa de cartão. Sem fidelidade.") — quebra expectativa do "começar grátis" padrão, gera confiança real.

---

## Priority Issues

### [P1] Nav active state não renderiza (bug silencioso)
- **Localização:** `js/main.js:78-90` adiciona `.is-active`, mas `css/styles.css` só tem a regra para `.product-mock__nav a.is-active`, não para `.nav__links a.is-active`
- **Why it matters:** Usuário scrollando pela página não vê onde está. Compromete a heurística 1 (visibility of system status) inteiramente
- **Fix:** Adicionar `.nav__links a.is-active { color: var(--ink-100); }` e opcional underline
- **Comando:** `/impeccable polish`

### [P1] `og:image` aponta para arquivo deletado
- **Localização:** `index.html:16`
- **Why it matters:** Toda vez que o site for compartilhado em LinkedIn, Twitter, WhatsApp, Slack, o preview vai ser broken. É a primeira impressão que contatos profissionais recebem
- **Fix:** Substituir por uma URL real (gerar um OG image 1200x630 com hero + título) ou apontar para `images/favicon.svg`
- **Comando:** `/impeccable harden` ou gerar imagem dedicada

### [P1] Sem prova social real
- **Localização:** toda a página, exceto a frase vaga "Mais de 800 times de vendas B2B" no CTA final (que é número fabricado)
- **Why it matters:** Para B2B, o gerente de vendas não compra feature, compra confiança. Sem depoimento, logo de cliente, métrica de resultado mensurável, a página soa como pitch de deck
- **Fix:** Adicionar 1-2 depoimentos curtos (com nome, cargo, empresa) entre Pricing e CTA final. Ou um logo strip ("Usado por times de vendas em:") no topo da pricing section
- **Comando:** `/impeccable clarify` ou copy direto

### [P1] CTA "Ver demonstração" é enganoso
- **Localização:** `index.html:106-109` — link vai para `#modulos`, não para uma demo real
- **Why it matters:** Quebra expectativa. Usuário clica esperando um vídeo ou tour interativo, recebe uma seção de texto. Gera frustração e quebra confiança (heurística 2)
- **Fix:** Ou renomear para "Ver como funciona" (mais honesto) ou construir uma mini-demo (gif/looped video) no hero
- **Comando:** `/impeccable clarify`

### [P2] Pricing escondida após 8 seções
- **Localização:** estrutura da página (1-8 são features, 9 é pricing)
- **Why it matters:** B2B buyers fazem "filtro de orçamento" cedo. Quem não tem budget sai antes de chegar no preço, e quem tem fica 8 scrolls esperando
- **Fix:** Adicionar um floating "Ver preços" button no canto inferior direito (mobile-first) ou um "Preços desde R$ 50/mês" sutil no hero sub
- **Comando:** `/impeccable layout` ou `/impeccable adapt`

### [P2] CTAs idênticos competem por atenção
- **Localização:** "Começar agora" aparece 5 vezes (header, drawer, hero, pricing card Pro, final CTA)
- **Why it matters:** Quando tudo é primário, nada é. Apple.com usa 1 CTA por viewport
- **Fix:** Variar linguagem: "Começar agora" (header/hero), "Assinar Starter"/"Assinar Pro" (pricing), "Criar conta" (final). Já fiz parte dessa variação
- **Comando:** `/impeccable clarify`

### [P2] Falta affordance de atalho para humanos ocupados
- **Localização:** navegação inteira
- **Why it matters:** Manager quer 3 informações: o que é, quanto custa, é confiável. Hoje a página força sequência linear
- **Fix:** Botão "Ver preços" persistente no canto, ou um mini-sticky no mobile
- **Comando:** `/impeccable adapt`

### [P3] Seção "extensions" usa WhatsApp + LinkedIn de forma simétrica mas LinkedIn mostra "Maria Souza / Têxtil Brasil" sem mostrar cadência ativa (só botão "salvar")
- **Localização:** `index.html:530-560`
- **Why it matters:** O WhatsApp card mostra uma tarefa em andamento (Tarefa 3/6 com template). O LinkedIn card só mostra perfil + botão. A simetria está quebrada — a extensão LinkedIn parece subutilizada
- **Fix:** Adicionar uma tarefa "LinkedIn: enviar InMail personalizado" no card do LinkedIn para paridade
- **Comando:** `/impeccable layout`

---

## Persona Red Flags

**Jordan (First-Timer) — gerente comercial que nunca usou CRM moderno:**
- Acha 10 seções intimidadoras. Espera um "tour" guiado, não documentação.
- O label `<MakeCash />` parece o nome de uma função JavaScript, não de um produto. **Confusão de domínio**.
- "ICP" aparece 3 vezes sem definição. **Jargão sem glossário** — quem não sabe o que é fica de fora.
- O FAQ explica "ICP" indiretamente mas só depois de scrollar até o final.

**Casey (Mobile) — vendo no celular, no metrô, com uma mão:**
- Hero CTAs ficam stacked vertical no mobile (✓), mas o **botão primário "Começar agora" não está no thumb zone** (centro da tela, não embaixo). Teria que rolar para alcançar.
- O **product mockup do hero** some de forma útil no mobile (vira só os leads cards sem a sidebar) mas **perde o "wow"** que justifica rolar a página inteira.
- Não tem sticky CTA bar no mobile que diga "Quero experimentar". **Conversão mobile fica abaixo do desktop**.

**Carla (SDR, persona implícita no chrome mockup) — a usuária real do produto:**
- O **Painel Hoje** (citado como feature) não aparece em lugar nenhum como mockup. É a feature mais citada do Engage, mas não tem prova visual.
- As cadências mostram o **fluxo do gestor** (definir 6 passos). Não mostram o **fluxo do SDR** (abrir o painel e executar 12 tarefas). São dois lados do mesmo produto, e só um está visualizado.
- O **"Gerente de Compras"** é o decisor-tipo mostrado em todas as 4 leads cards do mockup de busca. A repetição sugere viés — o produto serve só para "gerente de compras"? Falta variedade de decisor (CEO, CFO, Diretor de TI).

---

## Minor Observations

- **Footer com 3 colunas de links** (Produto, Empresa, Legal) mas os links de "Termos de uso", "Privacidade", "Segurança" em `href="#"` são placeholders não-funcionais. **Quebra a heurística 4** (consistency) — todos os outros links do site funcionam.
- **`<system />` label no início** é o único que não é nome de componente. Inconsistência na cadência.
- **Empresa "Têxtil Brasil"** aparece no IA insights (R$ 134k) e no card do LinkedIn (Maria Souza). Continuidade narrativa ✓.
- **"João Silva"** aparece no WhatsApp extension e nos leads cards do hero mockup (Alimentos Marfim). Mesma continuidade, mostra que o produto "amarra" o lead ao canal. ✓
- **Em-dash ausente** ✓ (usei vírgulas e pontos). 
- **Lingagem consistente**: copy em PT-BR, terminologia B2B brasileira (CNAE, "Gerente de Compras" em vez de "Head of Procurement").
- **OG e Twitter Card** descrevem o produto bem, mas a imagem está quebrada (ver P1).

---

## Questions to Consider

- **Se você tivesse que cortar 4 das 10 seções, quais ficam?** (Sugestão: Prospecção, Cadências, Extensões, Pricing. O resto é nice-to-have.)
- **A primeira impressão é "ferramenta técnica para times de vendas" ou "produto premium que vai me fazer bater meta"?** Hoje pende para o primeiro. Qual é a voz de marca certa?
- **Quem é a Carla Mendes que aparece no chrome mockup?** Se ela é o "user persona", dê a ela uma página de caso de uso inteira — não só um avatar.
- **Qual o resultado de um cliente real?** "Antes: 5 leads/semana. Depois: 30 leads/semana." Esse número é mais persuasivo que qualquer feature list.
- **Você está confortável publicando a página com R$ 50/mês Starter, sabendo que HubSpot/Salesforce têm free tiers?** Se sim, o argumento da página precisa mudar de "preço" para "foco B2B Brasil + cadências + extensões".

---

**Trend for `leadgen-pro-index-html` (last 5 runs):** First run for this target, no trend yet.

Wrote `.impeccable/critique/2026-06-02-leadgen-pro-index-html.md`.
