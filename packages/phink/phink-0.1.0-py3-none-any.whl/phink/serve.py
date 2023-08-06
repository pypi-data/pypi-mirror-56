from livereload import Server

from .build import build, BUILD_PATH


def serve() -> None:
    build()

    server = Server()
    server.watch("**/*", build, ignore=check_ignore)
    server.serve(root=BUILD_PATH)


def check_ignore(path: str) -> bool:
    return path.startswith(str(BUILD_PATH))
