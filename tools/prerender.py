#!/usr/bin/env python3
import sys, re, html, pathlib

TEMPLATE_KEYS = {
    '{{title}}': 'title',
    '{{content}}': 'content',
}

def md_to_html(md: str) -> str:
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
        s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', s)  # images
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
    content = md_to_html(md)
    html_page = render(template, title, content)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_page, encoding='utf-8')
    print(f'Rendered {src} -> {out}')

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
