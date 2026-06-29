from __future__ import annotations

import json
from pathlib import Path

from pydantic import AliasChoices, BaseModel, Field, field_validator

from src.phone_guard import normalize_phone_number


class Scenario(BaseModel):
    scenario_id: str
    title: str
    patient_name: str
    patient_dob: str
    patient_phone: str
    target_number: str
    goal: str = Field(validation_alias=AliasChoices("goal", "scenario_goal"))
    starting_message: str
    patient_personality: str
    constraints: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    bug_hunting_focus: list[str] = Field(default_factory=list)
    max_call_minutes: int
    expected_end_condition: str

    @field_validator("target_number", "patient_phone")
    @classmethod
    def normalize_numbers(cls, value: str) -> str:
        return normalize_phone_number(value)


def load_scenarios(path: str | Path = "scenarios/scenarios.json") -> list[Scenario]:
    scenario_path = Path(path)
    if not scenario_path.exists():
        raise FileNotFoundError(f"Scenario file not found: {scenario_path}")

    raw = json.loads(scenario_path.read_text(encoding="utf-8"))
    scenarios_raw = raw["scenarios"] if isinstance(raw, dict) and "scenarios" in raw else raw
    if not isinstance(scenarios_raw, list):
        raise ValueError("Scenario file must contain a list or a {'scenarios': [...]} object.")
    return [Scenario.model_validate(item) for item in scenarios_raw]


def get_scenario_by_id(
    scenario_id: str, path: str | Path = "scenarios/scenarios.json"
) -> Scenario:
    for scenario in load_scenarios(path):
        if scenario.scenario_id == scenario_id:
            return scenario
    raise ValueError(f"Scenario not found: {scenario_id}")
