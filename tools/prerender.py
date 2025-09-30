#!/usr/bin/env python3
import sys, re, html, pathlib

TEMPLATE_KEYS = {
    '{{title}}': 'title',
    '{{content}}': 'content',
}

def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    in_list = False
    para = []

    def flush_para():
        nonlocal para
        if para:
            out.append('<p>' + inline(' '.join(para).strip()) + '</p>')
            para = []

    def start_list():
        nonlocal in_list
        if not in_list:
            out.append('<ul>')
            in_list = True

    def end_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def inline(s: str) -> str:
        s = html.escape(s)
        # images ![alt](src)
        s = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'<img src="\2" alt="\1">', s)
        # links [text](url)
        s = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', s)
        # code `...`
        s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
        # bold **...**
        s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
        # italics *...*
        s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
        return s

    for raw in lines:
        line = raw.rstrip('\n')
        if not line.strip():
            flush_para()
            end_list()
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            flush_para(); end_list()
            level = len(m.group(1))
            text = inline(m.group(2))
            out.append(f'<h{level}>' + text + f'</h{level}>')
            continue
        if re.match(r'^-{3,}\s*$', line):
            flush_para(); end_list()
            out.append('<hr>')
            continue
        m = re.match(r'^(?:- |\* )\s*(.*)$', line)
        if m:
            flush_para(); start_list()
            out.append('<li>' + inline(m.group(1)) + '</li>')
            continue
        para.append(line)

    flush_para(); end_list()
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
    content = md_to_html(md)
    html_page = render(template, title, content)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_page, encoding='utf-8')
    print(f'Rendered {src} -> {out}')

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

