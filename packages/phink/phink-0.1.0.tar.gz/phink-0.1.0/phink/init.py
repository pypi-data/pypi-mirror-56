from pathlib import Path
import sys
from typing import Optional


def init() -> None:
    doc_path = Path("doc")
    if doc_path.exists():
        print("'doc/' directory already exists.")
        sys.exit(1)
    create_dirs(doc_path)

    data = Data.get_user_input()
    data.doc_path = doc_path
    create_readme_symlink(data)
    apply_template("conf.py", data)
    apply_template("index.rst", data)
    apply_template("customising.md", data)
    apply_template("commands.md", data)
    apply_template("api.md", data)

    print()
    print(f"Documentation source has been written to '{doc_path}/'.")
    print("Please edit it as you wish.")
    print("Use 'phink serve' to view your docs in your browser.")


def create_dirs(doc_path: Path) -> None:
    doc_path.mkdir()
    (doc_path / "_static").mkdir()


class Data:
    doc_path: Path
    project: str
    project_section_underline: str

    @classmethod
    def get_user_input(cls) -> "Data":
        data = cls()
        data.project = cls.ask("Project name")
        data.project_section_underline = "=" * len(data.project)
        return data

    @staticmethod
    def ask(question: str) -> str:
        answer = input(f"{question}: ")
        if answer == "":
            print("No answer given - aborting.")
            sys.exit(1)
        return answer

    def __getattr__(self, name: str) -> str:
        if name.startswith("_section_underline_"):
            return "=" * len(getattr(self, name[19:]))

        raise AttributeError


def create_readme_symlink(data: Data) -> None:
    readme_source_path = data.doc_path / ".." / "README.md"
    if not readme_source_path.exists():
        apply_template("README.md", data, output_path=(data.doc_path / ".."))

    symlink = data.doc_path / "README.md"
    symlink.symlink_to(Path("..") / "README.md")


def apply_template(
    template_name: str, data: Data, output_path: Optional[Path] = None
) -> None:
    if output_path is None:
        output_path = data.doc_path
    template_path = Path(__file__).parent / "templates" / template_name
    template = template_path.read_text()
    text = template.format(data=data)
    (output_path / template_name).write_text(text)
