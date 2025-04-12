from argparse import ArgumentParser
from pathlib import Path

from src.count_words import word_counts
from src.format_as_string import as_string
from src.highlight_identifiers import highlight_identifiers
from src.get_functions import get_functions_from_paths

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
    parser.add_argument(
        "--function",
        "-f",
        required=False,
        help="Apply only to functions that match",
    )

    args, unknown = parser.parse_known_args()

    command = args.command

    dirs = args.directory

    functions = get_functions_from_paths(dirs, args.function)

    print()
    match command:
        case "wc":
            for function in functions:
                print(f"{function.location}: ")
                print(as_string(word_counts(function.definition).sorted_by_occurences()))
        case "hi":
            hi_parser = ArgumentParser()
            hi_parser.add_argument("--word", "-w", type=str, nargs="*", default=None)
            hi_parser.add_argument("--params-only", "-p", action="store_true", default=False)
            hi_args = hi_parser.parse_args(unknown)
            words = set(hi_args.word) if hi_args.word is not None else None

            for function in functions:
                print(f"{function.location}: ")
                print(highlight_identifiers(function.source, words, params_only=hi_args.params_only))


if __name__ == "__main__":
    main()
