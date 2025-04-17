from textwrap import dedent

from src.format_as_string import present_word_count
from src.count_words import WordCount, Word


def test_display_word_count():
    produced = present_word_count(WordCount([Word("x", 1, 1)], 1))
    expected = dedent(
        """\
        ------------------------------------------------------------------------
        word                                             #      span  proportion
        ------------------------------------------------------------------------
        x                                                1         1        100%
        """
    )
    assert produced == expected
