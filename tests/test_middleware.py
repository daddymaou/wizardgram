from __future__ import annotations

from wizardgram import Context, TestBot, Updates
from wizardgram.middleware import MiddlewareManager


async def test_middlewares_run_in_order() -> None:
    manager = MiddlewareManager()
    events: list[int] = []

    async def first(ctx: Context, next_: object) -> None:
        events.append(1)
        await next_()  # type: ignore[operator]
        events.append(4)

    async def second(ctx: Context, next_: object) -> None:
        events.append(2)
        await next_()  # type: ignore[operator]
        events.append(3)

    manager.add(first)
    manager.add(second)
    await manager.run(Context(Updates.text("hi"), TestBot()))
    assert events == [1, 2, 3, 4]


async def test_next_short_circuits() -> None:
    manager = MiddlewareManager()
    events: list[str] = []

    async def stop(ctx: Context, next_: object) -> None:
        events.append("stop")

    async def skipped(ctx: Context, next_: object) -> None:
        events.append("skipped")

    manager.add(stop)
    manager.add(skipped)
    await manager.run(Context(Updates.text("hi"), TestBot()))
    assert events == ["stop"]


async def test_middleware_exception_does_not_break_chain() -> None:
    manager = MiddlewareManager()
    events: list[str] = []

    async def broken(ctx: Context, next_: object) -> None:
        raise RuntimeError("expected")

    async def following(ctx: Context, next_: object) -> None:
        events.append("ran")

    manager.add(broken)
    manager.add(following)
    await manager.run(Context(Updates.text("hi"), TestBot()))
    assert events == ["ran"]
