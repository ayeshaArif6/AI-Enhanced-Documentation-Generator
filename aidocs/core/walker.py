from pathlib import Path
from typing import List

def find_python_files(root: Path) -> List[Path]:
    return [p for p in root.rglob("*.py") if "site-packages" not in str(p)]
