from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar, Iterable, Callable

from src.aggregation import Aggregation
from src.count_words import WordCount
from src.get_nodes import Node

TableItem = TypeVar("TableItem")


@dataclass(frozen=True)
class Table:
    columns: list[_Column]
    table_width: int

    @classmethod
    def of(cls, columns: list[_Column]) -> Table:
        table_width = sum(c.width for c in columns)
        return Table(columns, table_width)

    def present(self, words, param) -> str:
        res = ""
        res += self._separator()
        res += self._header()
        res += self._separator()
        res += self._body(words, param)
        return res

    def _header(self) -> str:
        return "".join(c.present_header() for c in self.columns) + "\n"

    def _separator(self) -> str:
        return "-" * self.table_width + "\n"

    def _body(self, item: Iterable[TableItem], item_to_tuple: Callable[[TableItem], tuple]):
        res = ""
        for word in item:
            line = "".join([c.present_value(v) for c, v in zip(self.columns, item_to_tuple(word))])
            res += line + "\n"
        return res


def present_word_count(word_count: WordCount) -> str:
    return Table.of(
        [
            _Column("word", 40, "<"),
            _Column("#", 10, ">"),
            _Column("span", 10, ">"),
            _Column("proportion", 12, ">", precision=".0", type="%"),
        ]
    ).present(
        word_count.words,
        lambda w: (w.word, w.occurences, w.span, w.span / word_count.length),
    )


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
    name: str
    width: int
    align: str
    precision: str = ""
    type: str = ""

    def present_header(self) -> str:
        return f"{self.name: {self.align}{self.width}}"

    def present_value(self, value: object):
        return f"{value: {self.align}{self.width}{self.precision}{self.type}}"

    def str_value(self, value: str) -> str:
        return f"{value: {self.align}{self.width}}"

    def int_value(self, value: int) -> str:
        return f"{value: {self.align}{self.width}}"

    def percentage(self, normalized_percentage: float) -> str:
        return f"{normalized_percentage: {self.align}{self.width}.0%}"
