import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Iterable


@dataclass(frozen=True)
class Function:
    definition: ast.FunctionDef
    location: str
    source: str

    @property
    def name(self):
        return self.definition.name


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, filepath: Path, pattern: Optional[str], source: str):
        self._class_stack = []
        self._filepath = filepath
        self._sourcefile = source.splitlines()
        self._pattern = pattern
        self._functions = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self._pattern is None or self._pattern in node.name:
            location = "::".join([self._filepath.name, *self._class_stack, node.name])
            source = "\n".join(self._sourcefile[node.lineno - 1 : node.end_lineno]) + "\n"
            self._functions.append(Function(node, location, source))

    @property
    def functions(self) -> list:
        return self._functions


def get_functions_from_paths(paths: list[Path], pattern: Optional[str] = None) -> Iterable[Function]:
    for path in paths:
        yield from get_functions_from_path(path, pattern)


def get_functions_from_path(folder: Path, pattern: Optional[str] = None) -> Iterable[Function]:
    for source_file in folder.glob("**/*.py"):
        with open(source_file) as f:
            file = f.read()
        yield from get_functions_from_source_code(file, pattern, source_file)


def get_functions_from_source_code(
    source: str, pattern: Optional[str] = None, filepath: Path = Path()
) -> Iterable[Function]:
    tree = ast.parse(source)
    visitor = FunctionVisitor(filepath, pattern, source)
    visitor.visit(tree)
    yield from visitor.functions
