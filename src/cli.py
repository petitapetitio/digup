from argparse import ArgumentParser
from pathlib import Path

from src.count_words import word_counts
from src.format_as_string import as_string
from src.select_function import get_functions


def main():
    parser = ArgumentParser(
        usage=f"%(prog)s [options] [dir] [dir] [...]",
    )
    parser.add_argument("dir", type=Path, nargs="*")
    parser.add_argument("-f", required=False, help="function")

    args = parser.parse_args()

    dirs = args.dir
    if len(dirs) == 0:
        dirs.append(Path())

    functions = get_functions(dirs[0], args.f)
    for function in functions:
        print(as_string(word_counts(function)))


if __name__ == "__main__":
    main()
