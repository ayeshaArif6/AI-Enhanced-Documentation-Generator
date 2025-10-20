from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FunctionInfo:
    name: str
    signature: str
    doc: Optional[str]
    lineno: int
    end_lineno: Optional[int] = None

@dataclass
class ClassInfo:
    name: str
    doc: Optional[str]
    lineno: int
    end_lineno: Optional[int] = None
    methods: List[FunctionInfo] = field(default_factory=list)

@dataclass
class ModuleInfo:
    file_path: str
    module_doc: Optional[str]
    classes: List[ClassInfo] = field(default_factory=list)
    functions: List[FunctionInfo] = field(default_factory=list)
