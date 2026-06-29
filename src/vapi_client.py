from __future__ import annotations

import logging
import time
from typing import Any

import httpx

from src.config import Settings
from src.phone_guard import assert_allowed_target
from src.scenario_loader import Scenario

logger = logging.getLogger(__name__)


FINISHED_STATUSES = {"ended", "completed", "failed", "cancelled", "canceled"}


class VapiClient:
    def __init__(self, settings: Settings, http_client: httpx.Client | None = None) -> None:
        self.settings = settings
        self._client = http_client or httpx.Client(
            base_url=settings.vapi_base_url.rstrip("/"),
            timeout=30,
            headers={
                "Authorization": f"Bearer {settings.vapi_api_key}",
                "Content-Type": "application/json",
            },
        )

    def build_create_call_payload(self, scenario: Scenario) -> dict[str, Any]:
        target_number = assert_allowed_target(
            scenario.target_number, self.settings.allowed_target_number
        )
        variable_values = {
            "patient_name": scenario.patient_name,
            "patient_dob": scenario.patient_dob,
            "patient_phone": scenario.patient_phone,
            "scenario_id": scenario.scenario_id,
            "scenario_title": scenario.title,
            "scenario_goal": scenario.goal,
            "starting_message": scenario.starting_message,
            "patient_personality": scenario.patient_personality,
            "constraints": "\n".join(scenario.constraints),
            "success_criteria": "\n".join(scenario.success_criteria),
            "bug_hunting_focus": "\n".join(scenario.bug_hunting_focus),
            "expected_end_condition": scenario.expected_end_condition,
        }
        return {
            "assistantId": self.settings.vapi_assistant_id,
            "phoneNumberId": self.settings.vapi_phone_number_id,
            "customer": {
                "number": target_number,
                "name": scenario.patient_name,
            },
            "assistantOverrides": {
                "variableValues": {key: str(value) for key, value in variable_values.items()}
            },
        }

    def create_phone_call(self, scenario: Scenario) -> dict[str, Any]:
        payload = self.build_create_call_payload(scenario)
        if self.settings.dry_run:
            logger.info("DRY_RUN=true; not creating live Vapi call.")
            return {
                "call_id": f"dry_run_{scenario.scenario_id}",
                "dry_run": True,
                "payload": payload,
                "raw_response": {"message": "Dry run only. No Vapi request was sent."},
            }

        if not self.settings.vapi_api_key:
            raise ValueError("VAPI_API_KEY is required when DRY_RUN=false.")
        if not self.settings.vapi_assistant_id:
            raise ValueError("VAPI_ASSISTANT_ID is required when DRY_RUN=false.")
        if not self.settings.vapi_phone_number_id:
            raise ValueError("VAPI_PHONE_NUMBER_ID is required when DRY_RUN=false.")

        response = self._client.post("/call", json=payload)
        if response.is_error:
            raise ValueError(
                f"Vapi create call failed with HTTP {response.status_code}: {response.text}"
            )
        data = response.json()
        call_id = data.get("id") or data.get("call_id")
        if not call_id:
            raise ValueError(f"Vapi response did not include id: {data}")
        return {"call_id": call_id, "dry_run": False, "payload": payload, "raw_response": data}

    def get_call(self, call_id: str) -> dict[str, Any]:
        if self.settings.dry_run and call_id.startswith("dry_run_"):
            return {
                "id": call_id,
                "status": "dry_run",
                "artifact": {"transcript": "", "recordingUrl": None, "messages": []},
            }
        response = self._client.get(f"/call/{call_id}")
        if response.is_error:
            raise ValueError(
                f"Vapi get call failed with HTTP {response.status_code}: {response.text}"
            )
        return response.json()

    def poll_until_call_finished(self, call_id: str) -> dict[str, Any]:
        deadline = time.monotonic() + self.settings.poll_timeout_seconds
        while time.monotonic() < deadline:
            data = self.get_call(call_id)
            status = str(data.get("status") or "").lower()
            if status in FINISHED_STATUSES:
                return data
            logger.info("Vapi call %s still in status %r; polling again.", call_id, status)
            time.sleep(self.settings.poll_interval_seconds)
        raise TimeoutError(f"Timed out waiting for Vapi call to finish: {call_id}")
