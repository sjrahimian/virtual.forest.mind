#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Virtual Forest Mind CLI Tool

    Yet another plaintext notetaking system.

    Provides commands to initialize, create, search, and open Markdown 
    notes (or any plaintext note) in a user-defined folder system.

    Copyright (C) 2025, Sama Rahimian

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

__version__ = "1.1.0"
__author__ = "Sama Rahimian"
__license__ = "GNU GPLv3"

from pathlib import Path
import argparse
import configparser
import sys
import time
import re
import subprocess
import shlex
import shutil
from typing import Optional


# ----------------------------
# Path management
# ----------------------------

class PathManager:
    def __init__(self):
        self.script_dir = self._get_script_dir()
        self.root_dir = Path.cwd()
        self.config_file = self.script_dir / "vfm.conf"
        self.template_dir = self.script_dir / "templates"
        self.default_template = self.template_dir / "note.md"

    @staticmethod
    def _get_script_dir() -> Path:
        if getattr(sys, "frozen", False):
            # for PyInstaller / frozen binaries
            return Path(sys.executable).resolve().parent

        return Path(__file__).resolve().parent


# ----------------------------
# Config management
# ----------------------------

class ConfigManager:
    def __init__(self, paths: PathManager):
        self.paths = paths
        self.parser = configparser.ConfigParser()
        if "init" and "-h" and "--help" not in sys.argv:
            self._load()

    def _load(self):
        if not self.paths.config_file.exists():
            raise FileNotFoundError(f"Missing config file: {self.paths.config_file}\nFirst run: {Path(sys.argv[0]).name} [init|-h, --help]")
        self.parser.read(self.paths.config_file)

    @property
    def spaces(self) -> dict:
        return dict(self.parser["paths"]) if "paths" in self.parser else {}

    @property
    def editor(self) -> Optional[str]:
        return self.parser.get("settings", "editor", fallback=None)


# ----------------------------
# Editor handling
# ----------------------------

class Editor:
    def __init__(self, editor_cmd: Optional[str]):
        self.editor_cmd = editor_cmd

    def open(self, file_path: Path):
        if not self.editor_cmd:
            self._open_system_default(file_path)
            return

        parts = shlex.split(self.editor_cmd)
        exe = parts[0]

        if not Path(exe).exists():
            resolved = shutil.which(exe)
            if not resolved:
                raise RuntimeError(f"Editor not found: {exe}")
            parts[0] = resolved

        subprocess.run(parts + [str(file_path)])

    @staticmethod
    def _open_system_default(path: Path):
        if sys.platform.startswith("win"):
            os.startfile(path)  # type: ignore
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        else:
            subprocess.run(["xdg-open", str(path)])


# ----------------------------
# Notes
# ----------------------------
TAGS = """---
tags:
  - new-note-tag
---
"""

class NoteManager:
    def __init__(self, paths: PathManager, config: ConfigManager):
        self.paths = paths
        self.config = config

    def create(self, target: str) -> Path:
        base_dir = self._resolve_target(target)
        base_dir.mkdir(parents=True, exist_ok=True)

        # Ask for filename
        default = "new-note"
        name = input(f"Filename [{default}]: ").strip() or default

        # Append epoch + extension
        epoch = int(time.time())
        file_path = base_dir / f"{name}-{epoch}.md"
        content = self._load_template()

        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_path}")
        return file_path

    def _resolve_target(self, target: str) -> Path:
        if target in self.config.spaces:
            return Path(self.config.spaces[target]).expanduser().resolve()
        return Path(target).expanduser().resolve()

    def _load_template(self) -> str:
        tmpl = self.paths.default_template
        if tmpl.exists():
            return tmpl.read_text(encoding="utf-8")
        return f"{TAGS}\n# Welcome Note!\n\n_created:_ {epoch} // {datetime.now()}\n\n"

# ----------------------------
# Initialize
# ----------------------------

class InitManager(NoteManager):
    def __init__(self, paths: PathManager):
        self.paths = paths
        self.paths.config_file = self.paths.root_dir / self.paths.config_file.name
        self._handle_init()

    def _handle_init(self):
        if self.paths.config_file.exists():
            print(f"Virtual Forest Mind has already been initialized.")
            return

        dirs = {
            "space": Path("vfm.space"),
            "private": Path("vfm.private"),
            "public": Path("vfm.public"),
        }

        for key, directory in dirs.items():
            directory.mkdir(parents=True, exist_ok=True)

        self.paths.config_file.write_text(self._default_config(), encoding="utf-8")
        
        root = self.paths.config_file.cwd() / "vfm"
        print(f"Config file created: {self.paths.config_file}")
        print(f"Workspace: {root}")
        # note = self.create("private")
        # print(f"Initial note: {note}")cls
        print("VFM initialized successfully.")

    def _default_config(self) -> str:
        return """# vfm configuration

[paths]
space = vfm/vfm.space
private = vfm/vfm.private
public = vfm/vfm.public

[editor]
default = codium
"""

# ----------------------------
# Search
# ----------------------------

