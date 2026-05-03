from __future__ import annotations

from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.messages import NonSelectableStatic
from vibe.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic


class StatusMessage(NoMarkupStatic):
    def __init__(self, initial_text: str = "", **kwargs: Any) -> None:
        self._initial_text = initial_text
        self._indicator_widget: Static | None = None
        self._text_widget: NoMarkupStatic | None = None
        self.success = True
        self._is_spinning = True
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with Horizontal():
            self._indicator_widget = NonSelectableStatic(
                "...", classes="status-indicator-icon"
            )
            yield self._indicator_widget
            self._text_widget = NoMarkupStatic("", classes="status-indicator-text")
            yield self._text_widget

    def on_mount(self) -> None:
        self.update_display()

    def update_display(self) -> None:
        if not self._indicator_widget or not self._text_widget:
            return

        content = self.get_content()

        if self._is_spinning:
            self._indicator_widget.update("...")
            self._indicator_widget.remove_class("success")
            self._indicator_widget.remove_class("error")
        elif self.success:
            self._indicator_widget.update("✓")
            self._indicator_widget.add_class("success")
            self._indicator_widget.remove_class("error")
        else:
            self._indicator_widget.update("✕")
            self._indicator_widget.add_class("error")
            self._indicator_widget.remove_class("success")

        self._text_widget.update(content)

    def get_content(self) -> str:
        return self._initial_text

    def stop_spinning(self, success: bool = True) -> None:
        self._is_spinning = False
        self.success = success
        self.update_display()
