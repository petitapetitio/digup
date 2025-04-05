from dataclasses import dataclass
from textwrap import dedent

import parso
from parso.python.tree import Function, PythonNode
from parso.tree import NodeOrLeaf


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


def test_a_complex_case():
    code = dedent("""\
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
    """)
    p = parso.parse(code)
    function = p.children[0]
    assert word_counts(function) == WordCounts([
        WordCount("items", 3, 6, 11),
        WordCount("log", 1, 1, 11),
        WordCount("item", 4, 5, 11),
        WordCount("is_valid", 1, 1, 11),
        WordCount("handle", 1, 1, 11),
        WordCount("warn", 1, 1, 11),
        WordCount("notify", 1, 1, 11),
    ])


def get_identifiers(node: NodeOrLeaf):
    if node.type == "name":
        yield node
    if hasattr(node, "children"):
        for child in node.children:
            yield from get_identifiers(child)


def word_counts(function: Function) -> WordCounts:
    func_len = function.end_pos[0] - function.start_pos[0]
    word_count = {}
    word_line_start = {}
    word_line_end = {}

    names = get_identifiers(function)
    for name in names:
        if name.parent.type == "funcdef":
            continue
        if name.value not in word_count:
            word_count[name.value] = 1
            word_line_start[name.value] = name.start_pos[0]
            word_line_end[name.value] = name.start_pos[0]
        else:
            word_count[name.value] += 1
            word_line_end[name.value] = name.start_pos[0]

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
