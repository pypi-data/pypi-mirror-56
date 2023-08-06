import sys
from typing import List

from .init import init
from .build import build
from .serve import serve


def main(args: List[str] = sys.argv[1:]) -> None:
    if args == []:
        args = ["build"]

    command = args[0]
    if command == "init":
        init()
    elif command == "build":
        build()
    elif command == "serve":
        serve()
    else:
        print(f"Invalid command: {command}")
        sys.exit(1)
