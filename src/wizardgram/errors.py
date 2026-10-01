from __future__ import annotations


class WizardgramError(Exception):
    """Base class for all wizardgram errors."""


class TelegramError(WizardgramError):
    """Raised when the Telegram Bot API returns an unsuccessful response.

    Attributes:
            error_code: HTTP-style error code returned by Telegram.
            description: Human-readable error description.
            retry_after: Suggested delay in seconds for flood-control responses.
    """

    def __init__(self, error_code: int, description: str, retry_after: int | None = None) -> None:
        self.error_code = error_code
        self.description = description
        self.retry_after = retry_after
        super().__init__(f"Telegram API error {error_code}: {description}")


class NetworkError(WizardgramError):
    """Raised for connection failures, timeouts, and DNS errors."""
