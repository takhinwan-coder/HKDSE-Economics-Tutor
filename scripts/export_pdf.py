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


def warn_if_cjk_font_is_missing() -> None:
    font_matcher = shutil.which("fc-match")
    if not font_matcher:
        return
    result = subprocess.run(
        [font_matcher, "-f", "%{family}", ":lang=zh"],
        check=False,
        capture_output=True,
        text=True,
    )
    family = result.stdout.strip().lower()
    known_cjk_families = (
        "noto",
        "source han",
        "wenquanyi",
        "microsoft jhenghei",
        "mingliu",
        "pingfang",
        "ar pl",
    )
    if result.returncode == 0 and family and not any(
        name in family for name in known_cjk_families
    ):
        print(
            "Warning: no common Chinese font was detected; install a Traditional "
            "Chinese font (for example Noto Sans CJK TC) before sharing this PDF.",
            file=sys.stderr,
        )


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
    if output.suffix.lower() != ".pdf":
        parser.error("Output file must have a .pdf extension")
    output.parent.mkdir(parents=True, exist_ok=True)

    browser = args.browser or find_browser()
    if not browser:
        parser.error(
            "Chromium or Google Chrome was not found. Install it or pass --browser."
        )
    if args.browser and not Path(args.browser).is_file() and not shutil.which(args.browser):
        parser.error(f"Browser executable not found: {args.browser}")

    warn_if_cjk_font_is_missing()

    stylesheet_path = Path(__file__).with_name("print.css")
    markdown = source.read_text(encoding="utf-8")
    document = render_html(
        source,
        markdown,
        stylesheet_path.read_text(encoding="utf-8"),
    )

    temporary_html: Path | None = None
    temporary_pdf: Path | None = None
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

        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            prefix=".lesson-export-",
            dir=output.parent,
            delete=False,
        ) as pdf_file:
            temporary_pdf = Path(pdf_file.name)

        command = [
            browser,
            "--headless",
            "--disable-gpu",
            "--no-first-run",
            "--no-pdf-header-footer",
            f"--print-to-pdf={temporary_pdf}",
            temporary_html.as_uri(),
        ]
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0 and "No usable sandbox" in result.stderr:
            print(
                "Warning: Chromium sandbox is unavailable in this environment; "
                "retrying without it for this local Markdown export.",
                file=sys.stderr,
            )
            result = subprocess.run(
                [browser, "--no-sandbox", *command[1:]],
                check=False,
                capture_output=True,
                text=True,
                timeout=120,
            )
        if result.returncode != 0:
            detail = (result.stderr.strip() or result.stdout.strip())[-2000:]
            raise RuntimeError(detail or f"Browser exited with {result.returncode}")
        if (
            not temporary_pdf.is_file()
            or temporary_pdf.stat().st_size == 0
            or not temporary_pdf.read_bytes().startswith(b"%PDF-")
        ):
            raise RuntimeError("The browser did not create a PDF.")
        temporary_pdf.chmod(0o644)
        temporary_pdf.replace(output)
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        print(f"PDF export failed: {error}", file=sys.stderr)
        return 1
    finally:
        if temporary_html:
            temporary_html.unlink(missing_ok=True)
        if temporary_pdf:
            temporary_pdf.unlink(missing_ok=True)

    print(f"PDF exported: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
