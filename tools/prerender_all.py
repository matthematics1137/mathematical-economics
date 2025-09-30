#!/usr/bin/env python3
import pathlib, re, html

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / 'notes'
PAGES = ROOT / 'pages'
TEMPLATE = ROOT / 'templates' / 'section.html'

def inline_html(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', s)
    s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    return s

def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out, para = [], []
    list_stack = []
    bullet_re = re.compile(r'^([ \t]*)([-\*])\s+(.*)$')
    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline_html(' '.join(para).strip()) + '</p>')
            para = []
    def set_list_depth(depth: int):
        while len(list_stack) < depth:
            out.append('<ul>'); list_stack.append('ul')
        while len(list_stack) > depth:
            out.append('</ul>'); list_stack.pop()
    for raw in lines:
        line = raw.rstrip('\n')
        if not line.strip():
            flush_para(); set_list_depth(0); continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_para(); set_list_depth(0)
            level = len(m.group(1)); text = inline_html(m.group(2))
            out.append(f'<h{level}>' + text + f'</h{level}>'); continue
        if re.match(r'^-{3,}\s*$', line):
            flush_para(); set_list_depth(0); out.append('<hr>'); continue
        bm = bullet_re.match(line)
        if bm:
            flush_para()
            indent = bm.group(1).replace('\t', '    ')
            depth = min(6, len(indent)//2)
            set_list_depth(depth+1)
            out.append('<li>' + inline_html(bm.group(3)) + '</li>'); continue
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

def main():
    if not NOTES.exists():
        print('No notes/ directory found; nothing to render.')
        return 0
    count = 0
    for md_path in NOTES.rglob('*.md'):
        rel = md_path.relative_to(NOTES)
        out = (PAGES / rel).with_suffix('.html')
        title_fallback = ' '.join(rel.with_suffix('').parts).replace('-', ' ').title()
        md = md_path.read_text(encoding='utf-8')
        title = extract_title(md, title_fallback)
        # Drop first H1 from body content if present
        md_lines = md.splitlines()
        if md_lines and re.match(r'^#\s+.+', md_lines[0]):
            md_lines = md_lines[1:]
            md = '\n'.join(md_lines)
        html_content = md_to_html(md)
        html_page = render_page(title, html_content)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html_page, encoding='utf-8')
        print(f'Rendered {md_path} -> {out}')
        count += 1
    print(f'Done. Rendered {count} page(s).')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
