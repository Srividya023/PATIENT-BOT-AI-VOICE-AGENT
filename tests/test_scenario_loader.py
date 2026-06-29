import json

import pytest
from pydantic import ValidationError

from src.scenario_loader import get_scenario_by_id, load_scenarios


def test_scenario_loader_loads_at_least_10_scenarios() -> None:
    scenarios = load_scenarios()
    assert len(scenarios) >= 10
    assert scenarios[0].scenario_id == "scenario_01_basic_scheduling"


def test_get_scenario_by_id() -> None:
    scenario = get_scenario_by_id("scenario_02_reschedule_existing_appointment")
    assert scenario.title == "Reschedule existing appointment"
    assert scenario.goal == "Reschedule an existing appointment from Monday afternoon to later in the week."


def test_scenario_missing_target_number_fails_clearly(tmp_path) -> None:
    path = tmp_path / "scenarios.json"
    path.write_text(
        json.dumps(
            [
                {
                    "scenario_id": "bad",
                    "title": "Bad",
                    "patient_name": "Test",
                    "patient_dob": "1990-01-01",
                    "patient_phone": "+18054398008",
                    "goal": "Missing target",
                    "starting_message": "Hi",
                    "patient_personality": "calm",
                    "constraints": [],
                    "success_criteria": [],
                    "bug_hunting_focus": [],
                    "max_call_minutes": 1,
                    "expected_end_condition": "Done"
                }
            ]
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="target_number"):
        load_scenarios(path)
