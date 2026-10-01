from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any, cast


class VerificationStatus(str, Enum):
    """Confidence category assigned to a Bot API method."""

    VERIFIED = "verified"
    INFERRED = "inferred"
    UNVERIFIED = "unverified"


def load() -> dict[str, Any]:
    """Load the bundled API method verification data."""
    path = Path(__file__).with_name("_coverage.json")
    with path.open(encoding="utf-8") as coverage_file:
        return cast(dict[str, Any], json.load(coverage_file))


def status(method: str) -> VerificationStatus:
    """Look up a method's verification status; unknown names are unverified."""
    entry = load().get(method)
    if isinstance(entry, dict):
        value = entry.get("status", VerificationStatus.UNVERIFIED.value)
    else:
        value = entry
    try:
        return VerificationStatus(value)
    except (ValueError, TypeError):
        return VerificationStatus.UNVERIFIED


def main() -> int:
    """Print the method verification table and return success."""
    methods = load()
    print(f"{'Method':<32} {'Status':<12} Bot API")
    print("-" * 64)
    for method, entry in sorted(methods.items()):
        if isinstance(entry, dict):
            method_status = entry.get("status", "unverified")
            api_version = entry.get("api_version", "-")
        else:
            method_status = entry
            api_version = "-"
        print(f"{method:<32} {method_status:<12} {api_version}")
    return 0
