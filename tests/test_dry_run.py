from src.config import Settings
from src.scenario_loader import get_scenario_by_id
from src.vapi_client import VapiClient


class ExplodingClient:
    def post(self, *args, **kwargs):  # noqa: ANN002, ANN003
        raise AssertionError("Dry run must not call Vapi")


def test_dry_run_does_not_call_vapi() -> None:
    settings = Settings(DRY_RUN=True, VAPI_ASSISTANT_ID="assistant", VAPI_PHONE_NUMBER_ID="phone")
    scenario = get_scenario_by_id("scenario_01_basic_scheduling")
    client = VapiClient(settings, http_client=ExplodingClient())
    result = client.create_phone_call(scenario)
    assert result["dry_run"] is True
    assert result["call_id"] == "dry_run_scenario_01_basic_scheduling"
