from textwrap import dedent

from src.highlight_identifiers import highlight_identifiers


def test_highlighting_identifiers():
    code = dedent(
        """
    def f():
        a
        b
        a
    """
    )

    colored = highlight_identifiers(code)

    assert colored == dedent(
        """
    def \x1b[38;5;196mf\x1b[0m():
        \x1b[38;5;46ma\x1b[0m
        \x1b[38;5;21mb\x1b[0m
        \x1b[38;5;46ma\x1b[0m
    """
    )


def test_highlighting_only_some_identifiers():
    code = """
    def f():
        a
        b
        c
    """

    colored = highlight_identifiers(code, only={"a", "b"})

    assert colored == dedent(
        """
    def f():
        \x1b[38;5;196ma\x1b[0m
        \x1b[38;5;154mb\x1b[0m
        c
    """
    )


def test_highlighting_params_only():
    code = """
    def f(a, b):
        a
        b
        c = lambda x: x + 1
    """

    colored = highlight_identifiers(code, params_only=True)

    assert colored == dedent(
        """
    def f(\x1b[38;5;196ma\x1b[0m, \x1b[38;5;190mb\x1b[0m):
        \x1b[38;5;196ma\x1b[0m
        \x1b[38;5;190mb\x1b[0m
        c = lambda \x1b[38;5;48mx\x1b[0m: \x1b[38;5;48mx\x1b[0m + 1
    """
    )


def test_highlighting_classes():
    code = """
    class A:
        class B: ...
    """

    colored = highlight_identifiers(code)

    assert colored == dedent(
        """
    class \x1b[38;5;196mA\x1b[0m:
        class \x1b[38;5;51mB\x1b[0m: ...
    """
    )


def test_highlighting_a_module():
    code = """
    x = 0
    
    class A: ...
    """

    colored = highlight_identifiers(code)

    assert colored == dedent(
        """
    \x1b[38;5;196mx\x1b[0m = 0
    
    class \x1b[38;5;51mA\x1b[0m: ...
    """
    )
