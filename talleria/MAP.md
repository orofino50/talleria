# MAP — Context Index for Token-Efficient Editing

> **Purpose:** Know WHERE to look before reading. Never read a full file blind.
> **Rule:** `grep` → `MAP.md` → `Read(offset, limit)` → edit.

---

## CSS (`css/styles.css` — 4521 lines)

| Lines   | Section                          | Classes                                         |
|---------|----------------------------------|--------------------------------------------------|
| 1-94    | **Variables + Reset**            | `:root`, `*`, `html`, `body`, `.skip-link`, `.container` |
| 95-162  | **Buttons**                      | `.btn`, `.btn--accent`, `.btn--trust`, `.btn--outline-light` |
| 163-334 | **Product Nav**                  | `.product-nav`, `.nav-wordmark`, hamburger, mobile menu |
| 335-460 | **Hero Apple (homepage)**        | `.hero--apple`, `.hero--apple__visual`, headline/sub/badge |
| 461-589 | **Hero Product (old?)**          | `.hero--apple--product`, product hero variant     |
| 590-646 | **Carousel**                     | `.carousel`, `.carousel__track`, auto-scroll       |
| 647-655 | **Full-Bleed utility**           | `.full-bleed`                                     |
| 656-712 | **Apple Design section**         | `.apple-design`, label/headline/text/visual       |
| 713-798 | **Bento Grid**                   | `.bento-grid`, dark background                    |
| 799-877 | **Lifestyle**                    | `.lifestyle`, dark background                     |
| 878-1064| **Specs (old?)**                 | `.specs`, spec cards, grid                        |
| 1065-1282| **Video Feature**               | `.video-feature`, player, text, list              |
| 1283-1346| **Box Grid**                    | `.box-grid`, dark background                      |
| 1347-1422| **Why Buy**                     | `.why-buy`, cards, icons                          |
| 1423-1511| **Testimonials**                | `.testimonials`, stars, quotes, avatars           |
| 1512-1586| **Compare Table**               | `.compare-table`, highlights                      |
| 1587-1648| **Specs FAQ**                   | `.specs-faq`, accordion, details                  |
| 1649-1742| **CTA Final**                   | `.brand-cta`, headline/sub/price/btn/trust        |
| 1743-1817| **CTA Sticky Mobile**           | `.cta-sticky`, fixed bottom bar                   |
| 1818-1891| **Footer**                      | `.footer`, columns, wordmark                      |
| 1892-2139| **Animations**                  | `@keyframes`, `.animate-in`, parallax effects     |
| 2140-2475| **Homepage extras**             | Homepage-specific overrides                       |
| 2476-3114| **Homepage v3**                 | Brand hero, manifesto, values, products grid      |
| 3115-3762| **Secondary Pages**             | `sobre.html`, `faq.html`, `contacto.html` styles  |
| 3763-3800| **Utilities**                   | `.scroll-progress`, misc                          |
| **3801-4521** | **Product Page (ap-*)**    | **← MOST USED** See below                        |

### Product Page CSS (`ap-*` classes, lines 3801-4521)

| Lines   | Component                       | Key Classes                                      |
|---------|----------------------------------|--------------------------------------------------|
| 3801-3818| **Section headline + eyebrow** | `.ap-section-headline`, `.ap-eyebrow`             |
| 3820-3905| **Hero**                       | `.ap-hero`, `__inner`, `__visual`, `__headline`, `__sub`, `__price`, `__actions`, `__hint` |
| 3907-3940| **Carousel**                   | `.ap-carousel`, `__track`, `__slide`              |
| 3942-3994| **Highlights**                 | `.ap-highlights`, `__grid`, `.ap-highlight`       |
| 3996-4032| **Social Proof Bar**           | `.ap-social-bar`, `__inner`, `__stat`, `__value`, `__label`, `__divider` |
| 4034-4128| **Video**                      | `.ap-video`, `__inner`, `__text`, `__headline`, `__list`, `__player`, `__video`, `__play` |
| 4130-4175| **Compare**                    | `.ap-compare`, `__table`, `__highlight`, `__row-label` |
| 4177-4228| **CTA Mid-page**               | `.ap-cta-mid`, `__inner`, `__price`, `__current`, `__original`, `__badge` |
| 4230-4296| **Specs + Box**                | `.ap-specs`, `__inner`, `__item`, `__question`, `__answer`, `.ap-box__grid/item/image/label` |
| 4298-4370| **Testimonials**               | `.ap-testimonials`, `__grid`, `.ap-testimonial`, `__stars`, `__quote`, `__author` |
| 4372-4425| **Trust**                      | `.ap-trust`, `__grid`, `__item`, `__icon`, `__title`, `__text` |
| 4427-4521| **CTA Final**                  | `.ap-cta`, `__headline`, `__sub`, `__price`, `__countdown`, `__btn`, `__trust` |

---

## HTML Pages

### `producto.html` (580 lines) — Product page
| Lines   | Section                         |
|---------|---------------------------------|
| 1-43    | Head, meta, schema.org          |
| 44-77   | Nav                             |
| 79-99   | 1. Hero (price + discount)      |
| 101-127 | 2. Carousel (11 SVGs)           |
| 129-157 | 3. Highlights (3 features)      |
| 159-177 | 4. Social Proof Bar             |
| 179-208 | 5. Video (GISAM only)           |
| 210-253 | 6. Compare table                |
| 255-266 | 7. CTA Mid-page                 |
| 268-322 | 8. Specs + Box contents         |
| 324-364 | 9. Testimonials (3 reviews)     |
| 366-393 | 10. Trust (4 items)             |
| 395-422 | 11. CTA Final + countdown       |
| 424-435 | CTA Sticky mobile               |
| 437-478 | Footer                          |
| 480-577 | Inline JS (observer, countdown) |

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

### Other pages
- `sobre.html` — Brand story, team, values
- `faq.html` — Accordion FAQ
- `contacto.html` — Contact cards + form

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

**Example — "change the hero price color in product page":**
```
grep "ap-hero__price" talleria/css/styles.css
→ Found at line 3876
Read talleria/css/styles.css offset=3876 limit=30
→ See the price CSS, edit color
```

**Token cost comparison:**
- ❌ Old: Read full CSS = ~25,000 tokens
- ✅ New: grep + Read 30 lines = ~2,000 tokens (92% savings)
