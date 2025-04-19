import ast
from collections import defaultdict
from textwrap import dedent
from typing import Optional, TypeAlias

from src.color import hue_gradient, colorize
from src.count_words import get_identifiers, IdentifierKind

RGBColor: TypeAlias = tuple[int, int, int]


def highlight_identifiers(
    code: str,
    only: Optional[set[str]] = None,
    params_only: bool = False,
) -> str:
    # TODO : je parse le code plusieurs fois ici, c'est un peu bête
    source = dedent(code)
    tree = ast.parse(source)

    color_by_identifier = {}
    identifiers_by_line: dict[int, list] = defaultdict(list)
    sorted_identifiers = sorted(get_identifiers(tree), key=lambda idtf: (idtf.lineno, idtf.column))

    colors_iterator = hue_gradient(len({i.name for i in sorted_identifiers}))

    for identifier in sorted_identifiers:
        if only is not None and identifier.name not in only:
            continue
        if params_only and identifier.kind != IdentifierKind.ARG and identifier.name not in color_by_identifier:
            continue

        if identifier.name not in color_by_identifier:
            color_by_identifier[identifier.name] = next(colors_iterator)
        identifiers_by_line[identifier.lineno].append(identifier)
    highlighted_lines = []

    for lineno, line in enumerate(source.splitlines(), start=1):
        if lineno not in identifiers_by_line:
            highlighted_lines.append(line)
            continue

        highlighted_line = line
        for identifier in reversed(identifiers_by_line[lineno]):
            highlighted_identifier = colorize(identifier.name, foreground=color_by_identifier[identifier.name])
            highlighted_line = (
                highlighted_line[: identifier.column]
                + highlighted_identifier
                + highlighted_line[identifier.column + len(identifier.name) :]
            )
        highlighted_lines.append(highlighted_line)

    return "\n".join(highlighted_lines) + "\n"
