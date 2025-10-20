from pathlib import Path
from typing import List


def find_source_files(root: Path) -> List[Path]:
    """
    Recursively find all supported source files (.py, .js)
    """
    exts = [".py", ".js"]
    return [
        p for p in root.rglob("*")
        if p.suffix in exts and "site-packages" not in str(p)
    ]
