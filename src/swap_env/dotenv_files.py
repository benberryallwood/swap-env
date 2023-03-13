from pathlib import Path
from typing import Iterator


class DotenvFiles:
    """Collection of .env files named `.env.<name>` to be linked to from the cwd.

    On initialisation, a directory is created at the given path if it doesn't
    exist. All files in the given directory named `.env.*` are picked up and can
    be accessed by their name, given by the part after `.env.`.

    Example usage::

        >>> dotenv_files = DotenvFiles(pathlib.Path.home())

        >>> dotenv_files.save_local_dotenv("test")

        >>> list(dotenv_files)
        ['dev', 'test']

        >>> # Link ./.env to ~/.env.dev
        >>> dotenv_files.link("dev")
    """

    def __init__(self, path: Path):
        if not path.exists():
            path.mkdir()
        if not path.is_dir():
            raise ValueError("Path must be a directory")

        self._path = path
        self._load()

    def _load(self) -> None:
        """Load .env files with names given by their suffix."""
        self._files = {
            filename.removeprefix(".env."): file
            for file in self._path.iterdir()
            if (filename := file.name).startswith(".env.")
        }

    def __iter__(self) -> Iterator[str]:
        """Return an alphabetically sorted iterator of .env file nicknames."""
        return iter(sorted(self._files))

    def __getitem__(self, name: str) -> Path:
        """Return the path of the .env file with the nickname `name`."""
        return self._files[name]

    def __bool__(self) -> bool:
        """Return `True` iff there are files named `.env.*` in the given dir."""
        return bool(self._files)

    def link(self, name: str) -> None:
        """Create symlink from ./.env to the dotenv file with the given name."""
        dotenv = Path.cwd().joinpath(".env")
        dotenv.unlink(missing_ok=True)
        dotenv.symlink_to(self._files[name])

    def save_local_dotenv(self, name: str) -> None:
        """Save ./.env to the store with the given name."""
        local_dotenv_path = Path.cwd().joinpath(".env")
        new_path = local_dotenv_path.rename(self._path.joinpath(f".env.{name}"))
        self._files[name] = new_path
