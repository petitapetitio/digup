from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.aggregation import Aggregation
from src.count_words import WordCount
from src.get_nodes import Node


def present_word_count(word_count: WordCount) -> str:
    columns = {
        "word": _Column("word", 40, "<"),
        "occurences": _Column("#", 10, ">"),
        "span": _Column("span", 10, ">"),
        "proportion": _Column("proportion", 12, ">"),
    }

    header = "".join(c.present_header() for c in columns.values())
    array_width = sum(c.width for c in columns.values())

    res = ""
    res += "-" * array_width + "\n"
    res += header + "\n"
    res += "-" * array_width + "\n"

    for word in word_count.words:
        line = (
            columns["word"].str_value(word.word)
            + columns["occurences"].int_value(word.occurences)
            + columns["span"].int_value(word.span)
            + columns["proportion"].percentage(word.span / word_count.length)
        )
        res += line + "\n"

    return res


def present_aggregation(aggregation: Aggregation):
    columns = {"word": _Column("word", 40, "<"), "occurences": _Column("occurences", 10, ">")}

    header = "".join(c.present_header() for c in columns.values())
    array_width = sum(c.width for c in columns.values())

    res = ""
    res += "-" * array_width + "\n"
    res += header + "\n"
    res += "-" * array_width + "\n"

    for word, count in aggregation.counts():
        res += columns["word"].str_value(word) + columns["occurences"].int_value(count) + "\n"

    return res


@dataclass(frozen=True)
class LsItem:
    name: str
    length: int

    @classmethod
    def from_node(cls, node: Node, from_path: Path) -> LsItem:
        return LsItem(node.location_from(from_path), node.length)


def present_nodes(nodes: list[LsItem], kind: str):
    columns: dict[str, _Column] = {
        kind: _Column(kind, 110, "<"),
        "length": _Column("length", 10, ">"),
    }

    header = "".join(c.present_header() for c in columns.values())
    array_width = sum(c.width for c in columns.values())

    res = ""
    res += "-" * array_width + "\n"
    res += header + "\n"
    res += "-" * array_width + "\n"

    for line in nodes:
        res += columns[kind].str_value(line.name) + columns["length"].int_value(line.length) + "\n"

    return res


@dataclass(frozen=True)
class _Column:
    header: str
    width: int
    indent: str

    def present_header(self) -> str:
        return f"{self.header: {self.indent}{self.width}}"

    def str_value(self, value: str) -> str:
        return f"{value: {self.indent}{self.width}}"

    def int_value(self, value: int) -> str:
        return f"{value: {self.indent}{self.width}}"

    def percentage(self, normalized_percentage: float) -> str:
        return f"{normalized_percentage: {self.indent}{self.width}.0%}"
