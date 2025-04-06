import ast
from pathlib import Path


def select_function(pattern: str, folder: Path):
    for source_file in folder.glob("**/*.py"):
        with open(source_file) as f:
            tree = ast.parse(f.read())
            print(tree)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and pattern in node.name:
                    yield node
