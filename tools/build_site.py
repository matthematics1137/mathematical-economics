#!/usr/bin/env python3
import pathlib, re, html, json, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOK = ROOT / 'mathematical-economics' / 'mathematical-economics-book'
PAGES = ROOT / 'pages'
PARTIALS = ROOT / 'assets' / 'partials'
TEMPLATE = ROOT / 'templates' / 'section.html'

ASSET_BASE = '/mathematical-economics'

def slugify(s: str) -> str:
    s = s.strip().lower()
    # replace non-alnum with hyphen
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-')
    return s or 'index'

def title_from_name(name: str) -> str:
    name = re.sub(r'^[0-9_.-]+', '', name)  # drop numeric prefixes if any
    name = name.replace('-', ' ').replace('_',' ').strip()
    return ' '.join(w.capitalize() for w in name.split())

def _is_abs_url(u: str) -> bool:
    return bool(re.match(r'^(?:[a-z]+:)?//', u)) or u.startswith('data:') or u.startswith('/')

def inline_html(s: str, rel_dir: pathlib.Path, src_root: pathlib.Path) -> str:
    s = html.escape(s)
    # images ![alt](src)
    def _img_sub(m):
        alt = m.group(1); src = m.group(2)
        if _is_abs_url(src):
            new_src = src
        else:
            src_path = (src_root / rel_dir / src).resolve()
            dest_path = (ROOT / 'assets' / 'media' / rel_dir / src).resolve()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if src_path.exists():
                    dest_path.write_bytes(src_path.read_bytes())
            except Exception:
                pass
            new_src = f"{ASSET_BASE}/assets/media/{rel_dir.as_posix()}/{src}"
        return f'<img src="{new_src}" alt="{alt}">'
    s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', _img_sub, s)
    # links [text](url)
    s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)
    # code `...`
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    # bold/italics
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

