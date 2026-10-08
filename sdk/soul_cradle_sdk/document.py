"""Document loading: PDF, Markdown, and plain text -> text + sections."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


@dataclass
class Section:
    section_id: str
    heading: str
    text: str
    source_ref: str  # e.g. "pages 2-3", "lines 40-120"


@dataclass
class Document:
    filename: str
    sha256: str
    text: str
    pages: int
    sections: List[Section] = field(default_factory=list)


def _read_pdf(path: Path) -> Tuple[str, int, List[Tuple[int, str]]]:
    from pypdf import PdfReader
    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        pages.append((i + 1, page.extract_text() or ""))
    full = "\n".join(t for _, t in pages)
    return full, len(pages), pages


def _split_markdown(text: str, filename: str) -> List[Section]:
    lines = text.split("\n")
    sections: List[Section] = []
    cur_heading, cur_lines, start = "Document", [], 1
    for i, line in enumerate(lines, 1):
        m = re.match(r"#{1,3}\s+(.*)", line.strip())
        if m and cur_lines:
            sections.append(Section(
                section_id=f"s{len(sections)+1:02d}",
                heading=cur_heading[:80],
                text="\n".join(cur_lines).strip(),
                source_ref=f"lines {start}-{i-1} of {filename}",
            ))
            cur_heading, cur_lines, start = m.group(1).strip(), [], i
        elif m:
            cur_heading = m.group(1).strip()
            start = i
        else:
            cur_lines.append(line)
    if cur_lines and "\n".join(cur_lines).strip():
        sections.append(Section(
            section_id=f"s{len(sections)+1:02d}",
            heading=cur_heading[:80],
            text="\n".join(cur_lines).strip(),
            source_ref=f"lines {start}-{len(lines)} of {filename}",
        ))
    return [s for s in sections if s.text]


def _split_chunks(text: str, filename: str, unit: str,
                  parts: List[Tuple[int, str]]) -> List[Section]:
    sections: List[Section] = []
    buf, start, n = [], None, 0
    for idx, chunk in parts:
        buf.append(chunk)
        if start is None:
            start = idx
        if sum(len(c) for c in buf) >= 4000:
            n += 1
            sections.append(Section(
                section_id=f"s{n:02d}",
                heading=f"{filename} ({unit}s {start}-{idx})",
                text="\n".join(buf).strip(),
                source_ref=f"{unit}s {start}-{idx} of {filename}",
            ))
            buf, start = [], None
    if buf and "\n".join(buf).strip():
        n += 1
        sections.append(Section(
            section_id=f"s{n:02d}",
            heading=f"{filename} ({unit}s {start}-{parts[-1][0]})",
            text="\n".join(buf).strip(),
            source_ref=f"{unit}s {start}-{parts[-1][0]} of {filename}",
        ))
    return sections


def load_document(path: str | Path) -> Document:
    """Load a PDF, Markdown, or text file into sections for evaluation."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"no such file: {path}")
    raw = p.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    suffix = p.suffix.lower()

    if suffix == ".pdf":
        text, npages, pages = _read_pdf(p)
        sections = _split_chunks(text, p.name, "page", pages)
    else:
        text = raw.decode("utf-8", errors="replace")
        npages = 1
        if suffix in (".md", ".markdown") and re.search(r"(?m)^#{1,3}\s+", text):
            sections = _split_markdown(text, p.name)
        else:
            paras = [(i + 1, para) for i, para in enumerate(text.split("\n\n"))]
            sections = _split_chunks(text, p.name, "paragraph", paras)

    if not text.strip():
        raise ValueError(f"{p.name}: no extractable text")
    if not sections:
        sections = [Section(section_id="s01", heading=p.name,
                            text=text[:4000], source_ref=f"full text of {p.name}")]
    return Document(filename=p.name, sha256=digest, text=text,
                    pages=npages, sections=sections)
