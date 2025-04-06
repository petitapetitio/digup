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


def test_selecting_a_function_that_doesnt_exist_return_an_empty_collection():
    assert list(select_function("x", Path("test_data/selecting_a_function"))) == []


def test_selecting_in_a_file_with_several_functions():
    functions = list(select_function("function_a", Path("test_data/selecting_a_function/1")))
    assert len(functions) == 1
    assert functions[0].name == "function_a"


def test_selecting_in_a_subdirectory():
    functions = list(select_function("function_a", Path("test_data/selecting_a_function/2")))
    assert len(functions) == 1
    assert functions[0].name == "function_a"


def test_selecting_a_method():
    functions = list(select_function("method_a", Path("test_data/selecting_a_function/3")))
    assert len(functions) == 1
    assert functions[0].name == "method_a"


def test_selecting_a_method_in_a_nested_class():
    functions = list(select_function("method_a", Path("test_data/selecting_a_function/4")))
    assert len(functions) == 1
    assert functions[0].name == "method_a"


def test_selecting_when_several_matches():
    functions = list(select_function("function_a", Path("test_data/selecting_a_function/5")))
    assert len(functions) == 2


def test_selecting_with_partial_match():
    functions = list(select_function("function", Path("test_data/selecting_a_function/6")))
    assert len(functions) == 1
    assert functions[0].name == "function_a"
