from __future__ import annotations

from typing import Any, Protocol

from vibe.core.types import BaseEvent


class RemoteSessionUI(Protocol):
    async def on_remote_event(self, event: BaseEvent, loading_widget: Any) -> None: ...
    async def on_remote_waiting_input(self, event: Any) -> None: ...
    async def on_remote_user_message_cleared_input(self) -> None: ...
    async def on_remote_stream_error(self, error: str) -> None: ...
    async def on_remote_stream_ended(self, msg_type: str, text: str) -> None: ...
    async def on_remote_finalize_streaming(self) -> None: ...
    async def remove_loading(self) -> None: ...
    async def ensure_loading(self, status: str = "") -> None: ...
    @property
    def loading_widget(self) -> Any: ...


def is_progress_event(event: object) -> bool:
    return False


class RemoteSessionManager:
    def __init__(self) -> None:
        pass

    @property
    def is_active(self) -> bool:
        return False

    @property
    def is_terminated(self) -> bool:
        return True

    @property
    def is_waiting_for_input(self) -> bool:
        return False

    @property
    def has_pending_input(self) -> bool:
        return False

    @property
    def session_id(self) -> str | None:
        return None

    async def attach(self, session_id: str, config: Any) -> None:
        pass

    async def detach(self) -> None:
        pass

    def validate_input(self) -> str | None:
        return None

    async def send_prompt(self, message: str, *, require_source: bool = True) -> None:
        pass

    def cancel_pending_input(self) -> None:
        pass

    def build_question_args(self, event: Any) -> Any | None:
        return None

    def set_pending_input(self, event: Any) -> None:
        pass

    def start_stream(self, ui: RemoteSessionUI) -> None:
        pass

    async def stop_stream(self) -> None:
        pass

    def build_terminal_message(self) -> tuple[str, str]:
        return ("info", "Remote session completed")

    def cancel_stream_task(self) -> None:
        pass
