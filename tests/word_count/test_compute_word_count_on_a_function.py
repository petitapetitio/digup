import ast
from textwrap import dedent
from typing import cast

from src.count_words import word_count, WordCount, Word


def test_1():
    code = """\
    def f(): return 0 
    """
    assert _wc(code) == WordCount(
        [
            Word(word="f", occurences=1, span=1),
        ],
        length=1,
    )


def test_2():
    code = """\
    def id(x):
        return 0
    """
    assert _wc(code) == WordCount(
        [
            Word(word="id", occurences=1, span=1),
            Word(word="x", occurences=1, span=1),
        ],
        length=2,
    )


def test_3():
    code = """\
    def id(x):
        return x
    """
    assert _wc(code) == WordCount(
        [
            Word(word="id", occurences=1, span=1),
            Word(word="x", occurences=2, span=2),
        ],
        length=2,
    )


def test_4():
    code = """\
    def id(x, y=0, **args):
        return x
    """
    assert _wc(code) == WordCount(
        [
            Word(word="id", occurences=1, span=1),
            Word(word="x", occurences=2, span=2),
            Word(word="y", occurences=1, span=1),
            Word(word="args", occurences=1, span=1),
        ],
        length=2,
    )


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
    assert _wc(code) == WordCount(
        _word_counts=[
            Word(word="process_items", occurences=1, span=1),
            Word(word="items", occurences=3, span=6),
            Word(word="log", occurences=1, span=1),
            Word(word="item", occurences=4, span=5),
            Word(word="is_valid", occurences=1, span=1),
            Word(word="handle", occurences=1, span=1),
            Word(word="warn", occurences=1, span=1),
            Word(word="notify", occurences=1, span=1),
        ],
        length=11,
    )


def _wc(source: str) -> WordCount:
    tree = ast.parse(dedent(source))
    function = cast(ast.FunctionDef, tree.body[0])
    length = function.end_lineno - function.lineno + 1
    return word_count(function, length)
