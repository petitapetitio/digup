from textwrap import dedent

import parso

from src.count_words import WordCount, WordCounts, word_counts


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
