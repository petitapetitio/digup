import ast
from pathlib import Path
from typing import Optional


def get_functions(folder: Path, pattern: Optional[str] = None):
    for source_file in folder.glob("**/*.py"):
        with open(source_file) as f:
            tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if pattern is None or pattern in node.name:
                        yield node
