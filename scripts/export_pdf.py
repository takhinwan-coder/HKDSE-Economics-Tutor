#!/usr/bin/env python3
"""Export a Markdown lesson file to a print-ready PDF using Chromium."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from markdown_it import MarkdownIt


def find_browser() -> str | None:
    for candidate in (
        "chromium",
        "chromium-browser",
        "google-chrome",
        "google-chrome-stable",
        "chrome",
    ):
        if browser := shutil.which(candidate):
            return browser
    return None


def render_html(source: Path, markdown: str, stylesheet: str) -> str:
    renderer = MarkdownIt("default").enable(["table", "strikethrough"])
    content = renderer.render(markdown)
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <base href="{source.parent.as_uri()}/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>{stylesheet}</style>
</head>
<body>
  <main>{content}</main>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a Markdown lesson to a sibling PDF using Chromium."
    )
    parser.add_argument("source", type=Path, help="Markdown file to export")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="PDF destination (default: same folder and filename as the Markdown)",
    )
    parser.add_argument(
        "--browser",
        help="Chromium/Chrome executable (default: discover it from PATH)",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        parser.error(f"Markdown file not found: {source}")
    if source.suffix.lower() != ".md":
        parser.error("Source file must have a .md extension")

    output = (
        args.output.expanduser().resolve()
        if args.output
        else source.with_suffix(".pdf")
    )
    if output == source:
        parser.error("PDF output must not overwrite the Markdown source")
    output.parent.mkdir(parents=True, exist_ok=True)

    browser = args.browser or find_browser()
    if not browser:
        parser.error(
            "Chromium or Google Chrome was not found. Install it or pass --browser."
        )
    if args.browser and not Path(args.browser).is_file() and not shutil.which(args.browser):
        parser.error(f"Browser executable not found: {args.browser}")

    stylesheet_path = Path(__file__).with_name("print.css")
    markdown = source.read_text(encoding="utf-8")
    document = render_html(
        source,
        markdown,
        stylesheet_path.read_text(encoding="utf-8"),
    )

    temporary_html: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=".html",
            prefix=".lesson-export-",
            dir=source.parent,
            delete=False,
        ) as html_file:
            html_file.write(document)
            temporary_html = Path(html_file.name)

        result = subprocess.run(
            [
                browser,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--no-first-run",
                "--no-pdf-header-footer",
                f"--print-to-pdf={output}",
                temporary_html.as_uri(),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            raise RuntimeError(detail or f"Browser exited with {result.returncode}")
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError("The browser did not create a PDF.")
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        output.unlink(missing_ok=True)
        print(f"PDF export failed: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary_html:
            temporary_html.unlink(missing_ok=True)

    print(f"PDF exported: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
