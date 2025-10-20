from pathlib import Path
from typing import List
from .models import ModuleInfo

def build_markdown(modules: List[ModuleInfo], out_dir: Path) -> None:
    """
    Build grouped Markdown (Python / JavaScript / Java).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / "index.md"
    api_path = out_dir / "api.md"

    index_path.write_text(
        "# Project Documentation\n\n"
        "Generated automatically by the AI-Enhanced Documentation Generator.\n\n",
        encoding="utf-8",
    )

    groups = {"py": [], "js": [], "java": []}
    for m in modules:
        if m.file_path.endswith(".py"):
            groups["py"].append(m)
        elif m.file_path.endswith(".js"):
            groups["js"].append(m)
        elif m.file_path.endswith(".java"):
            groups["java"].append(m)

    md = ["# API Reference\n"]

    for label, title in [("py", "Python Modules"),
                         ("js", "JavaScript Modules"),
                         ("java", "Java Modules")]:
        if groups[label]:
            md.append(f"\n## {title}\n")
            for m in groups[label]:
                md.append(f"### Module: `{m.file_path}`\n")
                if m.module_doc:
                    md.append(f"{m.module_doc}\n")
                if m.functions:
                    md.append("\n**Functions**:\n")
                    for f in m.functions:
                        md.append(f"- `{f.signature}` — {f.doc or 'No docstring.'}")
                if m.classes:
                    md.append("\n**Classes**:\n")
                    for c in m.classes:
                        md.append(f"- `{c.name}` — {c.doc or 'No docstring.'}")
                md.append("\n---\n")

    api_path.write_text("\n".join(md), encoding="utf-8")
