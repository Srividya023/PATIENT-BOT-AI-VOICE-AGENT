"""Phone-number normalization and outbound-call safety guard."""

from __future__ import annotations

import re


ASSESSMENT_NUMBER = "+18054398008"


def normalize_phone_number(raw: str) -> str:
    """Normalize common US phone formats to E.164.

    This intentionally supports only the assessment use case: US-style numbers
    with optional punctuation, spaces, and a leading country code.
    """
    if raw is None or not str(raw).strip():
        raise ValueError("Phone number is required.")

    text = str(raw).strip()
    digits = re.sub(r"\D", "", text)
    if len(digits) == 10:
        digits = f"1{digits}"
    if len(digits) != 11 or not digits.startswith("1"):
        raise ValueError(f"Unsupported phone number format: {raw!r}")
    return f"+{digits}"


def assert_allowed_target(raw_target: str, allowed_target: str = ASSESSMENT_NUMBER) -> str:
    """Return normalized target number only if it exactly matches the allowed number."""
    target = normalize_phone_number(raw_target)
    allowed = normalize_phone_number(allowed_target)
    if target != allowed:
        raise ValueError(
            f"Blocked outbound call to {target}. This project may only call {allowed}."
        )
    return target

