from argparse import ArgumentParser
from pathlib import Path

from src.count_words import word_counts
from src.format_as_string import as_string
from src.highlight_identifiers import highlight_identifiers
from src.get_functions import get_functions_from_paths


def main():
    parser = ArgumentParser(
        usage=f"%(prog)s [options] COMMAND",
    )
    parser.add_argument("command")
    parser.add_argument("--directory", "-d", type=Path, nargs="*", default=[Path()])
    parser.add_argument("--function", "-f", required=False, help="function")

    args = parser.parse_args()

    command = args.command

    dirs = args.directory

    functions = get_functions_from_paths(dirs, args.function)

    match command:
        case "wc":
            for function in functions:
                print(f"{function.location}: ")
                print(as_string(word_counts(function.definition).sorted_by_occurences()))
        case "hi":
            for function in functions:
                print(f"{function.location}: ")
                print(highlight_identifiers(function.source))


if __name__ == "__main__":
    main()
