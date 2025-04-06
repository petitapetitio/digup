from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class WordCount:
    word: str
    occurences: int
    span: int
    function_length: int


@dataclass(frozen=True)
class WordCounts:
    _word_counts: list[WordCount]


@dataclass(frozen=True)
class Identifier:
    name: str
    lineno: int
    column: int


def get_identifiers(node: ast.FunctionDef) -> Iterable[Identifier]:
    for child in ast.walk(node):
        if isinstance(child, ast.arg):
            yield Identifier(child.arg, child.lineno, child.col_offset)
        if isinstance(child, ast.Name):
            yield Identifier(child.id, child.lineno, child.col_offset)


def word_counts(function: ast.FunctionDef) -> WordCounts:
    func_len = function.end_lineno - function.lineno + 1
    word_count = {}
    word_line_start = {}
    word_line_end = {}

    for identifier in sorted(get_identifiers(function), key=lambda idf: (idf.lineno, idf.column)):
        name_encountered_for_the_first_time = identifier.name not in word_count
        if name_encountered_for_the_first_time:
            word_count[identifier.name] = 1
            word_line_start[identifier.name] = identifier.lineno
            word_line_end[identifier.name] = identifier.lineno
        else:
            word_count[identifier.name] += 1
            word_line_end[identifier.name] = identifier.lineno

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