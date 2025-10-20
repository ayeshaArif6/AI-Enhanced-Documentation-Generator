import ast
from pathlib import Path
from typing import List
from .models import ModuleInfo, ClassInfo, FunctionInfo

def _signature_from_func(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    """Rebuild a signature string from AST args."""
    parts = []
    for a in node.args.args:
        parts.append(a.arg)
    if node.args.vararg:
        parts.append("*" + node.args.vararg.arg)
    for a in node.args.kwonlyargs:
        parts.append(a.arg + "=?")
    if node.args.kwarg:
        parts.append("**" + node.args.kwarg.arg)
    return f"{node.name}({', '.join(parts)})"

def parse_python_file(path: Path) -> ModuleInfo:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    module_doc = ast.get_docstring(tree)
    classes: List[ClassInfo] = []
    functions: List[FunctionInfo] = []

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(FunctionInfo(
                name=node.name,
                signature=_signature_from_func(node),
                doc=ast.get_docstring(node),
                lineno=node.lineno,
                end_lineno=getattr(node, "end_lineno", None),
            ))
        elif isinstance(node, ast.ClassDef):
            cinfo = ClassInfo(
                name=node.name,
                doc=ast.get_docstring(node),
                lineno=node.lineno,
                end_lineno=getattr(node, "end_lineno", None),
                methods=[],
            )
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    cinfo.methods.append(FunctionInfo(
                        name=child.name,
                        signature=_signature_from_func(child),
                        doc=ast.get_docstring(child),
                        lineno=child.lineno,
                        end_lineno=getattr(child, "end_lineno", None),
                    ))
            classes.append(cinfo)

    return ModuleInfo(
        file_path=str(path),
        module_doc=module_doc,
        classes=classes,
        functions=functions,
    )
