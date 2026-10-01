from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, cast

from wizardgram.transport import FileInput
from wizardgram.types import Chat, Message, Update, User

if TYPE_CHECKING:
    from wizardgram.bot import Bot
    from wizardgram.fsm import SceneContext


class Context:
    """Wrap a Telegram update and expose convenient reply helpers."""

    update: Update
    bot: Bot
    update_id: int | None
    update_type: str | None
    message: Message | None
    edited_message: Message | None
    channel_post: Message | None
    edited_channel_post: Message | None
    callback_query: dict[str, Any] | None
    inline_query: dict[str, Any] | None
    chosen_inline_result: dict[str, Any] | None
    poll: dict[str, Any] | None
    poll_answer: dict[str, Any] | None
    my_chat_member: dict[str, Any] | None
    chat_member: dict[str, Any] | None
    chat_join_request: dict[str, Any] | None
    from_user: User | None
    chat: Chat | None
    text: str | None
    match: re.Match[str] | None
    scene: SceneContext | None

    def __init__(self, update: Update, bot: Bot) -> None:
        self.update = update
        self.bot = bot
        self.update_id = update.get("update_id")
        event_keys = [key for key in update if key != "update_id"]
        self.update_type = event_keys[0] if event_keys else None
        for key in (
            "message",
            "edited_message",
            "channel_post",
            "edited_channel_post",
            "callback_query",
            "inline_query",
            "chosen_inline_result",
            "poll",
            "poll_answer",
            "my_chat_member",
            "chat_member",
            "chat_join_request",
        ):
            setattr(self, key, update.get(key))
        message = (
            self.message or self.edited_message or self.channel_post or self.edited_channel_post
        )
        callback = self.callback_query
        callback_message = callback.get("message") if callback else None
        user = None
        if message is not None:
            user = message.get("from_user") or cast(dict[str, Any], message).get("from")
        if user is None and callback:
            user = callback.get("from_user") or callback.get("from")
        self.from_user = user
        self.chat = message.get("chat") if message else None
        if self.chat is None and callback_message is not None:
            self.chat = callback_message.get("chat")
        self.text = message.get("text") if message else None
        self.match = None
        self.scene = None
        self.state: dict[str, Any] = {}

    async def reply(self, text: str, **kwargs: Any) -> Message:
        """Send a message to the current chat, filling in chat_id."""
        if self.chat is None:
            raise ValueError("This update does not belong to a chat")
        return cast(
            Message,
            await self.bot._api("sendMessage", chat_id=self.chat["id"], text=text, **kwargs),
        )

    async def reply_with_photo(
        self, source: FileInput, caption: str | None = None, **kwargs: Any
    ) -> Message:
        """Send a photo to the current chat."""
        if self.chat is None:
            raise ValueError("This update does not belong to a chat")
        params = {"chat_id": self.chat["id"], "caption": caption, **kwargs}
        return cast(
            Message, await self.bot._api_multipart("sendPhoto", {"photo": source}, **params)
        )

    async def reply_with_document(
        self, source: FileInput, filename: str | None = None, **kwargs: Any
    ) -> Message:
        """Send a document to the current chat."""
        if self.chat is None:
            raise ValueError("This update does not belong to a chat")
        file = (filename, source) if filename and isinstance(source, bytes) else source
        params = {"chat_id": self.chat["id"], **kwargs}
        return cast(
            Message,
            await self.bot._api_multipart("sendDocument", {"document": file}, **params),
        )

    async def edit_text(self, text: str, **kwargs: Any) -> Message | bool:
        """Edit the message that triggered this context."""
        message = self._source_message()
        if message is None or self.chat is None:
            raise ValueError("This update has no editable chat message")
        return cast(
            Message | bool,
            await self.bot._api(
                "editMessageText",
                chat_id=self.chat["id"],
                message_id=message["message_id"],
                text=text,
                **kwargs,
            ),
        )

    async def edit_reply_markup(self, reply_markup: Any, **kwargs: Any) -> Message | bool:
        """Edit the inline keyboard attached to the triggering message."""
        return await self._edit_message(
            "editMessageReplyMarkup", reply_markup=reply_markup, **kwargs
        )

    async def edit_caption(self, caption: str, **kwargs: Any) -> Message | bool:
        """Edit the caption of the triggering message."""
        return await self._edit_message("editMessageCaption", caption=caption, **kwargs)

    async def delete_message(self, **kwargs: Any) -> bool:
        """Delete the message that triggered this context."""
        message = self._source_message()
        if message is None or self.chat is None:
            raise ValueError("This update has no deletable chat message")
        return cast(
            bool,
            await self.bot._api(
                "deleteMessage",
                chat_id=self.chat["id"],
                message_id=message["message_id"],
                **kwargs,
            ),
        )

    async def answer_callback_query(self, text: str | None = None, **kwargs: Any) -> bool:
        """Answer the current callback query."""
        if self.callback_query is None:
            raise ValueError("This update is not a callback query")
        return cast(
            bool,
            await self.bot._api(
                "answerCallbackQuery",
                callback_query_id=self.callback_query["id"],
                text=text,
                **kwargs,
            ),
        )

    async def send_chat_action(self, action: str, **kwargs: Any) -> bool:
        """Send a chat action to the current chat."""
        if self.chat is None:
            raise ValueError("This update does not belong to a chat")
        return cast(
            bool,
            await self.bot._api("sendChatAction", chat_id=self.chat["id"], action=action, **kwargs),
        )

    async def reply_with_keyboard(self, text: str, keyboard: Any, **kwargs: Any) -> Message:
        """Send a message with the given reply markup."""
        return await self.reply(text, reply_markup=keyboard, **kwargs)

    def t(self, key: str, *args: Any) -> str:
        """Translate a key; return the key unchanged without an i18n layer."""
        return key.format(*args) if args else key

    def _source_message(self) -> Message | None:
        message = (
            self.message or self.edited_message or self.channel_post or self.edited_channel_post
        )
        if message is None and self.callback_query is not None:
            return self.callback_query.get("message")
        return message

    async def _edit_message(self, method: str, **params: Any) -> Message | bool:
        message = self._source_message()
        if message is None or self.chat is None:
            raise ValueError("This update has no editable chat message")
        return cast(
            Message | bool,
            await self.bot._api(
                method,
                chat_id=self.chat["id"],
                message_id=message["message_id"],
                **params,
            ),
        )
