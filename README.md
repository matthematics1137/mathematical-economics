Mathematical Economics — Interactive Notes and Simulations
=========================================================

[![Website](https://img.shields.io/website?url=https%3A%2F%2Fmatthematics1137.github.io%2Fmathematical-economics%2F)](https://matthematics1137.github.io/mathematical-economics/)
[![Last Commit](https://img.shields.io/github/last-commit/matthematics1137/mathematical-economics)](https://github.com/matthematics1137/mathematical-economics/commits/main)
[![Repo Size](https://img.shields.io/github/repo-size/matthematics1137/mathematical-economics)](https://github.com/matthematics1137/mathematical-economics)

Concise, dependency‑free study notes inspired by Kevin Lancaster’s Mathematical Economics and adjacent texts. We are intentionally not rushing into simulations; the initial focus is clear structure and outlines we’ll expand together.

Highlights
----------
- Clean, static site — no frameworks, just HTML/CSS/JS
- Clean typographic layout; accessible defaults
- Consistent styling; lightweight code and assets
- Clear progression we will build on together

Scope
-----
- Live site: https://matthematics1137.github.io/mathematical-economics/
- Four parts (landing page only for now):
  1) Optimizing Theory
  2) Static Economic Models
  3) Dynamic Economic Models
  4) Mathematical Reviews

Structure
---------
- `index.html` — Landing page linking to topics
- `pages/` — Generated HTML pages (do not edit by hand)
- `assets/css/style.css` — Shared, lightweight styles used by all pages
- `AGENTS.md` — Working conventions and code style
- `ROADMAP.md` — Planned topics and status

Working with Obsidian (in‑repo vault)
------------------------------------
- Point Obsidian at this repository folder as a vault.
- Write notes under `notes/<section>/<page>.md` using H1 at top for the title.
- Build pages locally: `make build` (renders Markdown from `notes/` into `pages/`).
- Commit and push; GitHub Pages serves the generated HTML.
- For now, avoid raw `<div data-widget=...>` placeholders while drafting. We will inject visualizations later.

Roadmap
-------
Planned enhancements and upcoming topics are tracked in `ROADMAP.md`.

Acknowledgments
---------------
- Influenced by the clean, dependency‑free structure used in the sibling `chaos/` repository.
- Inspired by the pedagogy of Kevin Lancaster and the broader mathematical‑economics literature.
