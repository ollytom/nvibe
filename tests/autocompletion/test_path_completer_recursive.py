from __future__ import annotations

from pathlib import Path

import pytest

from vibe.core.autocompletion.completers import PathCompleter


@pytest.fixture()
def file_tree(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    (tmp_path / "vibe" / "cli" / "autocompletion").mkdir(parents=True)
    (tmp_path / "vibe" / "cli" / "autocompletion" / "fuzzy.py").write_text("")
    (tmp_path / "vibe" / "cli" / "autocompletion" / "completers.py").write_text("")
    (tmp_path / "tests" / "autocompletion").mkdir(parents=True)
    (tmp_path / "tests" / "autocompletion" / "test_fuzzy.py").write_text("")
    (tmp_path / "README.md").write_text("")
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_finds_multiple_matches_recursively(file_tree: Path) -> None:
    results = PathCompleter().get_completions("@fuzzy", cursor_pos=6)

    vibe_index = results.index("@vibe/cli/autocompletion/fuzzy.py")
    test_index = results.index("@tests/autocompletion/test_fuzzy.py")
    assert vibe_index < test_index
