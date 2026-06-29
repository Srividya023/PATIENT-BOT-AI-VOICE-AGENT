import pytest

from src.config import Settings
from src.scenario_loader import get_scenario_by_id
from src.vapi_client import VapiClient


def test_vapi_payload_includes_expected_dynamic_variables() -> None:
    settings = Settings(
        DRY_RUN=True,
        VAPI_ASSISTANT_ID="assistant_123",
        VAPI_PHONE_NUMBER_ID="phone_123",
        ALLOWED_TARGET_NUMBER="+18054398008",
    )
    scenario = get_scenario_by_id("scenario_06_weekend_or_holiday_scheduling")
    payload = VapiClient(settings).build_create_call_payload(scenario)
    variables = payload["assistantOverrides"]["variableValues"]

    assert payload["assistantId"] == "assistant_123"
    assert payload["phoneNumberId"] == "phone_123"
    assert payload["customer"]["number"] == "+18054398008"
    assert variables["scenario_id"] == "scenario_06_weekend_or_holiday_scheduling"
    assert "Sunday" in variables["scenario_goal"]
    assert "valid availability" in variables["expected_end_condition"]


def test_vapi_payload_dynamic_values_are_strings() -> None:
    settings = Settings(
        DRY_RUN=True,
        VAPI_ASSISTANT_ID="assistant_123",
        VAPI_PHONE_NUMBER_ID="phone_123",
    )
    scenario = get_scenario_by_id("scenario_01_basic_scheduling")
    payload = VapiClient(settings).build_create_call_payload(scenario)
    values = payload["assistantOverrides"]["variableValues"].values()
    assert all(isinstance(value, str) for value in values)


def test_non_allowed_target_number_fails_clearly() -> None:
    settings = Settings(DRY_RUN=True, VAPI_ASSISTANT_ID="assistant_123", VAPI_PHONE_NUMBER_ID="phone_123")
    scenario = get_scenario_by_id("scenario_01_basic_scheduling").model_copy(
        update={"target_number": "+14155550123"}
    )
    with pytest.raises(ValueError, match="Blocked outbound call"):
        VapiClient(settings).build_create_call_payload(scenario)
