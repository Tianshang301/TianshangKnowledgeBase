#!/usr/bin/env python3
"""Recreate geography files with correct names and content."""
import os
import shutil
from path_utils import find_project_root

ROOT = find_project_root()
BASE = os.path.join(ROOT, '02_NaturalSciences/EarthSciences/PhysicalGeography')

# Read existing content from garbled files
file_data = {}
for f in os.listdir(BASE):
    if not f.endswith('.md') or f == 'INDEX.md':
        continue
    path = os.path.join(BASE, f)
    with open(path, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Clean content
    content = content.replace('\ufffd', '')
    
    # Determine correct topic name
    topic = None
    for line in content.split('\n'):
        if line.startswith('# '):
            title = line[2].strip().rstrip('?')
            if title:
                topic = title
            break
    
    # Try to identify by content keywords
    if topic and ('土壤' in content or 'Pedology' in content or 'Soil' in content):
        topic = '土壤地理学'
    elif topic and ('地貌' in content or 'Geomorphology' in content):
        topic = '地貌学'
    elif topic and ('水文' in content or 'Hydrogeography' in content):
        topic = '水文地理学'
    
    if topic:
        file_data[topic] = (content, path, f)

# Create files with proper Chinese filenames
for topic, (content, old_path, old_name) in file_data.items():
    new_name = topic + '.md'
    new_path = os.path.join(BASE, new_name)
    
    # Fix title in content
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('# '):
            lines[i] = f'# {topic}'
            break
    
    # Fix alias in frontmatter
    for i, line in enumerate(lines):
        if line.startswith('aliases:'):
            lines[i] = f'aliases: [{topic}]'
            break
    
    content = '\n'.join(lines)
    
    # Write to new filename
    with open(new_path, 'w', encoding='utf-8') as fh:
        fh.write(content)
    
    # Remove old file if different
    if old_path != new_path:
        os.remove(old_path)
        print(f'Recreated: {new_name}')
    else:
        print(f'Updated: {new_name}')

# Final listing
print('\nFinal files:')
for f in sorted(os.listdir(BASE)):
    print(f'  {f}')
