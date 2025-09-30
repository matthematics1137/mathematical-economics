Reusable GitHub Pages Builder for Obsidian Notes
===============================================

This folder contains a portable build script you can reuse across repos to
render any Obsidian directory (or subdirectory) into a static site suitable
for GitHub Pages.

Features
- Slugified URLs (no spaces/parentheses) mirroring the folder structure
- Titles derived from filenames (supports numeric prefixes like `1.1.2 ...`)
- Auto‑generated sidebar and Prev/Next from a manifest (`assets/site.json`)
- Index landing page with per‑section cards
- Copies referenced images to `assets/media/...`
- Repo‑absolute asset URLs so CSS/JS load at any depth

Quick Start (in this repo)
- Build using the in‑repo book:
  - python3 build-pages/build.py --book mathematical-economics/mathematical-economics-book --asset-base /mathematical-economics

Adapting for another repo
1) Ensure you have a minimal asset skeleton:
   - `assets/css/style.css`
   - `assets/js/site-nav.js` (uses `assets/site.json` and `assets/partials/sidebar.html`)
   - `assets/js/math.js` (optional; can be a no‑op if you don’t use math)
2) Run the builder:
   - python3 build-pages/build.py --book <path/to/obsidian/dir> --asset-base /<repo-name>
3) Serve on GitHub Pages. The script writes:
   - `pages/` generated HTML
   - `assets/partials/sidebar.html` for the shared nav
   - `assets/site.json` for Prev/Next
   - `index.html` landing page

Notes
- `--asset-base` should be `/<repo-name>` for user/org Pages (not custom domains).
- You can pass a custom template via `--template`. The default template in
  `build-pages/templates/section.html` uses `{{asset_base}}` placeholders and
  will be filled automatically.

