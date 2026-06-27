#!/usr/bin/env python3
"""Fix known broken relative-path wiki-links found by final_verify."""
import os
import re
from path_utils import BASE, walk_markdown

FIXES = {
    # file_contains_old_path -> new_path (relative to source file's directory)
    '02_NaturalSciences/Biology/CellBiology/Cryobiology.md': [
        ('../CellBiology', '../CellBiology/INDEX'),
    ],
    '02_NaturalSciences/Chemistry/PhysicalChemistry/AppliedChemistry.md': [
        ('../../PhysicalChemistry', '../INDEX'),
        ('../OrganicChemistry/OrganicChemistry', '../OrganicChemistry/INDEX'),
    ],
    '02_NaturalSciences/Chemistry/PhysicalChemistry/ColloidChemistry.md': [
        ('../PhysicalChemistry', '../INDEX'),
    ],
    '02_NaturalSciences/Chemistry/PhysicalChemistry/TheoreticalChemistry.md': [
        ('../PhysicalChemistry', '../INDEX'),
    ],
    '03_HumanitiesAndSocialSciences/Linguistics/AppliedLinguistics.md': [
        ('../ForeignLanguagesAndLiteratures/TranslationStudies',
         '../ForeignLanguagesAndLiteratures/TranslationStudies/INDEX'),
    ],
}

def fix_file(rel_path, replacements):
    fpath = os.path.join(BASE, rel_path.replace('/', '\\'))
    if not os.path.exists(fpath):
        print(f'  [SKIP] {rel_path} not found')
        return
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    for old, new in replacements:
        # Match [[old]] or [[old|display]] patterns
        pattern = re.compile(r'\[\[\s*' + re.escape(old) + r'\s*(?:[|#][^\]]*)?\]\]')
        def replacer(m):
            link = m.group(0)
            has_display = '|' in link
            has_anchor = '#' in link and not has_display
            if has_display:
                parts = link[2:-2].split('|', 1)
                display = parts[1]
                return f'[[{new}|{display}]]'
            elif has_anchor:
                parts = link[2:-2].split('#', 1)
                anchor = parts[1]
                return f'[[{new}#{anchor}]]'
            else:
                return f'[[{new}]]'
        content = pattern.sub(replacer, content)
    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  [FIXED] {rel_path}')
    else:
        print(f'  [NO CHANGE] {rel_path}')

def main():
    print('Fixing known broken relative-path wiki-links...')
    for rel_path, replacements in FIXES.items():
        fix_file(rel_path, replacements)
    print('Done!')

if __name__ == '__main__':
    main()
