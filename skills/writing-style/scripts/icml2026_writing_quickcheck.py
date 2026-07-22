#!/usr/bin/env python3
"""
Heuristic writing/LaTeX checks for ICML-style drafts.

This script is intentionally lightweight (no external dependencies).
It is NOT a formal validator — treat it as a triage tool.

Usage:
  python scripts/icml2026_writing_quickcheck.py --tex path/to/main.tex
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    level: str  # INFO / WARN
    message: str


ABSTRACT_BEGIN = re.compile(r"\\begin\{abstract\}")
ABSTRACT_END = re.compile(r"\\end\{abstract\}")
IMPACT_HEADING = re.compile(r"\\section\*?\{Impact Statement\}", re.IGNORECASE)
ACK_HEADING = re.compile(r"\\section\*?\{Acknowledg(e)?ments\}", re.IGNORECASE)
BIBLIO = re.compile(r"\\bibliography\{|\\begin\{thebibliography\}")
NEG_VSPACE = re.compile(r"\\vspace\{-")
INCLUDEGRAPHICS = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}")


def _strip_comments(text: str) -> str:
    # Remove full-line comments and trailing comments (naive but useful).
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("%"):
            continue
        # remove trailing comment markers not escaped (best-effort)
        parts = re.split(r"(?<!\\)%", line, maxsplit=1)
        lines.append(parts[0])
    return "\n".join(lines)


def _count_sentences(paragraph: str) -> int:
    # Very rough heuristic; counts sentence-ending punctuation.
    return len(re.findall(r"[.!?]\s", paragraph.strip() + " "))


def check(tex_path: Path) -> list[Finding]:
    raw = tex_path.read_text(encoding="utf-8", errors="ignore")
    text = _strip_comments(raw)

    findings: list[Finding] = []

    # Abstract presence + size heuristic
    m_begin = ABSTRACT_BEGIN.search(text)
    m_end = ABSTRACT_END.search(text)
    if not (m_begin and m_end and m_end.start() > m_begin.end()):
        findings.append(Finding("WARN", "Abstract block not found (\\begin{abstract} ... \\end{abstract})."))
    else:
        abstract_body = text[m_begin.end() : m_end.start()].strip()
        # collapse whitespace
        abstract_one_line = re.sub(r"\s+", " ", abstract_body)
        sentence_count = _count_sentences(abstract_one_line)
        if sentence_count < 4:
            findings.append(Finding("WARN", f"Abstract seems short ({sentence_count} sentences)."))
        elif sentence_count > 10:
            findings.append(Finding("WARN", f"Abstract seems long ({sentence_count} sentences). Consider tightening."))
        else:
            findings.append(Finding("INFO", f"Abstract sentence count (heuristic): {sentence_count}."))

        if "\n\n" in abstract_body:
            findings.append(Finding("WARN", "Abstract contains multiple paragraphs; ICML abstracts are typically one paragraph."))

    # Impact statement presence (writing-relevant; placement checked in guidelines skill)
    if not IMPACT_HEADING.search(text):
        findings.append(Finding("WARN", "Impact Statement section not found. ICML requires an Impact statement."))
    else:
        findings.append(Finding("INFO", "Impact Statement section detected."))

    # Acknowledgements in anonymous drafts
    if ACK_HEADING.search(text):
        findings.append(Finding("WARN", "Acknowledgements section detected — remove for anonymous submission."))

    # Negative vspace count (layout risk)
    neg_count = len(NEG_VSPACE.findall(text))
    if neg_count > 0:
        findings.append(Finding("INFO", f"Found {neg_count} instances of negative \\vspace{{-...}}. Use sparingly."))

    # Quick inventory of graphics paths
    graphics = sorted(set(INCLUDEGRAPHICS.findall(text)))
    if graphics:
        findings.append(Finding("INFO", f"Detected {len(graphics)} includegraphics paths (check anonymity/metadata)."))

    # Bibliography presence
    if not BIBLIO.search(text):
        findings.append(Finding("WARN", "No bibliography directive found (\\bibliography{...} or thebibliography)."))

    return findings


def main(argv: Iterable[str]) -> int:
    parser = argparse.ArgumentParser(description="Heuristic writing/LaTeX checks for ICML-style drafts.")
    parser.add_argument("--tex", required=True, help="Path to main .tex file.")
    args = parser.parse_args(list(argv))

    tex_path = Path(args.tex).expanduser()
    if not tex_path.exists():
        raise SystemExit(f"File not found: {tex_path}")

    findings = check(tex_path)
    print(f"File: {tex_path}")
    for f in findings:
        print(f"[{f.level}] {f.message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv[1:]))
