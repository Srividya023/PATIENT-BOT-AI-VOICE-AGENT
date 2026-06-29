import pytest

from src.phone_guard import assert_allowed_target, normalize_phone_number


def test_phone_number_normalization_accepts_assessment_formats() -> None:
    assert normalize_phone_number("+1-805-439-8008") == "+18054398008"
    assert normalize_phone_number("+18054398008") == "+18054398008"
    assert normalize_phone_number("(805) 439-8008") == "+18054398008"


def test_phone_guard_blocks_non_allowed_numbers() -> None:
    with pytest.raises(ValueError, match="Blocked outbound call"):
        assert_allowed_target("+14155550123", "+18054398008")


def test_phone_guard_allows_only_configured_assessment_number() -> None:
    assert assert_allowed_target("+1-805-439-8008", "+18054398008") == "+18054398008"

