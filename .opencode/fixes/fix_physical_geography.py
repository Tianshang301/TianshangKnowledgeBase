#!/usr/bin/env python3
"""Fix garbled files in PhysicalGeography directory."""
import os
import shutil
from path_utils import find_project_root

ROOT = find_project_root()
BASE = os.path.join(ROOT, '02_NaturalSciences/EarthSciences/PhysicalGeography')

for f in os.listdir(BASE):
    if not f.endswith('.md') or f == 'INDEX.md':
        continue
    old_path = os.path.join(BASE, f)
    
    # Read content
    with open(old_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    has_fffd = '\ufffd' in content
    print(f'{repr(f)}: FFFD={has_fffd}, size={len(content)}')
    
    if has_fffd:
        # Remove U+FFFD
        content = content.replace('\ufffd', '')
        
        # Fix frontmatter
        lines = content.split('\n')
        for i, line in enumerate(lines[:10]):
            if line.startswith('aliases:'):
                lines[i] = f'aliases: [{os.path.splitext(f)[0]}]'
                break
        content = '\n'.join(lines)
        
        with open(old_path, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'  -> Fixed content in {f}')

# Fix filename: the garbled name should be 土壤地理学
for f in os.listdir(BASE):
    if not f.endswith('.md') or f == 'INDEX.md':
        continue
    old_path = os.path.join(BASE, f)
    
    # Try to determine correct name from content
    with open(old_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Check for title
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2:].strip()
            # Skip if title is also garbled
            if any(ord(c) > 127 for c in title) and not any(ord(c) < 32 for c in title):
                new_name = title + '.md'
                new_path = os.path.join(BASE, new_name)
                if old_path != new_path and not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    print(f'Renamed: {repr(f)} -> {new_name}')
            break

print('\nDone!')
