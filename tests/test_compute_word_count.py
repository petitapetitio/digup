import ast
from textwrap import dedent
from typing import cast

from src.count_words import word_counts, WordCounts, WordCount


def test_1():
    code = """\
    def f(): return 0 
    """
    assert word_counts(_function(code)) == WordCounts([])


def test_2():
    code = """\
    def id(x):
        return 0
    """
    assert word_counts(_function(code)) == WordCounts([WordCount("x", 1, 1, 2)])


def test_3():
    code = """\
    def id(x):
        return x
    """
    assert word_counts(_function(code)) == WordCounts([WordCount("x", 2, 2, 2)])


def test_4():
    code = """\
    def id(x, y=0, **args):
        return x
    """
    assert word_counts(_function(code)) == WordCounts([
        WordCount("x", 2, 2, 2),
        WordCount("y", 1, 1, 2),
        WordCount("args", 1, 1, 2),
    ])


def test_a_complex_case():
    code = """\
    def process_items(items):
        if not items:
            log("No items to process.")
            return
    
        for item in items:
            if is_valid(item):
                handle(item)
            else:
                warn("Invalid item:", item)
        notify("Processing complete.")
    """
    assert word_counts(_function(code)) == WordCounts(
        [
            WordCount("items", 3, 6, 11),
            WordCount("log", 1, 1, 11),
            WordCount("item", 4, 5, 11),
            WordCount("is_valid", 1, 1, 11),
            WordCount("handle", 1, 1, 11),
            WordCount("warn", 1, 1, 11),
            WordCount("notify", 1, 1, 11),
        ]
    )


def _function(source: str) -> ast.FunctionDef:
    source = dedent(source)
    tree = ast.parse(source)
    return cast(ast.FunctionDef, tree.body[0])
