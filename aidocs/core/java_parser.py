import javalang
from pathlib import Path
from .models import ModuleInfo, ClassInfo, FunctionInfo

def parse_java_file(path: Path) -> ModuleInfo:
    """Parse a Java file to extract classes and methods."""
    code = path.read_text(encoding="utf-8")
    try:
        tree = javalang.parse.parse(code)
    except Exception as e:
        print(f"[parser error] {path}: {e}")
        return ModuleInfo(file_path=str(path), module_doc=None)

    classes, functions = [], []

    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        methods = []
        for m in node.methods:
            sig = f"{m.name}({', '.join(p.type.name for p in m.parameters)})"
            methods.append(FunctionInfo(
                name=m.name, signature=sig,
                doc=None, lineno=m.position.line if m.position else None))
        classes.append(ClassInfo(
            name=node.name, doc=None,
            methods=methods, lineno=node.position.line if node.position else None))

    for _, node in tree.filter(javalang.tree.MethodDeclaration):
        if not any(node in c.methods for c in classes):
            functions.append(FunctionInfo(
                name=node.name, signature=f"{node.name}()",
                doc=None, lineno=node.position.line if node.position else None))

    return ModuleInfo(
        file_path=str(path),
        module_doc=None,
        classes=classes,
        functions=functions,
    )
