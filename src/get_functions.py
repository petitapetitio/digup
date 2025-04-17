import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Iterable


@dataclass(frozen=True)
class Node:
    definition: ast.AST
    source: str
    filepath: Path
    class_stack: list[str]
    name: str
    length: int

    @property
    def location(self) -> str:
        return self._present_location(self.filepath.name)

    def location_from(self, path: Path) -> str:
        return self._present_location(str(self.filepath.relative_to(path)))

    def _present_location(self, root: str) -> str:
        location = "::".join([root, *self.class_stack, self.name])
        location = location.removesuffix("::")  # hack for the modules
        return location




class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, filepath: Path, search: str, source: str):
        self._class_stack = []
        self._filepath = filepath
        self._sourcefile = source.splitlines()
        self._search = search
        self._functions = []
        self._classes = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        self.generic_visit(node)
        self._class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self._search is None or self._search in node.name:
            source = "\n".join(self._sourcefile[node.lineno - 1 : node.end_lineno]) + "\n"
            length = node.end_lineno - node.lineno + 1
            self._functions.append(Node(node, source, self._filepath, list(self._class_stack), node.name, length))

    @property
    def functions(self) -> list:
        return self._functions


class ClassesVisitor(ast.NodeVisitor):
    def __init__(self, filepath: Path, search: Optional[str], source: str):
        self._class_stack = []
        self._filepath = filepath
        self._sourcefile = source.splitlines()
        self._search = search
        self._classes = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self._class_stack.append(node.name)
        if self._search is None or self._search in node.name:
            source = "\n".join(self._sourcefile[node.lineno - 1 : node.end_lineno]) + "\n"
            length = node.end_lineno - node.lineno + 1
            self._classes.append(Node(node, source, self._filepath, list(self._class_stack), node.name, length))
        self.generic_visit(node)
        self._class_stack.pop()

    @property
    def classes(self) -> list[Node]:
        return self._classes


def get_modules(paths: list[Path], search: str):
    for path in paths:
        for filepath in path.glob("**/*.py"):
            if search not in str(filepath):
                continue
            with open(filepath) as f:
                source_code = f.read()
                module = ast.parse(source_code)
                length = module.body[-1].end_lineno - module.body[0].lineno + 1 if len(module.body) > 0 else 0
                yield Node(module, source_code, filepath, [], "", length)

    return []


def get_classes(paths: list[Path], search: str) -> Iterable[Node]:
    for folder in paths:
        for filepath in folder.glob("**/*.py"):
            with open(filepath) as f:
                source_code = f.read()
            module = ast.parse(source_code)
            visitor = ClassesVisitor(filepath, search, source_code)
            visitor.visit(module)
            nodes = visitor.classes
            yield from nodes

    return []


def get_functions(paths: list[Path], search: str = "") -> Iterable[Node]:
    for folder in paths:
        for filepath in folder.glob("**/*.py"):
            with open(filepath) as f:
                source = f.read()
            module = ast.parse(source)
            visitor = FunctionVisitor(filepath, search, source)
            visitor.visit(module)
            yield from visitor.functions

    return []
