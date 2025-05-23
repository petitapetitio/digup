from textwrap import dedent

from digup.present import present_word_count
from digup.count_words import WordCount, Word


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
