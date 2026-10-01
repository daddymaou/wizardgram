"""Minimal Telegram object types.

The library accepts raw dictionaries anywhere. Users who need full Bot API
coverage can import schema types from a separate package.
"""

from __future__ import annotations

from typing import Any, TypedDict

from typing_extensions import NotRequired


class User(TypedDict):
    """A Telegram user with commonly used fields."""

    id: int
    is_bot: NotRequired[bool]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    username: NotRequired[str]
    language_code: NotRequired[str]


class Chat(TypedDict):
    """A Telegram chat with commonly used fields."""

    id: int
    type: NotRequired[str]
    title: NotRequired[str]
    username: NotRequired[str]
    first_name: NotRequired[str]
    last_name: NotRequired[str]


class Message(TypedDict):
    """A Telegram message with commonly used fields."""

    message_id: int
    date: NotRequired[int]
    chat: NotRequired[Chat]
    from_user: NotRequired[User]
    text: NotRequired[str]
    caption: NotRequired[str]
    reply_markup: NotRequired[dict[str, Any]]


class CallbackQuery(TypedDict):
    """A Telegram callback query."""

    id: str
    from_user: User
    chat_instance: NotRequired[str]
    message: NotRequired[Message]
    inline_message_id: NotRequired[str]
    data: NotRequired[str]


class InlineKeyboardButton(TypedDict):
    """A button in an inline keyboard."""

    text: str
    callback_data: NotRequired[str]
    url: NotRequired[str]


class InlineKeyboardMarkup(TypedDict):
    """An inline keyboard markup object."""

    inline_keyboard: list[list[InlineKeyboardButton]]


class KeyboardButton(TypedDict):
    """A button in a reply keyboard."""

    text: str
    request_contact: NotRequired[bool]
    request_location: NotRequired[bool]


class ReplyKeyboardMarkup(TypedDict):
    """A reply keyboard markup object."""

    keyboard: list[list[KeyboardButton]]
    resize_keyboard: NotRequired[bool]
    one_time_keyboard: NotRequired[bool]
    selective: NotRequired[bool]


class ReplyParameters(TypedDict):
    """Parameters identifying a message to reply to."""

    message_id: int
    chat_id: NotRequired[int | str]


class Update(TypedDict, total=False):
    """An update with optional top-level event fields."""

    update_id: int
    message: Message
    edited_message: Message
    channel_post: Message
    edited_channel_post: Message
    callback_query: CallbackQuery
    inline_query: dict[str, Any]
    chosen_inline_result: dict[str, Any]
    poll: dict[str, Any]
    poll_answer: dict[str, Any]
    my_chat_member: dict[str, Any]
    chat_member: dict[str, Any]
    chat_join_request: dict[str, Any]
