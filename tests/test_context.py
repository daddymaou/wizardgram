from __future__ import annotations

import pytest

from wizardgram import Context, TestBot, Updates


@pytest.mark.asyncio
async def test_reply_fills_chat_id(bot: TestBot) -> None:
    await bot.simulate(Updates.text("hello", chat_id=23))

    @bot.command("go")
    async def handler(ctx: Context) -> None:
        await ctx.reply("reply")

    await bot.simulate(Updates.command("go", chat_id=23))
    assert bot.calls[0][1]["chat_id"] == 23


def test_from_user_from_message() -> None:
    context = Context(Updates.text("hello", user="Mina"), TestBot())
    assert context.from_user is not None
    assert context.from_user["first_name"] == "Mina"


def test_from_user_from_callback_query() -> None:
    context = Context(Updates.callback("x", user="Mina"), TestBot())
    assert context.from_user is not None
    assert context.from_user["first_name"] == "Mina"


def test_text_shortcut() -> None:
    assert Context(Updates.text("hello"), TestBot()).text == "hello"


@pytest.mark.asyncio
async def test_edit_text_from_callback(bot: TestBot) -> None:
    context = Context(Updates.callback("x", chat_id=7, message_id=9), bot)
    await context.edit_text("changed")
    assert bot.calls[0][0] == "editMessageText"
    assert bot.calls[0][1]["message_id"] == 9


@pytest.mark.asyncio
async def test_delete_message() -> None:
    bot = TestBot()
    context = Context(Updates.text("hello", chat_id=8), bot)
    assert await context.delete_message()
    assert bot.calls[0][0] == "deleteMessage"


@pytest.mark.asyncio
async def test_answer_callback_query() -> None:
    bot = TestBot()
    context = Context(Updates.callback("x"), bot)
    assert await context.answer_callback_query("done")
    assert bot.calls[0][0] == "answerCallbackQuery"
    assert bot.calls[0][1]["callback_query_id"] == "callback-1"


def test_from_user_uses_telegram_from_key() -> None:
    update = {
        "update_id": 1,
        "message": {
            "message_id": 1,
            "chat": {"id": 8, "type": "private"},
            "from": {"id": 8, "first_name": "Mina"},
        },
    }
    context = Context(update, TestBot())
    assert context.from_user is not None
    assert context.from_user["first_name"] == "Mina"
