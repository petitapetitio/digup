from pathlib import Path

from src.select_function import get_functions


def test_selecting_all_functions():
    functions = list(get_functions(Path("test_data/selecting_a_function/all_functions")))
    assert len(functions) == 2
    assert functions[0].name == "function_a"
    assert functions[1].name == "function_b"


def test_selecting_a_function_that_doesnt_exist_return_an_empty_collection():
    assert list(get_functions(Path("test_data/selecting_a_function"), "x")) == []


def test_selecting_in_a_file_with_several_functions():
    functions = list(get_functions(Path("test_data/selecting_a_function/one_among_several"), "function_a"))
    assert len(functions) == 1
    assert functions[0].name == "function_a"


def test_selecting_in_a_subdirectory():
    functions = list(get_functions(Path("test_data/selecting_a_function/within_a_subdirectory"), "function_a"))
    assert len(functions) == 1
    assert functions[0].name == "function_a"


def test_selecting_a_method():
    functions = list(get_functions(Path("test_data/selecting_a_function/in_a_class"), "method_a"))
    assert len(functions) == 1
    assert functions[0].name == "method_a"


def test_selecting_a_method_in_a_nested_class():
    functions = list(get_functions(Path("test_data/selecting_a_function/in_a_nested_class"), "method_a"))
    assert len(functions) == 1
    assert functions[0].name == "method_a"


def test_selecting_when_several_matches():
    functions = list(get_functions(Path("test_data/selecting_a_function/with_several_matches"), "function_a"))
    assert len(functions) == 2


def test_selecting_with_partial_match():
    functions = list(get_functions(Path("test_data/selecting_a_function/with_partial_match"), "function"))
    assert len(functions) == 1
    assert functions[0].name == "function_a"
