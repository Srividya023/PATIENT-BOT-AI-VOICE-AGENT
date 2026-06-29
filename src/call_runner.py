from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.config import Settings
from src.phone_guard import assert_allowed_target
from src.recording_writer import write_recording_metadata
from src.scenario_loader import Scenario
from src.transcript_writer import write_transcript
from src.vapi_client import VapiClient


class CallRunner:
    def __init__(self, settings: Settings, voice_client: VapiClient | None = None) -> None:
        self.settings = settings
        self.voice_client = voice_client or VapiClient(settings)

    def start_call(
        self,
        scenario: Scenario,
        target_number_override: str | None = None,
        poll: bool = True,
    ) -> dict[str, Any]:
        if target_number_override:
            scenario = scenario.model_copy(update={"target_number": target_number_override})
        assert_allowed_target(scenario.target_number, self.settings.allowed_target_number)
        created = self.voice_client.create_phone_call(scenario)
        call_log_path = self.write_call_log(scenario, created)

        result: dict[str, Any] = {"call_log": str(call_log_path), "created": created}
        if created.get("dry_run") or not poll:
            return result

        call_data = self.voice_client.poll_until_call_finished(str(created["call_id"]))
        result["call_data"] = call_data
        result["transcript_file"] = str(write_transcript(call_data, scenario))
        result["recording_metadata_file"] = str(write_recording_metadata(call_data, scenario))
        self.write_call_log(scenario, {"created": created, "call_data": call_data})
        return result

    @staticmethod
    def write_call_log(
        scenario: Scenario, payload: dict[str, Any], output_dir: str | Path = "call_logs"
    ) -> Path:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        call_id = str(payload.get("call_id") or payload.get("created", {}).get("call_id") or "unknown")
        file_path = output_path / f"{scenario.scenario_id}_{call_id}.json"
        log_payload = {
            "scenario_id": scenario.scenario_id,
            "scenario_title": scenario.title,
            "written_at": datetime.now(UTC).isoformat(),
            **payload,
        }
        file_path.write_text(json.dumps(log_payload, indent=2), encoding="utf-8")
        return file_path
