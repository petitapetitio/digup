import ast
from collections import defaultdict
from textwrap import dedent
from typing import cast, Optional

from src.count_words import get_identifiers
from src.termcolor import colored


DISTINCT_RGB_COLORS = [
    (0, 130, 200),  # Blue
    (60, 180, 75),  # Green
    (230, 25, 75),  # Red
    (245, 130, 48),  # Orange
    (145, 30, 180),  # Purple
    (70, 240, 240),  # Cyan
    (240, 50, 230),  # Magenta
    (210, 245, 60),  # Lime
    (250, 190, 190),  # Pink
    (0, 128, 128),  # Teal
    (230, 190, 255),  # Lavender
    (170, 110, 40),  # Brown
    (255, 250, 200),  # Light Yellow
    (128, 0, 0),  # Maroon
    (170, 255, 195),  # Mint
    (128, 128, 0),  # Olive
    (255, 215, 180),  # Apricot
    (0, 0, 128),  # Navy
    (128, 128, 128),  # Grey
    (255, 255, 255),  # White
    (0, 0, 0),  # Black
    (255, 255, 0),  # Yellow
    (255, 153, 204),  # Bubblegum
    (102, 51, 153),  # Deep Purple
] + [(125, 125, 125)] * 1000


def highlight_identifiers(code: str, only: Optional[set[str]] = None) -> str:
    source = dedent(code)
    tree = ast.parse(source)
    f = cast(ast.FunctionDef, tree.body[0])
    colors = iter(DISTINCT_RGB_COLORS)

    color_by_identifier = {}
    identifiers_by_line: dict[int, list] = defaultdict(list)
    sorted_identifiers = sorted(get_identifiers(f), key=lambda idtf: (idtf.lineno, -idtf.column))
    for identifier in sorted_identifiers:
        if only is not None and identifier.name not in only:
            continue
        if identifier.name not in color_by_identifier:
            color = next(colors)
            color_by_identifier[identifier.name] = color
        identifiers_by_line[identifier.lineno].append(identifier)
    highlighted_lines = []

    for lineno, line in enumerate(source.splitlines(), start=1):
        if lineno not in identifiers_by_line:
            highlighted_lines.append(line)
            continue

        highlighted_line = line
        for identifier in identifiers_by_line[lineno]:
            highlighted_identifier = colored(
                identifier.name, color=color_by_identifier[identifier.name], force_color=True
            )
            highlighted_line = (
                highlighted_line[: identifier.column]
                + highlighted_identifier
                + highlighted_line[identifier.column + len(identifier.name) :]
            )
        highlighted_lines.append(highlighted_line)

    return "\n".join(highlighted_lines) + "\n"
