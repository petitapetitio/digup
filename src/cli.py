from argparse import ArgumentParser
from pathlib import Path
from textwrap import dedent

from src.count_words import word_count
from src.format_as_string import present_word_count, present_aggregation
from src.highlight_identifiers import highlight_identifiers
from src.get_functions import get_functions, get_classes, get_modules
from src.aggregation import Aggregation

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
    parser.add_argument("--target", "-t", choices=["functions", "classes", "modules"], default="modules")
    parser.add_argument(
        "--search",
        "-s",
        nargs="?",
        default="",
        help=dedent("""\
        keep only nodes that with a location that match the 'search'.
        Location has form 'directory/subdirectory/file.py::ClassName::method_name'
        """),
    )

    args, remaining_args = parser.parse_known_args()
    command = args.command
    dirs = args.directory
    target = args.target

    match target:
        case "functions":
            nodes = get_functions(dirs, args.search)
        case "classes":
            nodes = get_classes(dirs, args.search)
        case _:  # "modules"
            nodes = get_modules(dirs, args.search)

    print()
    match command:
        case "wc":
            wc_parser = ArgumentParser()
            wc_parser.add_argument("--aggregate", action="store_true", default=False)
            wc_args = wc_parser.parse_args(remaining_args)
            if wc_args.aggregate:
                word_counts = [word_count(n.definition, n.length) for n in nodes]
                print(f"{len(word_counts)} {target}")
                print(present_aggregation(Aggregation.of(word_counts)))
            else:
                for node in nodes:
                    print(f"{node.location}")
                    print(present_word_count(word_count(node.definition, node.length).sorted_by_occurences()))
        case "hi":
            hi_parser = ArgumentParser()
            hi_parser.add_argument("--word", "-w", type=str, nargs="*", default=None)
            hi_parser.add_argument("--params-only", "-p", action="store_true", default=False)
            hi_args = hi_parser.parse_args(remaining_args)
            words = set(hi_args.word) if hi_args.word is not None else None

            for node in nodes:
                print(f"{node.location} ")
                print(highlight_identifiers(node.source, words, params_only=hi_args.params_only))


if __name__ == "__main__":
    main()
