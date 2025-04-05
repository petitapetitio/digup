from argparse import ArgumentParser
from pathlib import Path

if __name__ == "__main__":
    parser = ArgumentParser(
        usage=f"%(prog)s [options] [dir] [dir] [...]",
    )
    parser.add_argument("dir", type=Path, nargs="*")
    parser.add_argument("-k", required=False, help="Expression")

    args = parser.parse_args()

    print(args)
