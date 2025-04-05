from dataclasses import dataclass
from textwrap import dedent

import parso
from parso.python.tree import Function

func = """
def fibonacci(n: int, memo: dict[int, int] = None) -> int:
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    result = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    memo[n] = result
    return result
"""


# ignore keywords, delimiters, operators


@dataclass(frozen=True)
class WordCount:
    word: str
    occurences: int
    span: int
    function_length: int


@dataclass(frozen=True)
class WordCounts:
    _word_counts: list[WordCount]


def test_1():
    code = dedent("""\
    def f(): return 0 
    """
    )
    p = parso.parse(code)
    function = p.children[0]
    assert word_counts(function) == WordCounts([])


def test_2():
    code = dedent("""\
    def id(x):
        return 0
    """
    )
    p = parso.parse(code)
    function = p.children[0]
    assert word_counts(function) == WordCounts([WordCount("x", 1, 1, 2)])


def test_3():
    code = dedent("""\
    def id(x):
        return x
    """)
    p = parso.parse(code)
    function = p.children[0]
    assert word_counts(function) == WordCounts([WordCount("x", 2, 2, 2)])


def word_counts(function: Function) -> WordCounts:
    func_len = function.end_pos[0] - function.start_pos[0]
    params = function.get_params()  # []
    word_count = {}
    word_line_start = {}
    word_line_end = {}
    for p in params:
        if p.name.value not in word_count:
            word_count[p.name.value] = 1
            word_line_start[p.name.value] = p.name.start_pos[0]
            word_line_end[p.name.value] = p.name.start_pos[0]
        else:
            word_count[p.name.value] += 1
            word_line_end[p.name.value] = p.name.start_pos[0]

    # for elt in function.children:
    return WordCounts(
        [
            WordCount(
                w,
                word_count[w],
                word_line_end[w] - word_line_start[w] + 1,
                func_len,
            )
            for w in word_count.keys()
        ]
    )
