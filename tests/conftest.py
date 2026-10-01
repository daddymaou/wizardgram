from __future__ import annotations

import pytest
import respx

from wizardgram import TestBot


@pytest.fixture
def mock_transport() -> respx.MockRouter:
    """Enable an isolated respx router for each transport test."""
    router = respx.mock(assert_all_called=False)
    router.start()
    yield router
    router.stop()


@pytest.fixture
def bot() -> TestBot:
    """Return a Bot with outgoing calls intercepted in memory."""
    return TestBot()
