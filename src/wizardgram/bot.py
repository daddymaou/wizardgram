from __future__ import annotations

import asyncio
import logging
import re
from collections.abc import Callable
from typing import Any, cast

from wizardgram.context import Context
from wizardgram.errors import NetworkError, TelegramError
from wizardgram.middleware import Middleware, MiddlewareManager
from wizardgram.router import Handler, action, command, hears, on
from wizardgram.transport import FileInput, Transport
from wizardgram.types import Update, User

logger = logging.getLogger(__name__)


class Bot:
    """The main entry point for polling, webhooks, and update handlers."""

    def __init__(
        self,
        token: str,
        *,
        max_retries: int = 3,
        timeout: float = 30.0,
        min_interval_ms: int | None = None,
    ) -> None:
        self.token = token
        self.transport = Transport(token, max_retries=max_retries, timeout=timeout)
        self.middlewares = MiddlewareManager()
        self.min_interval_ms = min_interval_ms
        self._last_chat_call: dict[int, float] = {}

    def use(self, mw: Middleware) -> Bot:
        """Register middleware and return this bot for chaining."""
        self.middlewares.add(mw)
        return self

    def middleware(self, fn: Middleware) -> Middleware:
        """Register middleware using decorator syntax."""
        self.use(fn)
        return fn

    def command(self, name: str, handler: Handler | None = None) -> Handler | Bot:
        """Register a command handler as a decorator or direct call."""
        return self._register(lambda fn: command(name, fn), handler)

    def hears(
        self, pattern: str | re.Pattern[str], handler: Handler | None = None
    ) -> Handler | Bot:
        """Register a text-pattern handler."""
        return self._register(lambda fn: hears(pattern, fn), handler)

    def action(
        self, pattern: str | re.Pattern[str], handler: Handler | None = None
    ) -> Handler | Bot:
        """Register a callback-data handler."""
        return self._register(lambda fn: action(pattern, fn), handler)

    def on(self, update_type: str, handler: Handler | None = None) -> Handler | Bot:
        """Register a handler for a specific Telegram update type."""
        return self._register(lambda fn: on(update_type, fn), handler)

    def _register(
        self, factory: Callable[[Handler], Middleware], handler: Handler | None
    ) -> Handler | Bot:
        if handler is None:

            def decorator(fn: Handler) -> Handler:
                self.use(factory(fn))
                return fn

            return cast(Handler | Bot, decorator)
        self.use(factory(handler))
        return self

    async def dispatch(self, update: Update) -> None:
        """Build a Context and run middleware; log handler errors."""
        try:
            await self.middlewares.run(Context(update, self))
        except Exception:
            logger.exception("Failed to dispatch Telegram update")

    async def get_updates(self, offset: int | None = None, timeout: int = 30) -> list[Update]:
        """Fetch updates using Telegram long polling."""
        result = await self._api("getUpdates", offset=offset, timeout=timeout)
        return cast(list[Update], result)

    async def start(self) -> None:
        """Poll forever, advancing update offset and backing off on errors."""
        offset: int | None = None
        backoff = 1.0
        while True:
            try:
                updates = await self.get_updates(offset=offset)
                backoff = 1.0
                for update in updates:
                    await self.dispatch(update)
                    if "update_id" in update:
                        offset = update["update_id"] + 1
            except asyncio.CancelledError:
                raise
            except (TelegramError, NetworkError):
                logger.exception("Polling request failed; retrying")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 30.0)

    def run(self) -> None:
        """Run the asynchronous polling loop."""
        asyncio.run(self.start())

    async def handle_webhook(self, request: Any) -> dict[str, bool]:
        """Parse and dispatch an update from a framework request object."""
        update = cast(Update, await request.json())
        await self.dispatch(update)
        return {"ok": True}

    async def set_webhook(self, url: str, **kwargs: Any) -> bool:
        """Register a Telegram webhook URL."""
        return cast(bool, await self._api("setWebhook", url=url, **kwargs))

    async def delete_webhook(self, **kwargs: Any) -> bool:
        """Remove the configured Telegram webhook."""
        return cast(bool, await self._api("deleteWebhook", **kwargs))

    async def get_me(self) -> User:
        """Return the bot's Telegram user record."""
        return cast(User, await self._api("getMe"))

    async def close(self) -> None:
        """Close the HTTP transport."""
        await self.transport.close()

    async def _api(self, method: str, **params: Any) -> Any:
        chat_id = params.get("chat_id")
        if self.min_interval_ms is not None and isinstance(chat_id, int):
            now = asyncio.get_running_loop().time()
            delay = self.min_interval_ms / 1000 - (now - self._last_chat_call.get(chat_id, 0))
            if delay > 0:
                await asyncio.sleep(delay)
            self._last_chat_call[chat_id] = asyncio.get_running_loop().time()
        return await self.transport.call(method, **params)

    async def _api_multipart(self, method: str, files: dict[str, FileInput], **params: Any) -> Any:
        chat_id = params.get("chat_id")
        if self.min_interval_ms is not None and isinstance(chat_id, int):
            now = asyncio.get_running_loop().time()
            delay = self.min_interval_ms / 1000 - (now - self._last_chat_call.get(chat_id, 0))
            if delay > 0:
                await asyncio.sleep(delay)
            self._last_chat_call[chat_id] = asyncio.get_running_loop().time()
        return await self.transport.call_multipart(method, files, **params)
