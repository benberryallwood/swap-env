from pathlib import Path

import pytest

from swap_env.dotenv_dir import DOTENV_DIR_NAME, iter_tree, search_fs_for_dotenv_dir


@pytest.fixture
def tmp_home(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return tmp_path


class TestSearchFSForDotenvDir:
    def test_dotenv_dir_in_cwd_found(
        self, tmp_home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        (cwd := tmp_home.joinpath("current_dir")).mkdir()
        (dotenv_dir := cwd.joinpath(DOTENV_DIR_NAME)).mkdir()
        monkeypatch.chdir(cwd)

        assert search_fs_for_dotenv_dir() == dotenv_dir

    def test_dotenv_dir_in_intermediate_dir_found(
        self, tmp_home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        (mid_dir_one := tmp_home.joinpath("mid_dir_one")).mkdir()
        (mid_dir_two := mid_dir_one.joinpath("mid_dir_two")).mkdir()
        (cwd := mid_dir_two.joinpath("current_dir")).mkdir()
        (dotenv_dir := mid_dir_one.joinpath(DOTENV_DIR_NAME)).mkdir()
        monkeypatch.chdir(cwd)

        assert search_fs_for_dotenv_dir() == dotenv_dir

    def test_default_to_home_if_none_found(
        self, tmp_home: Path, monkeypatch: pytest.MonkeyPatch
    ):
        (mid_dir := tmp_home.joinpath("mid_dir_one")).mkdir()
        (cwd := mid_dir.joinpath("current_dir")).mkdir()
        monkeypatch.chdir(cwd)

        assert search_fs_for_dotenv_dir() == tmp_home.joinpath(DOTENV_DIR_NAME)

    def test_default_to_home_if_cwd_not_in_home(self, tmp_home: Path, tmp_cwd: Path):
        tmp_cwd.joinpath(DOTENV_DIR_NAME).mkdir()

        assert search_fs_for_dotenv_dir() == tmp_home.joinpath(DOTENV_DIR_NAME)


class TestIterTree:
    def test_empty_if_start_dir_not_in_end_dir(self, tmp_path: Path):
        (start_dir := tmp_path.joinpath("a")).mkdir()
        (end_dir := tmp_path.joinpath("b")).mkdir()

        assert list(iter_tree(start_dir, end_dir)) == []

    def test_empty_if_end_dir_in_start_dir(self, tmp_path: Path):
        (start_dir := tmp_path.joinpath("a")).mkdir()
        (end_dir := start_dir.joinpath("b")).mkdir()

        assert list(iter_tree(start_dir, end_dir)) == []

    def test_start_dir_returned_if_directly_in_end_dir(self, tmp_path: Path):
        (end_dir := tmp_path.joinpath("a")).mkdir()
        (start_dir := end_dir.joinpath("b")).mkdir()

        assert list(iter_tree(start_dir, end_dir)) == [start_dir]

    def test_correct_dirs_returned_when_nested(self, tmp_path: Path):
        (end_dir := tmp_path.joinpath("a")).mkdir()
        (third_dir := end_dir.joinpath("b")).mkdir()
        (second_dir := third_dir.joinpath("c")).mkdir()
        (start_dir := second_dir.joinpath("d")).mkdir()

        third_dir.joinpath("irrelevant").mkdir()

        assert list(iter_tree(start_dir, end_dir)) == [start_dir, second_dir, third_dir]
