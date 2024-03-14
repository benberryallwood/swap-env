from collections.abc import Iterator
from pathlib import Path


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

    DOTENV_FILE_PREFIX = ".env."

    def __init__(self, path: Path):
        if not path.exists():
            path.mkdir()
        if not path.is_dir():
            raise ValueError("Path must be a directory")

        self.path = path
        self._local_dotenv = Path.cwd().joinpath(".env")
        self._load()

    def _load(self) -> None:
        """Load .env files with names given by their suffix."""
        self._files = {
            file.name.removeprefix(self.DOTENV_FILE_PREFIX): file
            for file in self.path.iterdir()
            if file.name.startswith(self.DOTENV_FILE_PREFIX)
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
        self._local_dotenv.unlink(missing_ok=True)
        self._local_dotenv.symlink_to(self._files[name])

    def save_local_dotenv(self, name: str) -> None:
        """Save ./.env to the store with the given name."""
        new_path = self._local_dotenv.rename(
            self.path.joinpath(f"{self.DOTENV_FILE_PREFIX}{name}")
        )
        self._files[name] = new_path
