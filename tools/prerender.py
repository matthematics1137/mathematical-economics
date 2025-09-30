#!/usr/bin/env python3
import sys, re, html, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / 'notes'
MEDIA = ROOT / 'assets' / 'media'

TEMPLATE_KEYS = {
    '{{title}}': 'title',
    '{{content}}': 'content',
}

def _is_abs_url(u: str) -> bool:
    return bool(re.match(r'^(?:[a-z]+:)?//', u)) or u.startswith('data:') or u.startswith('/')

def md_to_html(md: str, rel_dir: pathlib.Path) -> str:
    lines = md.splitlines()
    out = []
    para = []
    list_stack = []  # track list depth

    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline(' '.join(para).strip()) + '</p>')
            para = []

    def set_list_depth(depth: int):
        # open/close <ul> to reach desired depth
        while len(list_stack) < depth:
            out.append('<ul>')
            list_stack.append('ul')
        while len(list_stack) > depth:
            out.append('</ul>')
            list_stack.pop()

    def inline(s: str) -> str:
        s = html.escape(s)
        def _img_sub(m):
            alt = m.group(1); src = m.group(2)
            if _is_abs_url(src):
                new_src = src
            else:
                src_path = (NOTES / rel_dir / src).resolve()
                dest_path = (MEDIA / rel_dir / src).resolve()
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    if src_path.exists():
                        shutil.copy2(src_path, dest_path)
                except Exception:
                    pass
                depth = len(rel_dir.parts) + 1
                prefix = '../' * depth
                new_src = f"{prefix}assets/media/{rel_dir.as_posix()}/{src}"
            return f'<img src="{new_src}" alt="{alt}">'
        s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', _img_sub, s)  # images
        s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)        # links
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)                                    # code
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)                      # bold
        s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)                     # italics
        return s

    bullet_re = re.compile(r'^([ \t]*)([-\*])\s+(.*)$')

    for raw in lines:
        line = raw.rstrip('\n')
        if not line.strip():
            flush_para(); set_list_depth(0)
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_para(); set_list_depth(0)
            level = len(m.group(1))
            text = inline(m.group(2))
            out.append(f'<h{level}>' + text + f'</h{level}>')
            continue
        if re.match(r'^-{3,}\s*$', line):
            flush_para(); set_list_depth(0)
            out.append('<hr>')
            continue
        bm = bullet_re.match(line)
        if bm:
            flush_para()
            indent = bm.group(1).replace('\t', '    ')
            depth = min(6, len(indent) // 2)  # 2 spaces per level (tabs become 4)
            set_list_depth(depth + 1)
            out.append('<li>' + inline(bm.group(3)) + '</li>')
            continue
        # plain text
        para.append(line)

    flush_para(); set_list_depth(0)
    return '\n'.join(out)

def render(template_path: pathlib.Path, title: str, content_html: str) -> str:
    tpl = template_path.read_text(encoding='utf-8')
    html_out = tpl.replace('{{title}}', title).replace('{{content}}', content_html)
    return html_out

def main(argv):
    if len(argv) < 4:
        print('Usage: tools/prerender.py <input.md> <output.html> <title> [<template.html>]')
        return 2
    src = pathlib.Path(argv[1])
    out = pathlib.Path(argv[2])
    title = argv[3]
    template = pathlib.Path(argv[4]) if len(argv) > 4 else pathlib.Path('templates/section.html')
    md = src.read_text(encoding='utf-8')
    # If first line is an H1, use title and drop that line from body
    lines = md.splitlines()
    if lines and re.match(r'^#\s+.+', lines[0]):
        lines = lines[1:]
        md = '\n'.join(lines)
    # Determine rel_dir relative to notes/
    try:
        rel = src.resolve().relative_to(NOTES)
        rel_dir = rel.parent
    except Exception:
        rel_dir = pathlib.Path('.')
    content = md_to_html(md, rel_dir)
    html_page = render(template, title, content)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_page, encoding='utf-8')
    print(f'Rendered {src} -> {out}')

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
