#!/usr/bin/env python3
"""
Extract a LaTeX outline (sections/subsections/paragraphs) with line numbers.

Usage:
  python scripts/extract_tex_outline.py --tex path/to/main.tex
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Heading:
    level: str
    title: str
    line_no: int


HEADING_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("section", re.compile(r"\\section\*?\{([^}]*)\}")),
    ("subsection", re.compile(r"\\subsection\*?\{([^}]*)\}")),
    ("subsubsection", re.compile(r"\\subsubsection\*?\{([^}]*)\}")),
    ("paragraph", re.compile(r"\\paragraph\*?\{([^}]*)\}")),
]

INPUT_PATTERN = re.compile(r"\\input\{([^}]*)\}")


def extract_outline(tex_path: Path) -> list[Heading]:
    headings: list[Heading] = []
    for idx, line in enumerate(tex_path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("%"):
            continue
        for level, pattern in HEADING_PATTERNS:
            m = pattern.search(line)
            if m:
                headings.append(Heading(level=level, title=m.group(1).strip(), line_no=idx))
    return headings


def extract_inputs(tex_path: Path) -> list[tuple[str, int]]:
    inputs: list[tuple[str, int]] = []
    for idx, line in enumerate(tex_path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("%"):
            continue
        for m in INPUT_PATTERN.finditer(line):
            inputs.append((m.group(1).strip(), idx))
    return inputs


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description="Extract LaTeX outline with line numbers.")
    parser.add_argument("--tex", required=True, help="Path to main .tex file.")
    args = parser.parse_args(list(argv))

    tex_path = Path(args.tex).expanduser()
    if not tex_path.exists():
        raise SystemExit(f"File not found: {tex_path}")

    headings = extract_outline(tex_path)
    inputs = extract_inputs(tex_path)

    print(f"File: {tex_path}")
    print("\nInputs:")
    if not inputs:
        print("  (none)")
    else:
        for name, ln in inputs:
            print(f"  L{ln}: \\input{{{name}}}")

    print("\nOutline:")
    if not headings:
        print("  (no headings found)")
    else:
        for h in headings:
            indent = {
                "section": "",
                "subsection": "  ",
                "subsubsection": "    ",
                "paragraph": "      ",
            }.get(h.level, "")
            print(f"{indent}L{h.line_no}: {h.level}: {h.title}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv[1:]))

