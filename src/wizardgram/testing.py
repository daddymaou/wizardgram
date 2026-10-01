from __future__ import annotations

from typing import Any, cast

from wizardgram.bot import Bot
from wizardgram.types import Message, Update


class MockMessage(dict[str, Any]):
    """Dictionary-like mock Telegram message returned by TestBot."""

    @property
    def text(self) -> str:
        """Message text content."""
        return str(self.get("text", ""))

    @property
    def chat_id(self) -> int:
        """Numeric chat identifier."""
        return int(self.get("chat", {}).get("id", 0))

    @property
    def reply_markup(self) -> Any | None:
        """Attached reply markup, if present."""
        return self.get("reply_markup")


class TestBot(Bot):
    """A Bot subclass that records outgoing API calls for handler tests."""

    __test__ = False

    def __init__(self) -> None:
        self.token = "test-token"
        self.transport = cast(Any, None)
        from wizardgram.middleware import MiddlewareManager

        self.middlewares = MiddlewareManager()
        self.min_interval_ms = None
        self._last_chat_call: dict[int, float] = {}
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self._last_message: MockMessage | None = None

    async def _api(self, method: str, **params: Any) -> Any:
        self.calls.append((method, params.copy()))
        if method == "sendMessage":
            self._last_message = MockMessage(
                message_id=len(self.calls),
                date=0,
                chat={"id": params.get("chat_id", 0), "type": "private"},
                text=params.get("text", ""),
                reply_markup=params.get("reply_markup"),
            )
            return cast(Message, self._last_message)
        if method in {"editMessageText", "editMessageCaption", "editMessageReplyMarkup"}:
            return cast(Message, self._last_message or {})
        return True

    async def _api_multipart(self, method: str, files: dict[str, Any], **params: Any) -> Any:
        self.calls.append((method, {**params, "files": files}))
        return self._last_message or {}

    async def simulate(self, update: Update) -> MockMessage | None:
        """Dispatch an update and return the most recent sendMessage result."""
        self.reset()
        await self.dispatch(update)
        return self._last_message

    def reset(self) -> None:
        """Clear recorded calls and mock result state."""
        self.calls.clear()
        self._last_message = None

    async def close(self) -> None:
        """No-op because TestBot does not create a transport client."""


class Updates:
    """Factories for realistic Telegram update dictionaries."""

    @staticmethod
    def text(content: str, *, user: str = "tester", chat_id: int = 1, update_id: int = 1) -> Update:
        """Build a message update containing text."""
        return cast(
            Update,
            {
                "update_id": update_id,
                "message": {
                    "message_id": 1,
                    "date": 0,
                    "chat": {"id": chat_id, "type": "private", "first_name": user},
                    "from_user": {"id": chat_id, "is_bot": False, "first_name": user},
                    "text": content,
                },
            },
        )

    @staticmethod
    def command(name: str, *, user: str = "tester", chat_id: int = 1, update_id: int = 1) -> Update:
        """Build a message update containing a slash command."""
        return Updates.text(f"/{name}", user=user, chat_id=chat_id, update_id=update_id)

    @staticmethod
    def callback(
        data: str,
        *,
        user: str = "tester",
        chat_id: int = 1,
        message_id: int = 1,
        update_id: int = 1,
    ) -> Update:
        """Build a callback query update with its originating message."""
        return cast(
            Update,
            {
                "update_id": update_id,
                "callback_query": {
                    "id": f"callback-{update_id}",
                    "from_user": {"id": chat_id, "is_bot": False, "first_name": user},
                    "chat_instance": str(chat_id),
                    "message": {
                        "message_id": message_id,
                        "date": 0,
                        "chat": {"id": chat_id, "type": "private"},
                        "text": "Choose",
                    },
                    "data": data,
                },
            },
        )

    @staticmethod
    def photo(
        *, user: str = "tester", chat_id: int = 1, file_id: str = "x", update_id: int = 1
    ) -> Update:
        """Build a message update containing one photo size."""
        update = Updates.text("", user=user, chat_id=chat_id, update_id=update_id)
        cast(dict[str, Any], update["message"])["photo"] = [{"file_id": file_id}]
        return update
