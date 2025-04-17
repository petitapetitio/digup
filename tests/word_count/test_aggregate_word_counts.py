from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from src.count_words import Word, WordCount


@dataclass(frozen=True)
class Aggregate:
    counts: dict[str, int]

    @classmethod
    def of(cls, statement_word_counts: list[WordCount]) -> Aggregate:
        total = defaultdict(lambda: 0)
        for word_counts in statement_word_counts:
            for word_count in word_counts._word_counts:
                total[word_count.word] += word_count.occurences
        return Aggregate(total)


def test_sum_a_single_wordcounts():
    assert Aggregate.of([WordCount([Word("x", 1, 1)], 2)]) == Aggregate({"x": 1})


def test_sum_of_distinct_identifiers():
    assert Aggregate.of([WordCount([Word("x", 1, 1)], 2), WordCount([Word("y", 1, 1)], 2)]) == Aggregate(
        {"x": 1, "y": 1}
    )


def test_sum_of_same_identifier():
    assert Aggregate.of([WordCount([Word("x", 1, 1)], 2), WordCount([Word("x", 1, 1)], 2)]) == Aggregate({"x": 2})
