Conventions for This Repository
===============================

Scope: Applies to the entire repository.

Goals
-----
- Keep pages lightweight and dependency‑free (plain HTML/CSS/vanilla JS if needed).
- Keep a consistent look and feel across all topic pages.
- Prefer clarity and pedagogy over maximal generality.

Structure
---------
- `index.html` — Landing page with short intro and buttons to topics.
- `pages/` — One HTML file per topic (e.g., `edgeworth_box.html`).
- `assets/css/style.css` — Shared styles. Keep inline styles to a minimum.
- Optional: Each page may include a small inline `<script>` for interactivity.

Page guidelines
---------------
- Use the shared stylesheet and the common container classes (`.container`, `.buttons`, `.button`, `.back`).
- Start with a brief 1–2 paragraph description of the concept and what the page demonstrates.
- If a page has multiple views, use tab‑like buttons to switch between `.panel` sections.
- Keep any math simple and inline; link to references for deeper math.

Roadmap
-------
- Maintain planned topics and checkboxes in `ROADMAP.md`. Keep it up to date as pages are added.

