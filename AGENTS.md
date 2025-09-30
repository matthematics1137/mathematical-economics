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

Theme & color mode
------------------
- Global theme lives in `assets/css/style.css`, which imports `assets/css/obsidian.css`.
- The site automatically adapts to the visitor’s light/dark preference via `@media (prefers-color-scheme: dark)`.
- Usage on new pages: just link `assets/css/style.css` in the `<head>`; no extra classes or wrappers needed.
- Typography: Share Tech Mono (via Google Fonts) is the base font for a consistent “Obsidian-like” look.

Markdown authoring (optional)
-----------------------------
- You can draft content in Markdown and render it client‑side.
- Include `assets/js/md-render.js` on the page, then either:
  - Inline: place a `<script type="text/markdown" data-target="#some-id">…</script>` and a `<div id="some-id"></div>` where it should render.
  - External: place `<div data-md-src="../../notes/<part>/<file>.md"></div>` and add the `.md` file under `notes/`.
- The renderer uses Marked + DOMPurify from a CDN, and wraps rendered content with `.md-content` so the Obsidian‑style CSS applies only to that block.

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

Editing content
---------------
- Write your notes directly in the HTML under the placeholder comments in each page (e.g., `pages/optimizing-theory/index.html`).
- Images: place under `assets/img/<part>/...` and include with `<img src="../../assets/img/<part>/file.png" alt="...">`.
- If you prefer Markdown while drafting, keep a parallel `.md` file locally and paste rendered content into the HTML; no build step is used here.

Sidebar + page order
--------------------
- The sidebar markup lives in `assets/partials/sidebar.html` and is injected on each page by `assets/js/site-nav.js`.
- To add a new page to the left‑hand navigation, update `assets/partials/sidebar.html` with a link.
- To enable Previous/Next buttons within a section, add the new page’s path to the ordered list in `assets/js/site-nav.js` under the correct section key (e.g., `optimizing-theory`).

Reviews (fourth part)
---------------------
The Mathematical Reviews section may deviate from the above (e.g., denser notes, fewer or no simulations). Maintain the same visual style and navigation.

Roadmap
-------
- Maintain planned topics and checkboxes in `ROADMAP.md`. Keep it up to date as pages are added.
