from pathlib import Path

import pytest


@pytest.fixture()
def tmp_cwd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path
