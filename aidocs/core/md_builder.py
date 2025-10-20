from pathlib import Path
from typing import List
from .models import ModuleInfo

SITE_INDEX = """\
# Project Documentation

This site was auto-generated from the codebase.  
- **API Reference:** See detailed docs for modules, classes, and functions.

[→ API Reference](./api.md)
"""

API_HEADER = """\
# API Reference

> Generated from parsed Python symbols. Improve by adding docstrings to your code.
"""

def build_markdown(mods: List[ModuleInfo], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.md").write_text(SITE_INDEX, encoding="utf-8")

    lines = [API_HEADER]
    for m in sorted(mods, key=lambda x: x.file_path.lower()):
        rel = m.file_path
        if m.module_doc:
            lines.append(f"\n## Module: `{rel}`\n\n{m.module_doc}\n")
        else:
            lines.append(f"\n## Module: `{rel}`\n")

        if m.functions:
            lines.append("\n### Top-level Functions\n")
            for f in m.functions:
                lines.append(f"#### `{f.signature}`  \nDefined at lines {f.lineno}"
                             + (f"–{f.end_lineno}" if f.end_lineno else "")
                             + "\n")
                if f.doc:
                    lines.append(f"{f.doc}\n")

        if m.classes:
            lines.append("\n### Classes\n")
            for c in m.classes:
                lines.append(f"#### `{c.name}`  \nDefined at lines {c.lineno}"
                             + (f"–{c.end_lineno}" if c.end_lineno else "")
                             + "\n")
                if c.doc:
                    lines.append(f"{c.doc}\n")
                if c.methods:
                    lines.append("\nMethods:\n")
                    for mth in c.methods:
                        lines.append(f"- `{mth.signature}`  (lines {mth.lineno}"
                                     + (f"–{mth.end_lineno}" if mth.end_lineno else "")
                                     + ")")
                        if mth.doc:
                            lines.append(f"  \n  {mth.doc}")

    (out_dir / "api.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
