#!/usr/bin/env python3
"""Build student-pack PDFs and optionally watch lesson files for changes."""

from __future__ import annotations

import argparse
from html import escape
import os
import sys
import time
from pathlib import Path

import markdown

if sys.platform == "darwin":
    homebrew_library_paths = [
        str(path)
        for path in (Path("/opt/homebrew/lib"), Path("/usr/local/lib"))
        if path.is_dir()
    ]
    existing_library_paths = os.environ.get("DYLD_FALLBACK_LIBRARY_PATH")
    if existing_library_paths:
        homebrew_library_paths.append(existing_library_paths)
    if homebrew_library_paths:
        os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = ":".join(homebrew_library_paths)

from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]
LESSONS = ROOT / "lessons"
STYLESHEET = ROOT / "scripts" / "student-pack.css"
POLL_INTERVAL_SECONDS = 1.5


def find_student_packs(paths: list[Path]) -> list[Path]:
    packs: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved.is_dir():
            packs.update(resolved.rglob("student-pack.md"))
        elif resolved.name == "student-pack.md" and resolved.is_file():
            packs.add(resolved)
        else:
            raise FileNotFoundError(f"Student pack not found: {path}")
    return sorted(packs)


def build_pdf(source: Path) -> Path:
    extensions = ["tables", "fenced_code", "sane_lists", "smarty"]
    body = markdown.markdown(source.read_text(encoding="utf-8"), extensions=extensions)
    title = escape(source.parent.name.replace("-", " "))
    html = f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <link rel="stylesheet" href="{STYLESHEET.as_uri()}">
</head>
<body>{body}</body>
</html>
"""
    destination = source.with_name("student-pack.pdf")
    HTML(string=html, base_url=source.parent.as_uri()).write_pdf(destination)
    return destination


def snapshot(packs: list[Path]) -> dict[Path, tuple[int, int]]:
    return {path: (path.stat().st_mtime_ns, path.stat().st_size) for path in packs}


def watch() -> int:
    packs = find_student_packs([LESSONS])
    if not packs:
        print(f"No student-pack.md files found under {LESSONS}", file=sys.stderr)
        return 1

    for pack in packs:
        try:
            print(f"Built {build_pdf(pack).relative_to(ROOT)}")
        except (OSError, RuntimeError, ValueError) as error:
            print(f"Failed to build {pack}: {error}", file=sys.stderr)
            return 1

    observed = snapshot(packs)
    observed_stylesheet = snapshot([STYLESHEET])[STYLESHEET]
    print(f"Watching {len(packs)} student pack(s). Save a student-pack.md to refresh its PDF.")
    while True:
        time.sleep(POLL_INTERVAL_SECONDS)
        current_packs = find_student_packs([LESSONS])
        current = snapshot(current_packs)
        current_stylesheet = snapshot([STYLESHEET])[STYLESHEET]
        stylesheet_changed = current_stylesheet != observed_stylesheet
        changed = [
            path for path in current_packs
            if stylesheet_changed or path not in observed or current[path] != observed.get(path)
        ]
        for pack in changed:
            try:
                print(f"Built {build_pdf(pack).relative_to(ROOT)}", flush=True)
                observed[pack] = current[pack]
            except (OSError, RuntimeError, ValueError) as error:
                print(f"Failed to build {pack}: {error}", file=sys.stderr, flush=True)
                observed[pack] = current[pack]
        observed_stylesheet = current_stylesheet
        for removed in observed.keys() - current.keys():
            observed.pop(removed)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Build all student packs, then rebuild a PDF whenever a pack changes.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Lesson directory or student-pack.md file(s); defaults to all lessons.",
    )
    args = parser.parse_args()

    if args.watch:
        if args.paths:
            parser.error("--watch monitors all lesson student packs; do not pass paths")
        return watch()

    paths = args.paths or [LESSONS]
    packs = find_student_packs(paths)
    if not packs:
        print("No student-pack.md files found.", file=sys.stderr)
        return 1
    for pack in packs:
        print(f"Built {build_pdf(pack).relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
