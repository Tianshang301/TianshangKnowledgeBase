#!/usr/bin/env python3
"""Final verification: correctly resolve path-based wiki-links per Obsidian rules."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build all existing files (set of absolute paths)
existing = set()
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if f.endswith('.md'):
            existing.add(os.path.normpath(os.path.join(root, f)))

# Obsidian resolution rules:
# [[relative/path]] -> resolved from source file's directory
# [[/absolute/path]] -> resolved from vault root
# [[vaultroot/path]] -> resolved from vault root (if no leading dot)
# [[file]] -> first: source dir; second: vault root

truly_broken = []
relative_from_root = []

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.normpath(os.path.join(root, f))
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        
        for m in re.finditer(r'\[\[([^\]]+?)\]\]', content):
            raw = m.group(1).strip()
            target = raw.split('|')[0].split('#')[0].strip()
            if not target or target in ('INDEX', 'LearningPath', 'README', '404'):
                continue
            
            # Skip simple names (already handled by previous fix)
            if '/' not in target and '\\' not in target:
                continue
            
            # Resolution rule 1: starts with . -> relative to source dir
            if target.startswith('.'):
                resolved = os.path.normpath(os.path.join(os.path.dirname(fpath), target))
                if not resolved.endswith('.md'):
                    resolved += '.md'
                if resolved not in existing:
                    truly_broken.append((target, fpath, resolved))
            else:
                # Resolution rule 2: no leading dot -> from VAULT ROOT
                resolved = os.path.normpath(os.path.join(BASE, target))
                if not resolved.endswith('.md'):
                    resolved += '.md'
                if resolved not in existing:
                    relative_from_root.append((target, fpath, resolved))

print(f'Truly broken relative links (path starting with .): {len(truly_broken)}')
if truly_broken:
    for t, src, resolved in truly_broken[:20]:
        rel_src = os.path.relpath(src, BASE).replace('\\', '/')
        rel_res = os.path.relpath(resolved, BASE).replace('\\', '/')
        print(f'  {t}')
        print(f'    in:    {rel_src}')
        print(f'    wants: {rel_res}')
        print()

print(f'\nVault-root relative links (path starting with name): {len(relative_from_root)}')
if relative_from_root:
    for t, src, resolved in relative_from_root[:20]:
        rel_src = os.path.relpath(src, BASE).replace('\\', '/')
        rel_res = os.path.relpath(resolved, BASE).replace('\\', '/')
        print(f'  {t}')
        print(f'    in:    {rel_src}')
        print(f'    wants: {rel_res}')
        print()
