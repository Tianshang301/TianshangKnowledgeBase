#!/usr/bin/env python3
"""Fix the final 47 broken wiki-links."""
import os
import re
from path_utils import BASE, SKIP_DIRS, walk_markdown

# --- Fix 1: Vault-root links that were affected by file renames ---
rename_fixes = {
    'ExamPreparation/Gaokao_Guide': '01_K12/ExamPreparation/GaokaoGuide',
    'ExamPreparation/Zhongkao_Guide': '01_K12/ExamPreparation/ZhongkaoGuide',
    '01_Physics/Thermodynamics/Thermodynamics_Laws': '02_NaturalSciences/Physics/Thermodynamics/ThermodynamicsOverview',
    '01_Physics/Thermodynamics/Entropy': '02_NaturalSciences/Physics/Thermodynamics/Entropy',
    'Basics/CLI_vs_GUI': '05_ComputerScience/Basics/CLIvsGUI',
    'DatabasesAndInformationSystems/MongoDB_Deep': '05_ComputerScience/DatabasesAndInformationSystems/MongoDBDeep',
    'DatabasesAndInformationSystems/MySQL_Deep': '05_ComputerScience/DatabasesAndInformationSystems/MySQLDeep',
    'DatabasesAndInformationSystems/PostgreSQL_Deep': '05_ComputerScience/DatabasesAndInformationSystems/PostgreSQLDeep',
    'DatabasesAndInformationSystems/Redis_Deep': '05_ComputerScience/DatabasesAndInformationSystems/RedisDeep',
    'DatabasesAndInformationSystems/SQL_Deep': '05_ComputerScience/DatabasesAndInformationSystems/SQLDeep',
    'DataStructuresAndAlgorithms/Algorithms/BFS_DFS': '05_ComputerScience/DataStructuresAndAlgorithms/Algorithms/BFSDFS',
    'HardwareAndEmbeddedSystems/Microcontrollers/51_MCU/INDEX': '05_ComputerScience/HardwareAndEmbeddedSystems/Microcontrollers/MCU51/INDEX',
}

# --- Fix 2: Relative path corrections ---
# Format: (source_file_substring, old_link_pattern, new_correct_path)
relative_fixes = {
    # PhysicalGeography/INDEX.md links to ../History and ../Anthropology - WRONG, fix to EarthSciences siblings
    ('PhysicalGeography/INDEX', '../History/INDEX', '../EarthSciences/History/INDEX'),
    ('PhysicalGeography/INDEX', '../Anthropology/INDEX', '../EarthSciences/Anthropology/INDEX'),
    
    # Linguistics/INDEX.md links to ../Psychology/Cognitive - WRONG depth
    ('Linguistics/INDEX', '../Psychology/Cognitive/INDEX', '../../Psychology/Cognitive/INDEX'),
    
    # ChinesePhilosophy/INDEX and Eastern/INDEX link to ../Western - WRONG
    ('ChinesePhilosophy/INDEX', '../Western/INDEX', '../../WesternPhilosophy/Western/INDEX'),
    ('Eastern/INDEX', '../Western/INDEX', '../../WesternPhilosophy/Western/INDEX'),
    
    # PoliticalScience/INDEX links to ../InternationalRelations - WRONG
    ('PoliticalScience/INDEX', '../InternationalRelations/INDEX', 'InternationalRelations/INDEX'),
    
    # InternationalRelations/INDEX inside PoliticalScience links to ../PoliticalScience, ../Economics, ../History
    ('PoliticalScience/InternationalRelations/INDEX', '../PoliticalScience/INDEX', ''),
    ('PoliticalScience/InternationalRelations/INDEX', '../Economics/INDEX', ''),
    ('PoliticalScience/InternationalRelations/INDEX', '../History/INDEX', ''),
    
    # Psychology/INDEX links to ../Cognitive, ../Social, ../../Economics
    ('Psychology/INDEX', '../Cognitive/INDEX', 'Cognitive/INDEX'),
    ('Psychology/INDEX', '../Social/INDEX', 'SocialPsychology/INDEX'),
    ('Psychology/INDEX', '../../Economics/INDEX', '../../Economics/INDEX'),
    
    # BehavioralEconomics/INDEX links to ../Cognitive - WRONG depth
    ('BehavioralEconomics/INDEX', '../Cognitive/INDEX', '../../Psychology/Cognitive/INDEX'),
}

# Phase 1: Fix vault-root links
print('=== Phase 1: Fix vault-root rename links ===')
for old_link, new_path in rename_fixes.items():
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
            
            # Check in content without display text
            new_content = content
            modified = False
            
            # Pattern: [[old_link]] or [[old_link|display_text]]
            pattern_plain = '[[' + old_link + ']]'
            pattern_with_display = re.escape('[[' + old_link + '|')
            
            if pattern_plain in new_content:
                new_content = new_content.replace(pattern_plain, '[[' + new_path + ']]')
                modified = True
            
            # Handle with display text
            for m in re.finditer(re.escape('[[') + re.escape(old_link) + r'\|([^\]]+)\]', content):
                display = m.group(1)
                old_full = f'[[{old_link}|{display}]]'
                new_full = f'[[{new_path}|{display}]]'
                if old_full in new_content:
                    new_content = new_content.replace(old_full, new_full)
                    modified = True
            
            if modified:
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
                print(f'  [{old_link}] -> [{new_path}] in {os.path.relpath(fpath, BASE)}')

# Phase 2: Fix relative path links
print('\n=== Phase 2: Fix relative-path links ===')
for src_pattern, old_link, new_link in relative_fixes:
    for root, dirs, files in os.walk(BASE):
        if '.git' in root or '.obsidian' in root or '.ruff_cache' in root or '.opencode' in root:
            continue
        for f in files:
            if not f.endswith('.md'):
                continue
            if src_pattern not in f:
                continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
            except:
                continue
            
            new_content = content
            modified = False
            rel_src = os.path.relpath(fpath, BASE)
            
            # Check for old_link in content
            pattern = f'[[{old_link}]]'
            if pattern in new_content:
                if new_link:
                    new_content = new_content.replace(pattern, f'[[{new_link}]]')
                else:
                    new_content = new_content.replace(pattern, '')
                modified = True
            
            # Check with display text
            for m in re.finditer(re.escape('[[') + re.escape(old_link) + r'\|([^\]]+)\]', content):
                display = m.group(1)
                old_full = f'[[{old_link}|{display}]]'
                if new_link:
                    new_full = f'[[{new_link}|{display}]]'
                else:
                    new_full = display
                if old_full in new_content:
                    new_content = new_content.replace(old_full, new_full)
                    modified = True
            
            if modified:
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(new_content)
                print(f'  [{old_link}] -> [{new_link or "(removed)"}] in {rel_src}')

print('\nDone!')
