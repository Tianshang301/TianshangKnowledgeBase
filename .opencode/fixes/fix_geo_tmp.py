#!/usr/bin/env python3
import os
from path_utils import find_project_root

ROOT = find_project_root()
BASE = os.path.join(ROOT, '02_NaturalSciences/EarthSciences/PhysicalGeography')

# Find files with garbled names (non-standard chars)
for f in os.listdir(BASE):
    old = os.path.join(BASE, f)
    if not f.endswith('.md') or f == 'INDEX.md':
        continue
    
    # Read first line to determine topic
    with open(old, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # Remove U+FFFD from content
    original = content
    content = content.replace('\ufffd', '')
    
    # Determine correct topic name from content + context
    # Check for keywords in content to identify topic
    has_fffd = '\ufffd' in original
    topic = f.replace('.md', '')
    
    # Fix frontmatter alias
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('aliases:') and has_fffd:
            lines[i] = f'aliases: [{topic}]'
            break
    content = '\n'.join(lines)
    
    if content != '\ufffd' not in original:
        with open(old, 'w', encoding='utf-8') as fh:
            fh.write(content)
    
    print(f'File: topic={topic}, had_fffd={has_fffd}')
