Mathematical Economics — Interactive Notes and Simulations
=========================================================

Interactive visualizations and notes inspired by Kelvin (Kevin) Lancaster’s Mathematical Economics and adjacent texts. The goal is to make core concepts in micro, macro, and optimization more concrete through small, self‑contained pages you can explore in the browser.

Repo layout
-----------
- `index.html` — Landing page linking to topics
- `pages/` — Individual topic pages (each is a standalone HTML file)
- `assets/css/style.css` — Shared, lightweight styles used by all pages
- `AGENTS.md` — Working conventions and tips for contributors
- `ROADMAP.md` — Planned topics and progress checklist

Local preview
-------------
You can open `index.html` directly in a browser, or serve the folder locally:

- Python: `python3 -m http.server -d . 8080`
- Node: `npx serve .`

Deploy (GitHub Pages)
---------------------
This repo is static; GitHub Pages can serve it directly from the default branch:

1. Push to GitHub.
2. In repository Settings → Pages, set Source to `Deploy from a branch`, pick `main` and `/ (root)`.
3. Wait for the site to publish; the URL will appear in the Pages settings.

Credits and influence
---------------------
- Inspired by Kelvin Lancaster’s work on consumer theory and demand systems.
- Heavily influenced by the clean, dependency‑free structure used in a sibling repo (`chaos/`).

