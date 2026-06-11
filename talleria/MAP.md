# MAP — Context Index for Token-Efficient Editing

> **Purpose:** Know WHERE to look before reading. Never read a full file blind.
> **Rule:** `grep` → `MAP.md` → `Read(offset, limit)` → edit.

---

## CSS (`css/styles.css` — 3639 lines)

| Lines   | Section                          | Key Classes                                         |
|---------|----------------------------------|------------------------------------------------------|
| 1-94    | **Variables + Reset**            | `:root`, `*`, `html`, `body`, `.skip-link`, `.container` |
| 95-162  | **Buttons**                      | `.btn`, `.btn--accent`, `.btn--trust`, `.btn--outline-light` |
| 163-320 | **Product Nav**                  | `.product-nav`, `.nav-wordmark`, hamburger, mobile menu |
| 321-470 | **Hero Apple**                   | `.hero--apple`, headline/sub/badge/price/visual      |
| 471-525 | **Carousel**                     | `.carousel`, `.carousel__track`, auto-scroll          |
| 526-534 | **Full-Bleed utility**           | `.full-bleed`                                        |
| 535-591 | **Apple Design section**         | `.apple-design`, label/headline/image                |
| 592-677 | **Bento Grid**                   | `.bento-grid`, `.bento-card`, dark background        |
| 678-756 | **Lifestyle**                    | `.apple-lifestyle`, stats, dark background           |
| 757-943 | **Specs**                        | `.apple-specs`, grid values                          |
| 944-1161| **Video Feature**                | `.video-feature`, player, text, list                 |
| 1162-1225| **Box Grid**                    | `.apple-box`, dark background                        |
| 1226-1301| **Why Buy**                     | `.whybuy`, cards, icons                              |
| 1302-1390| **Testimonials**                | `.testimonials`, `.testimonial-card`, stars/quotes   |
| 1391-1465| **Compare Table**               | `.apple-compare`, `.compare-table`                   |
| 1466-1527| **Specs FAQ**                   | `.specs-faq`, `.faq-item`, accordion                 |
| 1528-1621| **CTA Final**                   | `.apple-cta`, headline/price/btn/trust               |
| 1622-1696| **CTA Sticky Mobile**           | `.cta-sticky`, fixed bottom bar                      |
| 1697-1770| **Footer**                      | `.footer`, columns, `.footer-wordmark`               |
| 1771-2018| **Animations**                  | `@keyframes`, `.animate-in`, parallax effects        |
| 2019-2354| **Homepage extras**             | Homepage-specific overrides                          |
| 2355-2952| **Homepage v3**                 | Brand hero, manifesto, values, products grid         |
| 2953-3600| **Secondary Pages**             | `sobre.html`, `faq.html`, `contacto.html` styles     |
| 3601-3639| **Utilities**                   | `.scroll-progress`, misc                             |

---

## HTML Pages

### `producto.html` (773 lines) — Product page (old layout restored)
| Lines   | Section                         |
|---------|---------------------------------|
| 1-46    | Head, meta, schema.org          |
| 47-83   | Nav (Two Line Stack wordmark)   |
| 85-106  | Hero (hero--apple)              |
| 107-129 | Carousel (8 spin images)        |
| 130-139 | Design section                  |
| 140-170 | Bento Grid (3 cards)            |
| 171-194 | Lifestyle (stats overlay)       |
| 195-229 | Video 1 — GISAM                 |
| 230-263 | Video 2 — CultivoX              |
| 264-293 | Specs (5 values)                |
| 294-319 | Box contents (4 items)          |
| 320-353 | Video 3 — DIY ALAM              |
| 354-387 | Video 4 — Temu                  |
| 388-425 | Why Buy (6 cards)               |
| 426-468 | Testimonials (3 reviews)        |
| 469-514 | Compare table                   |
| 515-553 | Specs FAQ (3 items)             |
| 554-585 | CTA Final + countdown           |
| 586-597 | CTA Sticky mobile               |
| 598-650 | Footer                          |
| 651-773 | Inline JS (observer, parallax)  |

### `index.html` — Homepage
| Lines   | Section                         |
|---------|---------------------------------|
| 83-98   | Brand Hero                      |
| 100-120 | Stats Bar                       |
| 122-135 | Manifesto                       |
| 137-152 | History                         |
| 154-177 | Values (3 pillars)              |
| 179-216 | Video Feature                   |
| 218-276 | Products Grid                   |
| 278-314 | Compromiso                      |
| 316-357 | Testimonials                    |
| 359-384 | Brand CTA                       |
| 387+    | Sticky CTA + Footer             |

---

## JS (`js/scripts.js` — ~470 lines)

| Lines   | Feature                         |
|---------|---------------------------------|
| 1-95    | Scroll reveal + parallax        |
| 96-126  | Product Nav Transition          |
| 127-152 | Paint Reveal animation          |
| 153-267 | 360° Touch Rotation + Lazy-load |
| 268-308 | Highlights Interactive Tabs      |
| 309-347 | 3D Parallax Hero                |
| 348-375 | Why Buy sequential reveal        |
| 376-401 | Scroll-spy product nav           |
| 402-429 | Hamburger toggle                 |
| 430-470 | Video player                     |

---

## How to Use This Map

**Before any edit:**
1. `grep` for the class/section name in the target file
2. Check MAP.md for the line range
3. `Read(filePath, offset, limit)` with narrow range
4. Edit only what you need

**Example — "change the hero price color":**
```
grep "hero--apple__price" talleria/css/styles.css
→ Found at line 439
Read talleria/css/styles.css offset=439 limit=10
→ See the price CSS, edit color
```

**Token cost comparison:**
- ❌ Old: Read full CSS = ~20,000 tokens
- ✅ New: grep + Read 10 lines = ~1,000 tokens (95% savings)
