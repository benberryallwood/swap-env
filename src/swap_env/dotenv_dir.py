from collections.abc import Generator
from pathlib import Path

DOTENV_DIR_NAME = ".swap-env"


def search_fs_for_dotenv_dir() -> Path:
    """Search for a dotenv dir from the CWD up to the home dir.

    If no dotenv dir is found, or if the CWD isn't inside the home dir, then
    this defaults to `~/.swap-env/`.
    """
    cwd = Path.cwd()
    home = Path.home()

    return next(
        (
            dotenv_dir
            for dir in iter_tree(cwd, home)
            if (dotenv_dir := dir.joinpath(DOTENV_DIR_NAME)).is_dir()
        ),
        home.joinpath(DOTENV_DIR_NAME),
    )


def iter_tree(start_dir: Path, end_dir: Path) -> Generator[Path, None, None]:
    """Return an iterator of paths from start_dir up to end_dir.

    If start_dir is not in end_dir, an empty iterator is returned.
    """
    if not start_dir.is_relative_to(end_dir):
        return

    current_dir = start_dir
    while current_dir != end_dir:
        yield current_dir
        current_dir = current_dir.parent
