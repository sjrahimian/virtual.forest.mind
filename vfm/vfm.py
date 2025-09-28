#!/usr/bin/env python3
import argparse
import configparser
from datetime import datetime
from pathlib import Path
import re
import sys
import time

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

    return paths, settings


def handle_stats(target: str):
    """Show statistics about notes in a given space (or all)."""
    from collections import Counter

    config = load_config()

    # If "all", scan all spaces
    if target == "all":
        paths = [Path(p) for p in config.values()]
    else:
        if target in config:
            paths = [Path(config[target])]
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

def handle_new(target):
    """Handle the 'new' command"""
    config = load_config()

    # Resolve target as keyword or path
    if target in config:
        path = Path(config[target]).expanduser().resolve()
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
    stats_parser = subparsers.add_parser("stats", help="Output statistics: number of notes, most active space, total words.")
    stats_parser.add_argument("target", type=str, help="Path or keyword from config")


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

if __name__ == "__main__":
    main()
