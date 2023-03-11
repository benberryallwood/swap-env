from pathlib import Path
import pytest

from swap_env.dotenv_files import DotenvFiles


@pytest.fixture()
def tmp_cwd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestDotenvFiles:
    def test_value_error_raised_given_a_file(self, tmp_path: Path):
        (filepath := tmp_path.joinpath("file")).touch()

        with pytest.raises(ValueError, match="Path must be a directory"):
            DotenvFiles(path=filepath)

    def test_dir_created_if_not_exists(self, tmp_path: Path):
        path = tmp_path.joinpath("dir")

        DotenvFiles(path=path)
        assert path.is_dir()

    def test_dotenv_files_loaded_with_suffix_names(self, tmp_path: Path):
        (file_one := tmp_path.joinpath(".env.one")).touch()
        (file_two := tmp_path.joinpath(".env.two")).touch()

        dotenv_files = DotenvFiles(path=tmp_path)
        assert dotenv_files._files == {"one": file_one, "two": file_two}

    def test_files_without_dotenv_prefix_ignored(self, tmp_path: Path):
        (file_one := tmp_path.joinpath(".env.one")).touch()
        tmp_path.joinpath(".two").touch()

        dotenv_files = DotenvFiles(path=tmp_path)
        assert dotenv_files._files == {"one": file_one}

    def test_link_created_in_cwd(self, tmp_path: Path, tmp_cwd: Path):
        (dotenv := tmp_path.joinpath(".env.one")).touch()
        dotenv_files = DotenvFiles(tmp_path)
        dotenv_files.link("one")

        dotenv_link = tmp_cwd.joinpath(".env")
        assert dotenv_link.samefile(dotenv)
