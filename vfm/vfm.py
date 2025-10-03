#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vfm.py — Virtual Forest Mind CLI Tool

Provides commands to create, search, and open Markdown notes in user-defined spaces, 
  using a configuration file for paths and editor settings.

Created: 2025-09-30
"""

__version__ = "0.1.1"
__author__ = "Sama Rahimian"
__license__ = "GNU GPLv3"

import argparse
import configparser
from datetime import datetime
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import re
import time
from typing import List, Tuple, Optional

CONFIG_FILE = Path(".vfm_conf")
LIMIT_TAG_OUTPUT = 5
TAGS = """---
tags:
  - add-tag
---
"""

def ensure_config():
    """Ensure config exists, else exit with error."""
    if not CONFIG_FILE.exists():
        print(f"Error: vfm.conf is missing. Run `{Path(sys.argv[0]).name} init` first.")
        sys.exit(1)

def load_config():
    """Load config from vfm.conf"""
    ensure_config()
    parser = configparser.ConfigParser()
    file_content = CONFIG_FILE.read_text(encoding="utf-8")

    # Wrap in a dummy section if no headers exist
    if not file_content.strip().startswith("["):
        file_content = "[paths]\n" + file_content

    parser.read_string(file_content)
    paths = dict(parser["paths"])

    settings = {}
    if "settings" in parser:
        settings = dict(parser["settings"])
    # print(settings)
    # print(paths)
    return paths, settings

# --- Helper: find first H1 (# single hash) line ---
def extract_h1_title(text: str) -> Optional[str]:
    """
    Return the first line that starts with a single '#' (space after), trimmed.
    Skip lines starting with '##' or more.
    """
    for line in text.splitlines():
        m = re.match(r'^\s*#\s+(.*\S)', line)
        if m:
            return m.group(1).strip()
    return None

# --- The search handler ---
def handle_search(target: str, pattern: str, ignore_case: bool = False) -> None:
    """
    Search .md files under a target (keyword/path) for a regex/pattern.
    If target == "all", search all configured paths.
    """
    # Load config to get paths (and ignore settings here)
    try:
        paths_cfg, settings = load_config()
    except Exception:
        # If load_config only returns paths, handle that
        cfg = load_config()
        if isinstance(cfg, tuple) and len(cfg) == 2:
            paths_cfg, settings = cfg
        else:
            paths_cfg = cfg
            settings = {}

    # Resolve list of directories to search
    search_dirs: List[Path] = []
    if target == "all":
        for p in paths_cfg.values():
            search_dirs.append(Path(p).expanduser().resolve())
    else:
        if target in paths_cfg:
            search_dirs.append(Path(paths_cfg[target]).expanduser().resolve())
        else:
            # treat target as a path
            search_dirs.append(Path(target).expanduser().resolve())

    # Compile regex
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"Invalid regular expression: {e}")
        return

    # Find matches
    matches: List[Tuple[Path, str, str]] = []  # (file_path, first_h1_or_empty, excerpt_line)
    seen: set[Path] = set()  # keep track of files already added
    for d in search_dirs:
        if not d.exists() or not d.is_dir():
            continue

        for md in d.rglob("*.md"):
            if md in seen:
                continue

            try:
                text = md.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            if regex.search(text):
                h1 = extract_h1_title(text) or ""
                # find first matching line to show a short excerpt (optional)
                excerpt = ""
                for line in text.splitlines():
                    if regex.search(line):
                        excerpt = line.strip() if len(line) <= 100 else (line[0:100].strip()) + "..."
                        break
                matches.append((md, h1, excerpt))
                seen.add(md)

    # Respond based on number of matches
    if not matches:
        print("No files matched the search.")
        return

    if len(matches) == 1:
        file_path = matches[0][0]
        print(f"One match: {file_path}")
        handle_open(filename=file_path)
        return

    # Multiple matches — present menu
    while True:
        print("Multiple matches found:")
        for i, (fp, h1, excerpt) in enumerate(matches, start=1):
            # Show path relative to cwd if possible to keep it concise
            try:
                fp_display = fp.relative_to(Path.cwd())
            except Exception:
                fp_display = fp

            title_display = f" — {h1}" if h1 else ""
            excerpt_display = f"   | {excerpt}" if excerpt else ""
            print(f"{i}. {fp_display.parent.name}/{fp_display.name}{title_display}\n{excerpt_display}")
            # print(f"  {i}. {fp_display.name}{title_display}")

        # Prompt user for selection
        try:
            choice = input("Select file number to open (or press Enter to cancel): ").strip()
            if not choice:
                print("Canceled.")
                sys.exit(0)

            idx = int(choice)
            if 1 <= idx <= len(matches):
                chosen = matches[idx - 1][0]
                handle_open(filename=chosen)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def handle_open(filename: str, target: str=None):
    """Open a note in the editor defined in config (settings.editor)."""
    paths, settings = load_config()

    # Resolve base directory
    if target in paths:
        base_path = Path(paths[target]).expanduser().resolve()
    elif target:
        base_path = Path(target).expanduser().resolve()
    
    file_path = base_path / filename if target else filename
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Editor from config
    editor = settings.get("editor")
    if not editor:
        # fallback to system default
        if os.name == "nt":
            os.startfile(file_path)  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path)])
        else:
            subprocess.run(["xdg-open", str(file_path)])
        return

    # Parse editor string (can include flags)
    parts = shlex.split(editor)

    # If first part is not a path, try to resolve with shutil.which
    exe = parts[0]
    if not Path(exe).exists():
        resolved = shutil.which(exe)
        if resolved:
            parts[0] = resolved
        else:
            print(f"Error: Editor '{exe}' not found on PATH.")
            return

    # Final command
    cmd = parts + [str(file_path)]
    try:
        subprocess.run(cmd)
    except Exception as e:
        print(f"Error launching editor: {e}")

def handle_stats(target: str):
    """Show statistics about notes in a given space (or all)."""
    from collections import Counter

    paths, settings = load_config()

    # If "all", scan all spaces
    if target == "all":
        paths = [Path(p) for p in paths.values()]
    else:
        if target in paths:
            paths = [Path(paths[target])]
        else:
            paths = [Path(target).expanduser().resolve()]
    note_files = []
    for path in paths:
        if path.exists():
            note_files.extend(path.glob("*.md"))

    total_notes = len(note_files)
    total_words = 0
    tag_counter = Counter()

    tag_pattern = re.compile(r"^tags:\s*(?:- .+|\[.+\])", re.IGNORECASE)

    for file in note_files:
        text = file.read_text(encoding="utf-8")
        total_words += len(text.split())

        # extract tags from YAML frontmatter if present
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) > 2:
                frontmatter = parts[1]
                for line in frontmatter.splitlines():
                    if line.strip().startswith("- "):  # YAML list style
                        tag_counter[line.strip()[2:]] += 1

    print(f"Total notes: {total_notes}")
    print(f"Total words: {total_words}")
    if tag_counter:
        print("Top tags:")
        for tag, count in tag_counter.most_common(LIMIT_TAG_OUTPUT):
            print(f"  {tag}: {count}")

def handle_new(target: str):
    """Handle the 'new' command"""
    paths, settings = load_config()


    # Resolve target as keyword or path
    if target in paths:
        path = Path(paths[target]).expanduser().resolve()
    else:
        path = Path(target).expanduser().resolve()

    if not path.exists():
        print(f"Error: Path '{path}' does not exist.")
        return

    # Ask for filename
    default_name = "New Entry"
    user_input = input(f"Enter filename [{default_name}]: ").strip()
    if not user_input:
        user_input = default_name

    # Append epoch + extension
    epoch = int(time.time())
    final_name = f"quote-{epoch}.md"
    full_path = path / final_name

    # Create file
    full_path.write_text(f"{TAGS}\n# {user_input} - {epoch}\n\n_Created:_ {epoch} // {datetime.now()}", encoding="utf-8")
    print(f"Created: {full_path}")

    handle_open(filename=full_path)

def handle_init():
    """Handle the 'init' command: create directories + config"""
    dirs = {
        "space": Path("vfm.space"),
        "private": Path("vfm.private"),
        "public": Path("vfm.public"),
    }

    if not CONFIG_FILE.exists():
        for key, directory in dirs.items():
            directory.mkdir(parents=True, exist_ok=True)
            print(f"Ensured directory: {directory}")

        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            f.write(
                "[paths]\n"
                f"space={dirs['space'].resolve()}\n"
                f"private={dirs['private'].resolve()}\n"
                f"public={dirs['public'].resolve()}\n\n"
                "[settings]\n"
                "editor=code\n"
            )
        print(f"Created config file: {CONFIG_FILE}")
    else:
        print(f"Virtual Forest Mind is already initalized.")

def arguments():
    """Return the argument parser"""
    parser = argparse.ArgumentParser(description="Virtual Forest Mind CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # "init" command
    subparsers.add_parser("init", help="Initialize directories and config")

    # "new" command
    new_parser = subparsers.add_parser("new", help="Create a new note")
    new_parser.add_argument("target", type=str, help="Path or keyword from config")

    # "stats" command
    stats_parser = subparsers.add_parser("stats", help="Output statistics: number of notes, most active space, total words")
    stats_parser.add_argument("target", type=str, help="Path or keyword from config")

    # "search" command
    search_parser = subparsers.add_parser("search", help="egrep-like search in a space/path")
    search_parser.add_argument("target", type=str, nargs="?", default="all", help="Optional space keyword or path to search (default: all configured spaces)")
    search_parser.add_argument("pattern", help="Regex or plain text to search for")
    search_parser.add_argument("-i", "--ignore-case", action="store_true", help="Perform case-insensitive search")

    return parser.parse_args()

def main():
    args = arguments()
    if args.command == "new":
        handle_new(args.target)
    elif args.command == "stats":
        handle_stats(args.target)
    elif args.command == "init":
        print("Seeding the virtual forest mind...")
        handle_init()
    elif args.command == "search":
        handle_search(args.target, args.pattern, args.ignore_case)


if __name__ == "__main__":
    main()
