from __future__ import annotations

from typing import Any, cast

from wizardgram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class InlineKeyboardBuilder:
    """Build an inline keyboard using chained button and row calls."""

    def __init__(self) -> None:
        self._rows: list[list[InlineKeyboardButton]] = [[]]

    def button(
        self,
        text: str,
        callback_data: str | None = None,
        url: str | None = None,
        **kwargs: Any,
    ) -> InlineKeyboardBuilder:
        """Add a button to the current row."""
        button = cast(InlineKeyboardButton, {"text": text, **kwargs})
        if callback_data is not None:
            button["callback_data"] = callback_data
        if url is not None:
            button["url"] = url
        self._rows[-1].append(button)
        return self

    def row(self) -> InlineKeyboardBuilder:
        """Start a new row."""
        if self._rows[-1]:
            self._rows.append([])
        return self

    def build(self) -> InlineKeyboardMarkup:
        """Return the Telegram inline keyboard dictionary."""
        return {"inline_keyboard": [row.copy() for row in self._rows if row]}


class ReplyKeyboardBuilder:
    """Build a reply keyboard using chained button and layout calls."""

    def __init__(self) -> None:
        self._rows: list[list[KeyboardButton]] = [[]]
        self._options: dict[str, Any] = {}

    def button(self, text: str, **kwargs: Any) -> ReplyKeyboardBuilder:
        """Add a button to the current row."""
        self._rows[-1].append(cast(KeyboardButton, {"text": text, **kwargs}))
        return self

    def row(self) -> ReplyKeyboardBuilder:
        """Start a new row."""
        if self._rows[-1]:
            self._rows.append([])
        return self

    def resize(self, value: bool = True) -> ReplyKeyboardBuilder:
        """Set the resize_keyboard option."""
        self._options["resize_keyboard"] = value
        return self

    def one_time(self, value: bool = True) -> ReplyKeyboardBuilder:
        """Set the one_time_keyboard option."""
        self._options["one_time_keyboard"] = value
        return self

    def selective(self, value: bool = True) -> ReplyKeyboardBuilder:
        """Set the selective option."""
        self._options["selective"] = value
        return self

    def build(self) -> ReplyKeyboardMarkup:
        """Return the Telegram reply keyboard dictionary."""
        return cast(
            ReplyKeyboardMarkup,
            {"keyboard": [row.copy() for row in self._rows if row], **self._options},
        )


class Keyboard:
    """Namespace for keyboard builder factories."""

    @staticmethod
    def inline() -> InlineKeyboardBuilder:
        """Create an inline keyboard builder."""
        return InlineKeyboardBuilder()

    @staticmethod
    def reply() -> ReplyKeyboardBuilder:
        """Create a reply keyboard builder."""
        return ReplyKeyboardBuilder()
