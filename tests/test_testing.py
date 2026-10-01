from __future__ import annotations

from wizardgram import Context, TestBot, Updates


async def test_simulate_captures_reply(bot: TestBot) -> None:
    @bot.command("hello")
    async def hello(ctx: Context) -> None:
        await ctx.reply("world")

    result = await bot.simulate(Updates.command("hello"))
    assert result is not None
    assert result.text == "world"


def test_updates_text_builds_valid_update() -> None:
    update = Updates.text("hi", user="Kai", chat_id=5)
    assert update["message"]["text"] == "hi"
    assert update["message"]["chat"]["id"] == 5


def test_updates_callback_builds_valid_update() -> None:
    update = Updates.callback("confirm")
    assert update["callback_query"]["data"] == "confirm"
