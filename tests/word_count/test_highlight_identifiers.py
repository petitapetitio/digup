from textwrap import dedent

from src.get_functions import get_functions_from_source_code
from src.highlight_identifiers import highlight_identifiers


def test_highlighting_identifiers():
    code = dedent("""
    def f():
        a
        b
        a
    """)

    function = next(iter(get_functions_from_source_code(code)))
    colored = highlight_identifiers(function.source)

    assert colored == dedent(
        f"""\
    def f():
        \x1b[38;2;0;130;200ma\x1b[0m
        \x1b[38;2;60;180;75mb\x1b[0m
        \x1b[38;2;0;130;200ma\x1b[0m
    """
    )


def test_highlighting_only_some_identifiers():
    code = """
    def f():
        a
        b
        a
        c
    """

    colored = highlight_identifiers(code, {"a", "b"})

    assert colored == dedent(
        f"""
    def f():
        \x1b[38;2;0;130;200ma\x1b[0m
        \x1b[38;2;60;180;75mb\x1b[0m
        \x1b[38;2;0;130;200ma\x1b[0m
        c
    """
    )

