from textwrap import dedent

from src.format_as_string import as_string
from src.count_words import WordCounts, WordCount


def test_display_word_count():
    produced = as_string(WordCounts([WordCount("x", 1, 1, 1)]))
    expected = dedent(
        """\
        ------------------------------------------------------------------------
        word                                             #      span  proportion
        ------------------------------------------------------------------------
        x                                                1         1        100%
        """
    )
    assert produced == expected
