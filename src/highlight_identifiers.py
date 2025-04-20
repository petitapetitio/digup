import ast
from collections import defaultdict
from textwrap import dedent
from typing import Optional, TypeAlias

from src.colorize import hue_gradient, colorize
from src.count_words import get_identifiers, IdentifierKind, Identifier

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

    return present_highlights(color_by_identifier, identifiers_by_line, source)


def present_highlights(color_by_identifier, identifiers_by_line: dict[int, list[Identifier]], source: str):
    output_lines = []
    for lineno, line in enumerate(source.splitlines(), start=1):
        if lineno not in identifiers_by_line:
            output_lines.append(line)
            continue

        output_line = line
        for identifier in reversed(identifiers_by_line[lineno]):
            highlighted_identifier = colorize(identifier.name, foreground=color_by_identifier[identifier.name])
            output_line = (
                output_line[: identifier.column]
                + highlighted_identifier
                + output_line[identifier.column + len(identifier.name) :]
            )
        output_lines.append(output_line)
    return "\n".join(output_lines) + "\n"
