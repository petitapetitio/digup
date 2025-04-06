import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Iterable


@dataclass(frozen=True)
class Function:
    definition: ast.FunctionDef
    location: str

    @property
    def name(self):
        return self.definition.name


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, source_file: str, pattern: Optional[str]):
        self._class_stack = []
        self._source_file = source_file
        self._pattern = pattern
        self._functions = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self._pattern is None or self._pattern in node.name:
            location = "::".join([self._source_file, *self._class_stack, node.name])
            self._functions.append(Function(node, location))

    @property
    def functions(self):
        return self._functions


def get_functions(folder: Path, pattern: Optional[str] = None) -> Iterable[Function]:
    for source_file in folder.glob("**/*.py"):
        with open(source_file) as f:
            tree = ast.parse(f.read())

            visitor = FunctionVisitor(source_file.name, pattern)
            visitor.visit(tree)
            yield from visitor.functions
