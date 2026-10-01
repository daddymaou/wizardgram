from __future__ import annotations

import re

import pytest

from wizardgram import Context, TestBot, Updates


@pytest.mark.asyncio
async def test_command_matches(bot: TestBot) -> None:
    @bot.command("start")
    async def start(ctx: Context) -> None:
        await ctx.reply("started")

    await bot.simulate(Updates.command("start"))
    assert bot.calls[0][1]["text"] == "started"


@pytest.mark.asyncio
async def test_command_ignores_botname_suffix(bot: TestBot) -> None:
    matched: list[bool] = []

    @bot.command("start")
    async def start(ctx: Context) -> None:
        matched.append(True)

    await bot.simulate(Updates.text("/start@sample_bot hello"))
    assert matched == [True]


@pytest.mark.asyncio
async def test_hears_sets_match(bot: TestBot) -> None:
    found: list[str] = []

    @bot.hears(re.compile(r"ping (\w+)"))
    async def handler(ctx: Context) -> None:
        assert ctx.match is not None
        found.append(ctx.match.group(1))

    await bot.simulate(Updates.text("please ping wizard"))
    assert found == ["wizard"]


@pytest.mark.asyncio
async def test_action_matches_callback_data(bot: TestBot) -> None:
    found: list[str] = []

    @bot.action(r"^confirm:(\d+)$")
    async def handler(ctx: Context) -> None:
        assert ctx.match is not None
        found.append(ctx.match.group(1))

    await bot.simulate(Updates.callback("confirm:42"))
    assert found == ["42"]


@pytest.mark.asyncio
async def test_unknown_update_is_ignored(bot: TestBot) -> None:
    await bot.dispatch({"update_id": 9})
    assert bot.calls == []


@pytest.mark.asyncio
async def test_dispatch_builds_context(bot: TestBot) -> None:
    received: list[Context] = []

    @bot.command("start")
    async def handler(ctx: Context) -> None:
        received.append(ctx)

    await bot.dispatch(Updates.command("start", update_id=12))
    assert received[0].update_id == 12
    assert received[0].update_type == "message"
