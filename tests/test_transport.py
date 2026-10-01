from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx
import pytest

from wizardgram.errors import NetworkError, TelegramError
from wizardgram.transport import Transport

BASE_URL = "https://api.telegram.org/botTEST/"


@pytest.mark.asyncio
async def test_call_success(mock_transport: Any) -> None:
    mock_transport.post(f"{BASE_URL}getMe").mock(
        return_value=httpx.Response(200, json={"ok": True, "result": {"id": 1}})
    )
    transport = Transport("TEST", base_url=BASE_URL)
    assert await transport.call("getMe") == {"id": 1}
    await transport.close()


@pytest.mark.asyncio
async def test_call_raises_on_ok_false(mock_transport: Any) -> None:
    mock_transport.post(f"{BASE_URL}bad").mock(
        return_value=httpx.Response(
            400, json={"ok": False, "error_code": 400, "description": "bad request"}
        )
    )
    transport = Transport("TEST", base_url=BASE_URL)
    with pytest.raises(TelegramError, match="bad request"):
        await transport.call("bad")
    await transport.close()


@pytest.mark.asyncio
async def test_call_retries_on_429(mock_transport: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr("wizardgram.transport.asyncio.sleep", fake_sleep)
    route = mock_transport.post(f"{BASE_URL}busy")
    route.side_effect = [
        httpx.Response(
            429,
            json={
                "ok": False,
                "error_code": 429,
                "description": "busy",
                "parameters": {"retry_after": 4},
            },
        ),
        httpx.Response(200, json={"ok": True, "result": True}),
    ]
    transport = Transport("TEST", base_url=BASE_URL)
    assert await transport.call("busy") is True
    assert sleeps == [4.0]
    await transport.close()


@pytest.mark.asyncio
async def test_call_gives_up_after_max_retries(mock_transport: Any) -> None:
    mock_transport.post(f"{BASE_URL}busy").mock(
        return_value=httpx.Response(
            429,
            json={
                "ok": False,
                "error_code": 429,
                "description": "busy",
                "parameters": {"retry_after": 0},
            },
        )
    )
    transport = Transport("TEST", base_url=BASE_URL, max_retries=1)
    with pytest.raises(TelegramError) as error:
        await transport.call("busy")
    assert error.value.retry_after == 0
    await transport.close()


@pytest.mark.asyncio
async def test_call_multipart_with_bytes(mock_transport: Any) -> None:
    route = mock_transport.post(f"{BASE_URL}sendPhoto").mock(
        return_value=httpx.Response(200, json={"ok": True, "result": {"message_id": 1}})
    )
    transport = Transport("TEST", base_url=BASE_URL)
    await transport.call_multipart("sendPhoto", {"photo": b"image-data"}, chat_id=1)
    assert route.called
    assert b"image-data" in route.calls.last.request.content
    await transport.close()


@pytest.mark.asyncio
async def test_call_multipart_with_path(mock_transport: Any, tmp_path: Path) -> None:
    path = tmp_path / "photo.png"
    path.write_bytes(b"file-data")
    route = mock_transport.post(f"{BASE_URL}sendPhoto").mock(
        return_value=httpx.Response(200, json={"ok": True, "result": {"message_id": 1}})
    )
    transport = Transport("TEST", base_url=BASE_URL)
    await transport.call_multipart("sendPhoto", {"photo": str(path)}, chat_id=1)
    assert b"file-data" in route.calls.last.request.content
    await transport.close()


@pytest.mark.asyncio
async def test_network_error_wrapped(mock_transport: Any) -> None:
    mock_transport.post(f"{BASE_URL}offline").mock(side_effect=httpx.ConnectError("offline"))
    transport = Transport("TEST", base_url=BASE_URL)
    with pytest.raises(NetworkError, match="offline"):
        await transport.call("offline")
    await transport.close()
