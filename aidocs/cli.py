from pathlib import Path
from typing import List
import typer
from rich import print
from .core.walker import find_python_files
from .core.py_parser import parse_python_file
from .core.md_builder import build_markdown

app = typer.Typer(help="AI-Enhanced Documentation Generator (Phase 1)")

@app.command()
def generate(
    src: str = typer.Argument(..., help="Path to project root to scan"),
    out: str = typer.Option("docs", "--out", "-o", help="Output directory for Markdown"),
):
    root = Path(src).resolve()
    out_dir = Path(out).resolve()
    if not root.exists():
        raise typer.BadParameter(f"Path not found: {root}")

    print(f"[bold]Scanning[/bold] {root} for Python files...")
    files = find_python_files(root)
    if not files:
        print("[yellow]No Python files found.[/yellow]")
        raise typer.Exit(code=0)

    modules = []
    for fp in files:
        try:
            modules.append(parse_python_file(fp))
        except Exception as e:
            print(f"[red]Failed to parse {fp}: {e}[/red]")

    print(f"[bold]Building Markdown[/bold] → {out_dir}")
    build_markdown(modules, out_dir)
    print("[green]Done.[/green] Open docs/index.md and docs/api.md")

def main():
    app()

if __name__ == "__main__":
    main()
