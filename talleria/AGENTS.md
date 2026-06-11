# AGENTS.md — Talleria Pro

## Quick Context

- **Site:** https://orofino50.github.io/talleria/
- **Repo:** https://github.com/orofino50/talleria
- **Published:** 5 pages (index, producto, sobre, faq, contacto)
- **CSS:** `css/styles.css` (3639 lines) — see `MAP.md` for line ranges
- **JS:** `js/scripts.js` (~470 lines)
- **Images:** `images/` (SVGs, WebP, MP4/WebM videos)

## Design Tokens

| Token           | Value     | Usage                    |
|-----------------|-----------|--------------------------|
| `--bg-black`    | #000000   | Hero, dark sections      |
| `--bg-dark`     | #1a1a2e   | Dark section backgrounds |
| `--bg-light`    | #f5f5f7   | Light section backgrounds|
| `--bg-white`    | #ffffff   | Card backgrounds         |
| `--accent`      | #C5A55A   | Gold — CTAs, highlights  |
| `--accent-hover`| #A8903D   | Gold hover state         |
| `--trust`       | #1a9e58   | Trust badges, CTA final  |
| `--text-primary`| #1d1d1f   | Headings                 |
| `--text-secondary`| #6e6e73 | Body text                |
| `--border-light`| #e8e8ed   | Borders, dividers        |
| `--font-family` | Inter     | 300/400/600/700/900      |

## Rules

- **No box-shadow** — use borders + hover lift
- **No `background-clip: text`** — banned
- **No decorative animations** — only scroll reveal + parallax
- **No glassmorphism** — no backdrop-filter (except nav frosted glass)
- **Language:** Español (España)
- **Accent usage:** ≤10% of screen

## File Edit Workflow

**CRITICAL:** Always edit `talleria/` files FIRST, then sync to root.

```powershell
# After editing talleria/css/styles.css:
Copy-Item -Path "talleria\css\styles.css" -Destination "css\styles.css" -Force
Copy-Item -Path "talleria\producto.html" -Destination "producto.html" -Force
```

## Token-Efficient Editing

**Before reading any file, consult `MAP.md` for line ranges.**

```
grep "class-name" talleria/css/styles.css   # Find line number
MAP.md → check section                        # Confirm context
Read file offset=N limit=30                   # Read ONLY that section
```

**Never read full CSS/HTML/JS files.** Use grep + MAP.md + narrow Read.

## Product Page Layout (16 sections)

1. Hero (hero--apple)
2. Carousel (8 spin images, auto-scroll)
3. Design section
4. Bento Grid (3 feature cards, dark)
5. Lifestyle (stats overlay, dark)
6. Video 1 — GISAM (real painting)
7. Video 2 — CultivoX (metal surface)
8. Specs (5 values grid)
9. Box contents (4 items, dark)
10. Video 3 — DIY ALAM (assembly)
11. Video 4 — Temu (versatility)
12. Why Buy (6 trust cards)
13. Testimonials (3 reviews)
14. Compare table (PaintPro vs brochas)
15. Specs FAQ (3 accordion items)
16. CTA Final + countdown

## Homepage Layout

Brand Hero → Stats → Manifesto → History → Values → Video → Products → Compromiso → Testimonials → Brand CTA → Footer
