from __future__ import annotations

import pytest

from vibe.cli.textual_ui.remote.remote_session_manager import RemoteSessionManager


@pytest.fixture
def manager() -> RemoteSessionManager:
    return RemoteSessionManager()


class TestProperties:
    def test_is_active_always_false(self, manager: RemoteSessionManager) -> None:
        assert manager.is_active is False

    def test_is_terminated_always_true(self, manager: RemoteSessionManager) -> None:
        assert manager.is_terminated is True

    def test_is_waiting_for_input_always_false(
        self, manager: RemoteSessionManager
    ) -> None:
        assert manager.is_waiting_for_input is False

    def test_has_pending_input_always_false(
        self, manager: RemoteSessionManager
    ) -> None:
        assert manager.has_pending_input is False

    def test_session_id_always_none(self, manager: RemoteSessionManager) -> None:
        assert manager.session_id is None
