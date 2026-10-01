from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from wizardgram.context import Context

Next = Callable[[], Awaitable[None]]
Middleware = Callable[[Context, Next], Awaitable[None]]

logger = logging.getLogger(__name__)


class MiddlewareManager:
    """Ordered chain of middleware with compose() semantics."""

    def __init__(self) -> None:
        self._items: list[Middleware] = []

    def add(self, mw: Middleware) -> None:
        """Append middleware to the execution chain."""
        self._items.append(mw)

    async def run(self, ctx: Context) -> None:
        """Run middleware in registration order, honoring next callbacks."""

        async def dispatch(index: int) -> None:
            if index >= len(self._items):
                return
            called = False

            async def next_() -> None:
                nonlocal called
                if not called:
                    called = True
                    await dispatch(index + 1)

            try:
                await self._items[index](ctx, next_)
            except Exception:
                logger.exception("Middleware failed")
                if not called:
                    await next_()

        await dispatch(0)