class SearchManager:
    def __init__(self, config: ConfigManager, editor: Editor):
        self.config = config
        self.editor = editor

    def search(self, target: str, pattern: str, ignore_case: bool):
        flags = re.IGNORECASE if ignore_case else 0
        regex = re.compile(pattern, flags)

        dirs = self._resolve_dirs(target)
        matches = []
        seen = set()

        for d in dirs:
            for md in d.rglob("*.md"):
                if md in seen:
                    continue
                try:
                    text = md.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                if regex.search(text):
                    title = self._extract_h1(text)
                    matches.append((md, title))
                    seen.add(md)

        self._handle_results(matches)

    def _resolve_dirs(self, target: str):
        if target == "all":
            return [Path(p).expanduser().resolve() for p in self.config.spaces.values()]
        if target in self.config.spaces:
            return [Path(self.config.spaces[target]).expanduser().resolve()]
        return [Path(target).expanduser().resolve()]

    @staticmethod
    def _extract_h1(text: str) -> Optional[str]:
        for line in text.splitlines():
            if line.startswith("# ") and not line.startswith("##"):
                return line[2:].strip()
        return None

    def _handle_results(self, matches):
        if not matches:
            print("No matches found.")
            return

        if len(matches) == 1:
            self.editor.open(matches[0][0])
            return

        for i, (fp, title) in enumerate(matches, 1):
            parent = fp.parent.name
            label = f"{parent}/{fp.name}"
            if title:
                label += f" — {title}"
            print(f"{i}. {label}")

        choice = input("Select file number to open: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(matches):
                self.editor.open(matches[idx][0])

# ----------------------------
# Statistics Manager
# ----------------------------

class StatsManager:
    def __init__(self, config: ConfigManager):
        self.config = config

    def stats(self, target: str):
        dirs = self._resolve_dirs(target)

        file_count = 0
        dir_count = 0
        line_count = 0
        word_count = 0

        for d in dirs:
            if not d.exists() or not d.is_dir():
                continue

            for p in d.rglob("*"):
                if p.is_dir():
                    dir_count += 1
                elif p.is_file() and p.suffix.lower() == ".md":
                    file_count += 1
                    try:
                        text = p.read_text(encoding="utf-8", errors="ignore")
                    except Exception:
                        continue
                    lines = text.splitlines()
                    line_count += len(lines)
                    word_count += sum(len(line.split()) for line in lines)

        self._print_stats(target, file_count, dir_count, line_count, word_count)
        self.count_tags(target)

    def _resolve_dirs(self, target: str):
        if target == "all":
            return [Path(p).expanduser().resolve() for p in self.config.spaces.values()]
        if target in self.config.spaces:
            return [Path(self.config.spaces[target]).expanduser().resolve()]
        return [Path(target).expanduser().resolve()]

    @staticmethod
    def _print_stats(target, files, dirs, lines, words):
        print(f"\nStats for: {target}")
        print("-" * 30)
        print(f"Directories : {dirs}")
        print(f"Markdown files : {files}")
        print(f"Total lines : {lines}")
        print(f"Total words : {words}")
    
    def count_tags(self, target: str, limit: int = 10):
        """
        Count YAML frontmatter tags across markdown files.
        Expects tags in YAML list form:
            ---
            tags:
              - tag1
              - tag2
            ---
        """
        dirs = self._resolve_dirs(target)
        tag_counter = Counter()

        for d in dirs:
            if not d.exists() or not d.is_dir():
                continue

            for md in d.rglob("*.md"):
                try:
                    text = md.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue

                if not text.startswith("---"):
                    continue

                parts = text.split("---", 2)
                if len(parts) < 3:
                    continue

                frontmatter = parts[1]
                for line in frontmatter.splitlines():
                    line = line.strip()
                    if line.startswith("- "):  # YAML list-style tag
                        tag = line[2:].strip()
                        if tag:
                            tag_counter[tag] += 1

        if not tag_counter:
            print("No tags found.")
            return

        print("\nTop tags:")
        for tag, count in tag_counter.most_common(limit):
            print(f"  {tag}: {count}")

# ----------------------------
# App / CLI
# ----------------------------

class VFMApp:
    def __init__(self):
        self.paths = PathManager()
        self.config = ConfigManager(self.paths)
        self.editor = Editor(self.config.editor)
        self.notes = NoteManager(self.paths, self.config)
        self.searcher = SearchManager(self.config, self.editor)
        self.stats = StatsManager(self.config)

    def run(self):
        parser = self._build_parser()
        args = parser.parse_args()

        if args.command == "init":
            print("Seeding the virtual forest mind...")
            InitManager(self.paths)
        elif args.command == "new":
            self.notes.create(args.target)
        elif args.command == "search":
            self.searcher.search(args.target, args.pattern, args.ignore_case)
        elif args.command == "stats":
            self.stats.stats(args.target)

    @staticmethod
    def _build_parser():
        parser = argparse.ArgumentParser(description="Virtual Forest Mind CLI is a plaintext notetaking system.")
        subparsers = parser.add_subparsers(dest="command", required=True)
        
        # "init" command
        subparsers.add_parser("init", help="Initialize directories and config")

        # "new" command
        p_new = subparsers.add_parser("new", help="Create a new note")
        p_new.add_argument("target", type=str, help="Path or space keyword")

        # "stats" command
        p_stats = subparsers.add_parser("stats", help="Output statistics: number of notes, most active space, total words")
        p_stats.add_argument("target", type=str, help="Path or keyword from config")

        # "search" command
        p_search = subparsers.add_parser("search", help="Search notes")
        p_search.add_argument("target", type=str, nargs="?", default="all", help="Optional space keyword or path to search (default: all)")
        p_search.add_argument("pattern", help="Regex or plain text to search for")
        p_search.add_argument("-i", "--ignore-case", action="store_false", help="Perform case-insensitive search")

        return parser


# ----------------------------
# Entry
# ----------------------------

if __name__ == "__main__":
    try:
        VFMApp().run()
    except FileNotFoundError as e:
        print()
        print(e)
        print()
        sys.exit(0)
    except KeyboardInterrupt:
        print()
        sys.exit(-1)