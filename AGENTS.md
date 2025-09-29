Conventions for This Repository
===============================

Scope: Applies to the entire repository.

Goals
-----
- Keep the site lightweight and dependency‑free (plain HTML/CSS).
- For now, focus on the landing page and structure only (no programs yet).
- Prefer clarity and pedagogy over maximal generality.

Structure
---------
- `index.html` — Landing page organizing the four parts.
- `pages/` — Reserved for future outlines/notes.
- `assets/css/style.css` — Shared styles. Keep inline styles to a minimum.

Page guidelines (first three parts)
----------------------------------
For Optimizing Theory, Static Economic Models, and Dynamic Economic Models, each topic page should follow this outline:

1) Groundwork (text + images)
- 1–3 short sections introducing the concept and notation.
- Use images/diagrams where helpful. Store under `assets/img/<part>/...` with descriptive filenames.
- Keep math concise; use plain HTML where possible. If typesetting is needed later, we can add KaTeX/MathJax as a drop‑in.

2) Small simulations (lightweight)
- 1–2 minimal, self‑contained visuals or interactive snippets (vanilla JS only).
- Keep code inline or as a tiny `<script>` include in `assets/js/<part>/...` when reuse makes sense.
- Aim for clarity over features: a few well‑chosen parameters, immediate feedback, readable defaults.

3) Conclusion (wrap‑up)
- Summarize the key ideas and what to remember.
- Add 2–5 pointers: related chapters/sections, classic references, or exercises to try.

Navigation & UX
---------------
- Include a back link to the landing page at the top (`← Back to Introduction`).
- At the bottom, include simple next/previous links within the part when multiple pages exist.
- Use shared classes from `assets/css/style.css` (`.container`, `.card`, `.buttons`, `.button`, `.back`).

Naming & organization
---------------------
- File names: kebab‑case and grouped by part, e.g., `pages/optimizing-theory/kuhn-tucker.html`.
- Assets: `assets/img/optimizing-theory/...` and optional `assets/js/optimizing-theory/...`.
- Keep each page standalone (no build step). Avoid external dependencies unless clearly justified.

Reviews (fourth part)
---------------------
The Mathematical Reviews section may deviate from the above (e.g., denser notes, fewer or no simulations). Maintain the same visual style and navigation.

Roadmap
-------
- Maintain planned topics and checkboxes in `ROADMAP.md`. Keep it up to date as pages are added.
