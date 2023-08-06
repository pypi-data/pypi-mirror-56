from pathlib import Path
from subprocess import run
import sys

DOC_PATH = Path("doc")
BUILD_PATH = DOC_PATH / "_build"


def build() -> None:
    if not DOC_PATH.exists():
        print("No 'doc/' directory found. Create one with 'phink init'.")
        sys.exit(1)

    print("Running Sphinx build...")
    if run(["sphinx-build", DOC_PATH, BUILD_PATH, "-q"]).returncode == 0:
        print(f"Built HTML to: {BUILD_PATH}")
    else:
        print(f"ERROR: Sphinx build failed")
