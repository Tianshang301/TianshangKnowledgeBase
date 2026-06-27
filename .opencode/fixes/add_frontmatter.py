#!/usr/bin/env python3
"""Batch add YAML frontmatter (aliases + tags) to all .md files that lack it."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

total = 0
added = 0
skipped_has_fm = 0
errors = 0
stubs_added = 0

def derive_tags(path_parts):
    """Derive Obsidian tags from file path, excluding the root level."""
    tags = []
    for p in path_parts:
        if p and p != path_parts[0]:  # Skip root level (00_XX)
            tags.append(p)
    return tags

for root, dirs, files in os.walk(BASE):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    
    for f in files:
        if not f.endswith('.md'):
            continue
        
        fpath = os.path.join(root, f)
        rel = os.path.relpath(fpath, BASE).replace('\\', '/')
        total += 1
        
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except Exception as e:
            errors += 1
            print(f'[ERROR] reading {rel}: {e}')
            continue
        
        # Skip if already has frontmatter
        if content.startswith('---'):
            skipped_has_fm += 1
            continue
        
        # Derive filename (without extension) as alias
        name_no_ext = f[:-3]
        alias = name_no_ext
        
        # Derive tags from path
        path_parts = rel.split('/')
        tags = derive_tags(path_parts)
        
        # Handle _Stubs/
        is_stub = '_Stubs/' in rel
        if is_stub:
            tags = ['_Stubs', name_no_ext]
        
        # Build tag string
        tag_str = ', '.join([f"'{t}'" for t in tags]) if tags else "'untagged'"
        
        # Build frontmatter
        frontmatter = '---\n'
        frontmatter += f'aliases: [{alias}]\n'
        frontmatter += f'tags: [{tag_str}]\n'
        frontmatter += '---\n\n'
        
        # Write
        new_content = frontmatter + content.lstrip('\ufeff')  # Remove BOM if present
        try:
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
        except Exception as e:
            errors += 1
            print(f'[ERROR] writing {rel}: {e}')
            continue
        
        if is_stub:
            stubs_added += 1
        added += 1
        
        if added % 200 == 0:
            print(f'  Progress: {added} files...')

print()
print('=== Results ===')
print(f'Total .md files scanned: {total}')
print(f'Already had frontmatter: {skipped_has_fm}')
print(f'Frontmatter ADDED: {added}')
print(f'  (of which _Stubs/: {stubs_added})')
print(f'Errors: {errors}')
