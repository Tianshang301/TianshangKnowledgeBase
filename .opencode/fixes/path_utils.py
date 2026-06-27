#!/usr/bin/env python3
"""
Shared path utilities for TianshangKnowledgeBase fix scripts.
Auto-discovers the project root directory, eliminating hardcoded paths.
"""
import os
import pathlib


def find_project_root(marker_file='INDEX.md'):
    """
    Auto-discover the project root by walking up from this file's directory
    until finding a directory that contains the marker file.
    Falls back to environment variable KNOWLEDGE_BASE_DIR, then CWD.
    """
    script_dir = pathlib.Path(__file__).resolve().parent

    for parent in [script_dir, *script_dir.parents]:
        if (parent / marker_file).exists():
            return str(parent)

    env_dir = os.environ.get('KNOWLEDGE_BASE_DIR')
    if env_dir:
        return env_dir

    return os.getcwd()


#: Project root directory — import this in all fix scripts
BASE = find_project_root()

#: Directories to skip during file walks
SKIP_DIRS = {'.git', '.obsidian', '.ruff_cache', '__pycache__', 'node_modules'}

#: Files to skip during processing
SKIP_FILES = {'Vocabulary_3500.md'}


def relpath(filepath):
    """Return relative path from project root, with forward slashes."""
    return os.path.relpath(filepath, BASE).replace('\\', '/')


def walk_markdown(extra_skip=None):
    """
    Walk all .md files in the project, yielding (root, dirs, files) like os.walk,
    but with skip dirs already filtered out.
    """
    skip = SKIP_DIRS | set(extra_skip or [])
    for root, dirs, files in os.walk(BASE):
        dirs[:] = [d for d in dirs if d not in skip]
        # Filter to only .md files
        md_files = [f for f in files if f.endswith('.md')]
        yield root, dirs, md_files
