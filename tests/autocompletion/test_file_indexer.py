from __future__ import annotations

from collections.abc import Callable, Generator
from pathlib import Path
import time

import pytest

from vibe.core.autocompletion.file_indexer import FileIndexer


@pytest.fixture
def file_indexer() -> Generator[FileIndexer]:
    indexer = FileIndexer()
    yield indexer
    indexer.shutdown()


def _wait_for(condition: Callable[[], bool], timeout=3.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if condition():
            return True
        time.sleep(0.05)
    return False


def test_switching_between_roots_restarts_index(
    tmp_path: Path,
    tmp_path_factory: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
    file_indexer: FileIndexer,
) -> None:
    first_root = tmp_path
    second_root = tmp_path_factory.mktemp("second-root")
    (first_root / "first.py").write_text("", encoding="utf-8")
    (second_root / "second.py").write_text("", encoding="utf-8")

    monkeypatch.chdir(first_root)
    assert _wait_for(
        lambda: any(
            entry.rel == "first.py" for entry in file_indexer.get_index(Path("."))
        )
    )

    monkeypatch.chdir(second_root)
    assert _wait_for(
        lambda: all(
            entry.rel != "first.py" for entry in file_indexer.get_index(Path("."))
        )
    )
    assert _wait_for(
        lambda: any(
            entry.rel == "second.py" for entry in file_indexer.get_index(Path("."))
        )
    )


def test_shutdown_cleans_up_resources(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    (tmp_path / "test.txt").write_text("", encoding="utf-8")
    file_indexer = FileIndexer()
    file_indexer.get_index(Path("."))

    file_indexer.shutdown()
    assert file_indexer.get_index(Path(".")) == []
