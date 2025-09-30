#!/usr/bin/env python3
"""
Sync a local Obsidian vault subfolder into notes/ and pre-render pages.

Usage:
  python3 tools/import_from_vault.py /path/to/mathematical-economics-book

Behavior:
- Copies all Markdown (.md) files from the source into notes/ preserving structure.
- Copies other files (images, PDFs, etc.) into notes/ as well (renderer will copy images it sees to assets/media on build).
- Runs tools/prerender_all.py to generate pages/.
"""
import os, shutil, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / 'notes'

def copy_tree(src: pathlib.Path, dst: pathlib.Path):
    for root, dirs, files in os.walk(src):
        # skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '.git']
        rel = pathlib.Path(root).relative_to(src)
        out_dir = dst / rel
        out_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            if f.startswith('.'):
                continue
            sp = pathlib.Path(root) / f
            dp = out_dir / f
            dp.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(sp, dp)

def main(argv):
    if len(argv) < 2:
        print('Usage: tools/import_from_vault.py <source_folder>')
        return 2
    src = pathlib.Path(argv[1]).resolve()
    if not src.exists():
        print(f'Source not found: {src}')
        return 1
    copy_tree(src, NOTES)
    print(f'Copied {src} -> {NOTES}')
    # Run prerender
    subprocess.check_call([sys.executable, str(ROOT / 'tools' / 'prerender_all.py')])
    return 0

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))

