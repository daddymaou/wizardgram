from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path
from typing import Any, BinaryIO, cast

import httpx

from wizardgram.errors import NetworkError, TelegramError

FileInput = bytes | BinaryIO | str | os.PathLike[str] | tuple[Any, ...]


class Transport:
    """HTTP transport for the Telegram Bot API.

    Handles JSON calls, multipart uploads, and flood-control retries.

    Args:
            token: The bot token from BotFather.
            base_url: Optional override for the API base URL.
            max_retries: Maximum number of retries after HTTP 429 responses.
            timeout: Request timeout in seconds.
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str | None = None,
        max_retries: int = 3,
        timeout: float = 30.0,
    ) -> None:
        self.token = token
        self.base_url = base_url or f"https://api.telegram.org/bot{token}/"
        self.max_retries = max_retries
        self._client = httpx.AsyncClient(timeout=timeout)

    async def call(self, method: str, **params: Any) -> Any:
        """POST a JSON request to the Bot API and return the result.

        Raises TelegramError when Telegram rejects the request and NetworkError
        when httpx cannot connect or complete the request.
        """
        return await self._request(method, json=params)

    async def call_multipart(self, method: str, files: dict[str, FileInput], **params: Any) -> Any:
        """POST multipart form data with file objects streamed by httpx."""
        opened: list[BinaryIO] = []
        multipart: dict[str, Any] = {}
        try:
            for field, source in files.items():
                if isinstance(source, bytes):
                    multipart[field] = (field, source)
                elif isinstance(source, tuple) or hasattr(source, "read"):
                    multipart[field] = source
                else:
                    path = Path(source)
                    stream = cast(BinaryIO, path.open("rb"))
                    opened.append(stream)
                    multipart[field] = (path.name, stream)
            data = {
                key: value if isinstance(value, (str, bytes)) else json.dumps(value)
                for key, value in params.items()
                if value is not None
            }
            return await self._request(method, data=data, files=multipart)
        finally:
            for stream in opened:
                stream.close()

    async def _request(self, method: str, **kwargs: Any) -> Any:
        url = f"{self.base_url}{method}"
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._client.post(url, **kwargs)
            except httpx.HTTPError as exc:
                raise NetworkError(str(exc)) from exc
            try:
                payload = response.json()
            except ValueError as exc:
                raise TelegramError(response.status_code, "Invalid JSON response") from exc
            if payload.get("ok"):
                return payload.get("result")
            error_code = int(payload.get("error_code", response.status_code))
            parameters = payload.get("parameters") or {}
            retry_after = parameters.get("retry_after")
            if error_code == 429 and retry_after is None:
                header_value = response.headers.get("Retry-After")
                retry_after = int(header_value) if header_value else 1
            if error_code == 429 and attempt < self.max_retries:
                await asyncio.sleep(float(retry_after if retry_after is not None else 1))
                continue
            raise TelegramError(
                error_code,
                str(payload.get("description", "Telegram API request failed")),
                int(retry_after) if retry_after is not None else None,
            )
        raise AssertionError("retry loop exhausted unexpectedly")

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._client.aclose()
