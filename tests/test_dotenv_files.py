from pathlib import Path

import pytest

from swap_env.dotenv_files import DotenvFiles


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

    def test_link_overwritten_if_exists(self, tmp_path: Path, tmp_cwd: Path):
        (dotenv := tmp_path.joinpath(".env.one")).touch()
        (initial_link := tmp_path.joinpath("initial-link")).touch()

        dotenv_link = tmp_cwd.joinpath(".env")
        dotenv_link.symlink_to(initial_link)

        dotenv_files = DotenvFiles(tmp_path)
        dotenv_files.link("one")

        assert dotenv_link.samefile(dotenv)

    def test_file_overwritten_if_exists(self, tmp_path: Path, tmp_cwd: Path):
        (dotenv := tmp_path.joinpath(".env.one")).touch()
        (existing_dotenv := tmp_cwd.joinpath(".env")).touch()

        dotenv_files = DotenvFiles(tmp_path)
        dotenv_files.link("one")

        assert existing_dotenv.samefile(dotenv)

    def test_local_dotenv_file_saved(self, tmp_path: Path, tmp_cwd: Path):
        tmp_cwd.joinpath(".env").write_text("#dotenv")

        dotenv_files = DotenvFiles(tmp_path)
        dotenv_files.save_local_dotenv("name")

        assert tmp_path.joinpath(".env.name").read_text() == "#dotenv"
