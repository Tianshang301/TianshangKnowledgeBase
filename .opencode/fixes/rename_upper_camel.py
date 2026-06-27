#!/usr/bin/env python3
"""
Rename English-named files to UpperCamelCase and update all references.
"""
import os
import re
import shutil
from path_utils import BASE, SKIP_DIRS, walk_markdown

# Build mapping: old_name -> new_name (for English filenames needing change)
rename_map = {}

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        if f in ('INDEX.md', 'README.md', 'LearningPath.md', '404.md'):
            continue
        name = f[:-3]
        # Only ASCII names
        if not all(ord(c) < 128 for c in name):
            continue
        # Check if follows UpperCamelCase
        if re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
            continue
        
        new_name = name
        # Remove underscores and double capitals
        new_name = new_name.replace('_', '')
        new_name = new_name.replace('-', '')
        # Fix leading lowercase
        if new_name and new_name[0].islower():
            new_name = new_name[0].upper() + new_name[1:]
        # Fix trailing _INDEX, _Basics etc that may have been joined
        new_name = re.sub(r'INDEX$', 'Index', new_name)
        new_name = re.sub(r'Basics$', 'Basics', new_name)
        new_name = re.sub(r'Overview$', 'Overview', new_name)
        new_name = re.sub(r'Advanced$', 'Advanced', new_name)
        new_name = re.sub(r'Intro$', 'Intro', new_name)
        new_name = re.sub(r'Deep$', 'Deep', new_name)
        
        if new_name != name:
            old_path = os.path.join(root, f)
            new_path = os.path.join(root, new_name + '.md')
            if not os.path.exists(new_path):
                rename_map[(old_path, f)] = (name, new_name, os.path.relpath(old_path, BASE).replace('\\', '/'))

print(f'Files to rename: {len(rename_map)}')

# Phase 1: Update all wiki-links in all files before renaming
print('\nPhase 1: Updating wiki-links...')
link_changes = 0
for root, dirs, files in os.walk(BASE):
    if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
        continue
    for f in files:
        if not f.endswith('.md'):
            continue
        fpath = os.path.join(root, f)
        try:
            with open(fpath, 'r', encoding='utf-8') as fh:
                content = fh.read()
        except:
            continue
        
        new_content = content
        for (old_path, orig_fname), (old_name, new_name, rel) in rename_map.items():
            # Replace [[old_name]] with [[new_name]]
            new_content = new_content.replace(f'[[{old_name}]]', f'[[{new_name}]]')
            # Replace [[old_name|text]] with [[new_name|text]]
            new_content = re.sub(
                r'\[' + re.escape(old_name) + r'(\|[^\]]*)\]',
                r'[' + new_name + r'\1]',
                new_content
            )
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            link_changes += 1

print(f'  Files with updated links: {link_changes}')

# Phase 2: Rename files
print('\nPhase 2: Renaming files...')
for (old_path, orig_fname), (old_name, new_name, rel) in rename_map.items():
    new_path = os.path.join(os.path.dirname(old_path), new_name + '.md')
    
    # Read file and update its own frontmatter
    with open(old_path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Update alias in frontmatter if present
    if content.startswith('---'):
        end_idx = content.find('---', 3)
        if end_idx > 0:
            header = content[3:end_idx]
            if f'aliases: [{old_name}]' in header:
                header = header.replace(f'aliases: [{old_name}]', f'aliases: [{new_name}]')
            elif f'aliases: [{old_name}' in header:
                header = re.sub(r'aliases: \[' + re.escape(old_name), f'aliases: [{new_name}', header)
            content = '---\n' + header.strip() + '\n---\n' + content[end_idx+3:]
    
    with open(new_path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    
    # Remove old file
    os.remove(old_path)
    print(f'  {old_name}.md -> {new_name}.md')

print(f'\nDone! {len(rename_map)} files renamed, {link_changes} files with updated links.')
