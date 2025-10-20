from pathlib import Path
import typer
from rich import print
from .core.walker import find_source_files
from .core.py_parser import parse_python_file
from .core.js_parser import parse_js_file
from .core.md_builder import build_markdown
from .core.ai_client import AIClient
from .core.java_parser import parse_java_file

app = typer.Typer(help="AI-Enhanced Documentation Generator")

@app.command()
def generate(
    src: str = typer.Argument(..., help="Path to project root to scan"),
    out: str = typer.Option("docs", "--out", "-o", help="Output directory"),
    ai: bool = typer.Option(False, "--ai", help="Enhance docs using OpenAI"),
):
    root = Path(src).resolve()
    out_dir = Path(out).resolve()
    if not root.exists():
        raise typer.BadParameter(f"Path not found: {root}")

    print(f"[bold]Scanning[/bold] {root}")
    files = find_source_files(root)
    if not files:
        print("[yellow]No supported files found.[/yellow]")
        raise typer.Exit()

    modules = []
    for f in files:
        if f.suffix == ".py":
            modules.append(parse_python_file(f))
        elif f.suffix == ".js":
            modules.append(parse_js_file(f))
        elif f.suffix == ".java":
            modules.append(parse_java_file(f))

    # Optional AI enhancement
    if ai:
        print("[cyan]Enhancing documentation with AI...[/cyan]")
        client = AIClient()
        for m in modules:
            try:
                code = Path(m.file_path).read_text(encoding="utf-8")
            except Exception:
                code = ""
            if m.module_doc:
                m.module_doc = client.improve_doc(code, m.module_doc)
            for f in m.functions:
                if f.doc:
                    f.doc = client.improve_doc(code, f.doc)
            for c in m.classes:
                if c.doc:
                    c.doc = client.improve_doc(code, c.doc)

    build_markdown(modules, out_dir)
    print("[green]Done![/green] Open docs/api.md")

def main():
    app()

if __name__ == "__main__":
    main()
