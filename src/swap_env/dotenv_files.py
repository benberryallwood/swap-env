from pathlib import Path

class DotenvFiles:
    def __init__(self):
        self._path = Path.home().joinpath(".swap_env")
        self._load()

    def _load(self):
        """Load dotenv files at ~/.swap_env/ with names given by their suffix.

        Creates the directory ~/.swap_env/ if it doesn't exist.
        """
        if not self._path.exists():
            self._path.mkdir()
        self._files = {
            file.suffix.removeprefix("."): file
            for file in self._path.iterdir()
        }

    def __iter__(self):
        return iter(sorted(self._files))

    def __getitem__(self, name):
        return self._files[name]

    def link(self, name: str):
        """Create symlink from ./.env to the dotenv file with the given name."""
        dotenv = Path.cwd().joinpath(".env")
        dotenv.unlink(missing_ok=True)

        dotenv.symlink_to(self._files[name])
