from dataclasses import dataclass
from textwrap import dedent
from typing import NamedTuple

from src.word_count import WordCounts, WordCount


@dataclass(frozen=True)
class ColumnSpec:
    header: str
    width: int
    indent: str

    def string(self) -> str:
        return f"{self.header: {self.indent}{self.width}}"

    def str_value(self, value: str) -> str:
        return f"{value: {self.indent}{self.width}}"

    def int_value(self, value: int) -> str:
        return f"{value: {self.indent}{self.width}}"

    def percentage(self, normalized_percentage: float) -> str:
        return f"{normalized_percentage: {self.indent}{self.width}.0%}"


def as_string(word_counts: WordCounts) -> str:
    columns = {
        "word": ColumnSpec("word", 20, "<"),
        "occurences": ColumnSpec("#", 10, ">"),
        "span": ColumnSpec("span", 10, ">"),
        "proportion": ColumnSpec("proportion", 12, ">"),
    }

    header = "".join(c.string() for c in columns.values())
    array_width = sum(c.width for c in columns.values())

    res = "\n"
    res += header + "\n"
    res += "-" * array_width + "\n"
    for wc in word_counts._word_counts:
        line = (
            columns["word"].str_value(wc.word)
            + columns["occurences"].int_value(wc.occurences)
            + columns["span"].int_value(wc.span)
            + columns["proportion"].percentage(wc.span / wc.function_length)
        )
        res += line + "\n"
    return res


def test_display_word_count():
    string = as_string(WordCounts([WordCount("x", 1, 1, 1)]))
    print(string)
    expected = dedent(
        """
        word                         #      span  proportion
        ----------------------------------------------------
        x                            1         1        100%
        """
    )
    assert string == expected
