from pathlib import Path


class DotenvFiles:
    def __init__(self, path: Path):
        if not path.exists():
            path.mkdir()
        if not path.is_dir():
            raise ValueError("Path must be a directory")

        self._path = path
        self._load()

    def _load(self):
        """Load dotenv files with names given by their suffix."""
        self._files = {
            filename.removeprefix(".env."): file
            for file in self._path.iterdir()
            if (filename := file.name).startswith(".env.")
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