def md_to_html(md: str, rel_dir: pathlib.Path, src_root: pathlib.Path) -> str:
    lines = md.splitlines()
    out, para = [], []
    list_stack = []
    bullet_re = re.compile(r'^([ \t]*)([-\*])\s+(.*)$')
    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline_html(' '.join(para).strip(), rel_dir, src_root) + '</p>')
            para = []
    def set_list_depth(depth: int):
        while len(list_stack) < depth:
            out.append('<ul>'); list_stack.append('ul')
        while len(list_stack) > depth:
            out.append('</ul>'); list_stack.pop()
    for raw in lines:
        line = raw.rstrip('\n')
        if line.lstrip().startswith('<'):
            flush_para(); set_list_depth(0); out.append(line); continue
        if not line.strip():
            flush_para(); set_list_depth(0); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_para(); set_list_depth(0)
            level = len(m.group(1)); text = inline_html(m.group(2), rel_dir, src_root)
            out.append(f'<h{level}>' + text + f'</h{level}>'); continue
        if re.match(r'^-{3,}\s*$', line):
            flush_para(); set_list_depth(0); out.append('<hr>'); continue
        bm = bullet_re.match(line)
        if bm:
            flush_para()
            indent = bm.group(1).replace('\t', '    ')
            depth = min(6, len(indent)//2)
            set_list_depth(depth+1)
            out.append('<li>' + inline_html(bm.group(3), rel_dir, src_root) + '</li>'); continue
        para.append(line)
    flush_para(); set_list_depth(0)
    return '\n'.join(out)

def extract_title(md: str, fallback: str) -> str:
    for line in md.splitlines():
        m = re.match(r'^#\s+(.*)$', line)
        if m:
            return m.group(1).strip()
    return fallback

def render_page(title: str, content_html: str) -> str:
    tpl = TEMPLATE.read_text(encoding='utf-8')
    return tpl.replace('{{title}}', title).replace('{{content}}', content_html)

def build_manifest():
    sections = {}
    for md_path in BOOK.rglob('*.md'):
        rel = md_path.relative_to(BOOK)
        parts = list(rel.parts)
        if len(parts) == 0:
            continue
        section_key = parts[0]
        sections.setdefault(section_key, []).append(md_path)
    # sort each section's pages by path
    for k in sections:
        sections[k] = sorted(sections[k])
    return sections

def main():
    if not BOOK.exists():
        print('Book directory not found:', BOOK)
        return 1
    # Clean pages output for a fresh build
    if PAGES.exists():
        shutil.rmtree(PAGES)
    PAGES.mkdir(parents=True, exist_ok=True)

    manifest = []
    sections = build_manifest()
    for sect_label, files in sections.items():
        sect_slug = slugify(sect_label)
        sect_out_dir = PAGES / sect_slug
        sect_out_dir.mkdir(parents=True, exist_ok=True)
        sect_entry = { 'label': sect_label, 'slug': sect_slug, 'pages': [] }
        for md_path in files:
            rel = md_path.relative_to(BOOK)
            # Build slugged output path mirroring directories; stem for filename
            out_dirs = [slugify(p) for p in rel.parts[:-1]]
            name_slug = slugify(md_path.stem)
            out_html = PAGES.joinpath(*(out_dirs + [name_slug + '.html']))
            out_html.parent.mkdir(parents=True, exist_ok=True)
            md = md_path.read_text(encoding='utf-8')
            title = extract_title(md, title_from_name(md_path.stem))
            # Drop first H1
            md_lines = md.splitlines()
            if md_lines and re.match(r'^#\s+.+', md_lines[0]):
                md_lines = md_lines[1:]
                md = '\n'.join(md_lines)
            rel_dir = rel.parent
            content = md_to_html(md, rel_dir, BOOK)
            html_page = render_page(title, content)
            out_html.write_text(html_page, encoding='utf-8')
            url_path = f"/pages/{'/'.join(out_dirs + [name_slug + '.html'])}"
            sect_entry['pages'].append({ 'title': title, 'path': url_path })
            print(f'Rendered {md_path} -> {out_html}')
        manifest.append(sect_entry)

    # Write a small manifest for client-side use if needed
    (ROOT / 'assets').mkdir(exist_ok=True)
    (ROOT / 'assets' / 'site.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

    # Generate sidebar from manifest
    PARTIALS.mkdir(parents=True, exist_ok=True)
    sidebar = ['<div class="card">', '  <nav>', f'    <a href="{ASSET_BASE}/index.html" data-match="/index.html">Home</a>', '    <hr style="border:none;border-top:1px solid var(--border);margin:8px 0;">', '    <strong style="display:block;padding:4px 10px;color:var(--muted)">Sections</strong>']
    for sect in manifest:
        first = sect['pages'][0]['path'] if sect['pages'] else f"/pages/{sect['slug']}/"
        sidebar.append(f'    <a href="{ASSET_BASE}{first}" data-match="/pages/{sect["slug"]}/">{html.escape(sect["label"])}</a>')
    sidebar += ['  </nav>', '</div>']
    (PARTIALS / 'sidebar.html').write_text('\n'.join(sidebar), encoding='utf-8')

    # Generate index.html dynamically with section cards
    cards = []
    for sect in manifest:
        link = f'{ASSET_BASE}{sect["pages"][0]["path"]}' if sect['pages'] else f'{ASSET_BASE}/index.html'
        title = html.escape(sect['label'])
        cards.append(f'''    <div class="card">
      <h3>{title}</h3>
      <div class="buttons">
        <a href="{link}" class="button">Open Section</a>
      </div>
    </div>''')
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <script>
    (function(){{
      try {{ var m = localStorage.getItem('theme'); if (m === 'light' || m === 'dark') document.documentElement.setAttribute('data-theme', m); }} catch (e) {{}}
    }})();
  </script>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mathematical Economics</title>
  <link rel="stylesheet" href="{ASSET_BASE}/assets/css/style.css?v=20250930" />
  <script defer src="{ASSET_BASE}/assets/js/site-nav.js?v=20250930"></script>
</head>
<body>
  <button id="navToggle" class="hamburger" aria-label="Toggle navigation" aria-expanded="false">≡</button>
  <button id="themeToggle" class="theme-toggle" aria-label="Toggle theme" title="Toggle light/dark">◎</button>
  <div class="font-slider" aria-label="Font size">
    <input id="fontSize" type="range" min="90" max="220" step="5" />
  </div>
  <div id="backdrop" class="backdrop" hidden></div>
  <div class="layout">
    <aside id="sidebar" class="sidebar"></aside>
    <main class="content">
  <div class="container">
    <h1>Mathematical Economics</h1>
    <p class="tagline">Sections generated from the in-repo book.</p>

{chr(10).join(cards)}

  </div>
    </main>
  </div>
</body>
</html>
'''
    (ROOT / 'index.html').write_text(index_html, encoding='utf-8')

    print('Done. Built site from book and updated index + sidebar.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
