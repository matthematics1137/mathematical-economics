#!/usr/bin/env python3
import pathlib, re, html, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAGES = ROOT / 'pages'
TEMPLATE = ROOT / 'templates' / 'section.html'
MEDIA = ROOT / 'assets' / 'media'

def _is_abs_url(u: str) -> bool:
    return bool(re.match(r'^(?:[a-z]+:)?//', u)) or u.startswith('data:') or u.startswith('/')

def inline_html(s: str, rel_dir: pathlib.Path, src_root: pathlib.Path) -> str:
    s = html.escape(s)
    def _img_sub(m):
        alt = m.group(1); src = m.group(2)
        if _is_abs_url(src):
            new_src = src
        else:
            src_path = (src_root / rel_dir / src).resolve()
            dest_path = (MEDIA / rel_dir / src).resolve()
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                if src_path.exists():
                    dest_path.write_bytes(src_path.read_bytes())
            except Exception:
                pass
            depth = len(rel_dir.parts) + 1
            prefix = '../' * depth
            new_src = f"{prefix}assets/media/{rel_dir.as_posix()}/{src}"
        return f'<img src="{new_src}" alt="{alt}">'
    s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', _img_sub, s)
    s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
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

def main(argv):
    if len(argv) < 2:
        print('Usage: tools/prerender_from.py <source_markdown_root>')
        return 2
    src_root = pathlib.Path(argv[1]).resolve()
    if not src_root.exists():
        print(f'Source not found: {src_root}')
        return 1
    count = 0
    for md_path in src_root.rglob('*.md'):
        rel = md_path.relative_to(src_root)
        out = (PAGES / rel).with_suffix('.html')
        title_fallback = ' '.join(rel.with_suffix('').parts).replace('-', ' ').title()
        md = md_path.read_text(encoding='utf-8')
        title = extract_title(md, title_fallback)
        md_lines = md.splitlines()
        if md_lines and re.match(r'^#\s+.+', md_lines[0]):
            md_lines = md_lines[1:]
            md = '\n'.join(md_lines)
        rel_dir = rel.parent
        html_content = md_to_html(md, rel_dir, src_root)
        html_page = render_page(title, html_content)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_page, encoding='utf-8')
        print(f'Rendered {md_path} -> {out}')
        count += 1
    print(f'Done. Rendered {count} page(s).')
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

