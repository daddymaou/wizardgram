"""Middleware factories for common Telegram update patterns."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from typing import Any

from wizardgram.context import Context
from wizardgram.middleware import Middleware, Next

Handler = Callable[[Context], Awaitable[Any]]


def command(name: str, handler: Handler) -> Middleware:
    """Match a command at the start of the current message text."""
    pattern = re.compile(rf"^/{re.escape(name)}(?:@\w+)?(?:\s|$)")

    async def middleware(ctx: Context, next_: Next) -> None:
        if ctx.text is not None and pattern.match(ctx.text):
            ctx.match = pattern.match(ctx.text)
            await handler(ctx)
            return
        await next_()

    return middleware


def hears(pattern: str | re.Pattern[str], handler: Handler) -> Middleware:
    """Match message text with a regular expression and expose the match."""
    compiled = re.compile(pattern) if isinstance(pattern, str) else pattern

    async def middleware(ctx: Context, next_: Next) -> None:
        found = compiled.search(ctx.text) if ctx.text is not None else None
        if found is not None:
            ctx.match = found
            await handler(ctx)
            return
        await next_()

    return middleware


def action(pattern: str | re.Pattern[str], handler: Handler) -> Middleware:
    """Match callback-query data with a regular expression."""
    compiled = re.compile(pattern) if isinstance(pattern, str) else pattern

    async def middleware(ctx: Context, next_: Next) -> None:
        data = ctx.callback_query.get("data") if ctx.callback_query else None
        found = compiled.search(data) if isinstance(data, str) else None
        if found is not None:
            ctx.match = found
            await handler(ctx)
            return
        await next_()

    return middleware


def on(update_type: str, handler: Handler) -> Middleware:
    """Run a handler when the current update has the requested type."""

    async def middleware(ctx: Context, next_: Next) -> None:
        if ctx.update_type == update_type:
            await handler(ctx)
            return
        await next_()

    return middleware


def filter_(predicate: Callable[[Context], bool], handler: Handler) -> Middleware:
    """Run a handler when a synchronous context predicate returns true."""

    async def middleware(ctx: Context, next_: Next) -> None:
        if predicate(ctx):
            await handler(ctx)
            return
        await next_()

    return middleware


def branch(
    predicate: Callable[[Context], bool], on_true: Middleware, on_false: Middleware
) -> Middleware:
    """Run one of two middleware functions according to a predicate."""

    async def middleware(ctx: Context, next_: Next) -> None:
        await (on_true if predicate(ctx) else on_false)(ctx, next_)

    return middleware
