import pytest


@pytest.fixture(autouse=True)
def isolated_database(tmp_path, monkeypatch):
    monkeypatch.setenv("AI_DB_PATH", str(tmp_path / "test.sqlite3"))
