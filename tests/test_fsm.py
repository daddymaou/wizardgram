from __future__ import annotations

from wizardgram import Context, Scene, Stage, TestBot, Updates


async def test_scene_advances_through_steps() -> None:
    bot = TestBot()
    calls: list[int] = []

    async def first(ctx: Context) -> None:
        calls.append(1)
        assert ctx.scene is not None
        await ctx.scene.next()

    async def second(ctx: Context) -> None:
        calls.append(2)
        assert ctx.scene is not None
        await ctx.scene.leave()

    stage = Stage([Scene("signup", [first, second])])
    await stage.store.set(1, {"scene": "signup", "step": 0})
    bot.use(stage.middleware())
    await bot.simulate(Updates.text("one"))
    await bot.simulate(Updates.text("two", update_id=2))
    assert calls == [1, 2]


async def test_scene_leave_clears_state() -> None:
    bot = TestBot()

    async def step(ctx: Context) -> None:
        assert ctx.scene is not None
        await ctx.scene.leave()

    stage = Stage([Scene("flow", [step])])
    await stage.store.set(1, {"scene": "flow", "step": 0})
    bot.use(stage.middleware())
    await bot.simulate(Updates.text("leave"))
    assert await stage.store.get(1) == {}


async def test_unrelated_update_falls_through() -> None:
    bot = TestBot()
    seen: list[bool] = []
    stage = Stage([Scene("flow", [])])

    async def following(ctx: Context, next_: object) -> None:
        seen.append(True)

    bot.use(stage.middleware())
    bot.use(following)
    await bot.simulate(Updates.text("ordinary"))
    assert seen == [True]
