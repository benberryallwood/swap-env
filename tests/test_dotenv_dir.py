from pathlib import Path

from swap_env.dotenv_dir import iter_tree


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
