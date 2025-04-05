from dataclasses import dataclass

from parso.python.tree import Function, Name
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


def get_identifiers(node: NodeOrLeaf):
    if node.type == Name.type:
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
        if name.parent.type == Function.type:
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