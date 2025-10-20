import esprima
from pathlib import Path
from .models import ModuleInfo, FunctionInfo, ClassInfo


def parse_js_file(path: Path) -> ModuleInfo:
    """
    Parse a JavaScript file and extract top-level functions and classes.
    """
    code = path.read_text(encoding="utf-8")
    try:
        tree = esprima.parseScript(code, tolerant=True, loc=True)
    except Exception as e:
        print(f"[parser error] {path}: {e}")
        return ModuleInfo(file_path=str(path), module_doc=None)

    functions = []
    classes = []

    for node in tree.body:
        # function foo() { ... }
        if node.type == "FunctionDeclaration":
            name = node.id.name if node.id else "<anonymous>"
            functions.append(
                FunctionInfo(
                    name=name,
                    signature=f"{name}()",
                    doc=None,
                    lineno=node.loc.start.line,
                    end_lineno=node.loc.end.line if node.loc else None,
                )
            )

        # class MyClass { ... }
        elif node.type == "ClassDeclaration":
            name = node.id.name if node.id else "<anonymous>"
            classes.append(
                ClassInfo(
                    name=name,
                    doc=None,
                    lineno=node.loc.start.line,
                    end_lineno=node.loc.end.line if node.loc else None,
                )
            )

    return ModuleInfo(
        file_path=str(path),
        module_doc=None,
        classes=classes,
        functions=functions,
    )
