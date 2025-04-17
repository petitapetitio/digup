from argparse import ArgumentParser
from pathlib import Path

from src.count_words import word_count
from src.format_as_string import as_string
from src.highlight_identifiers import highlight_identifiers
from src.get_functions import get_functions, get_classes, get_modules

USAGE = f"""\
%(prog)s COMMAND [options]

A cli-tool that helps you dig up knowledge from Python legacy code.

Commands:
  hi          Highlight the identifiers in functions
  wc          Count the words in functions
"""


def main():
    parser = ArgumentParser(
        usage=USAGE,
        add_help=True,
    )
    parser.add_argument("command")
    parser.add_argument(
        "--directory",
        "-d",
        type=Path,
        nargs="*",
        default=[Path()],
        help="Apply only to modules in these directories",
    )
    parser.add_argument("--target", "-t", choices=["function", "class"])
    parser.add_argument(
        "--search",
        "-s",
        nargs="?",
        default="",
        help="keep only nodes that match this location pattern",
    )

    args, remaining = parser.parse_known_args()
    command = args.command
    dirs = args.directory
    target = args.target

    match target:
        case "function":
            nodes = get_functions(dirs, args.search)
        case "class":
            nodes = get_classes(dirs, args.search)
        case _:
            nodes = get_modules(dirs, args.search)

    print()
    match command:
        case "wc":
            for node in nodes:
                print(f"{node.location} ")
                print(as_string(word_count(node.definition, node.length).sorted_by_occurences()))
        case "hi":
            hi_parser = ArgumentParser()
            hi_parser.add_argument("--word", "-w", type=str, nargs="*", default=None)
            hi_parser.add_argument("--params-only", "-p", action="store_true", default=False)
            hi_args = hi_parser.parse_args(remaining)
            words = set(hi_args.word) if hi_args.word is not None else None

            for node in nodes:
                print(f"{node.location} ")
                print(highlight_identifiers(node.source, words, params_only=hi_args.params_only))


if __name__ == "__main__":
    main()
