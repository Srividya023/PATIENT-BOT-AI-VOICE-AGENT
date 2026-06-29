from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from src.scenario_loader import Scenario


def _speaker_label(raw_speaker: Any) -> str:
    speaker = str(raw_speaker or "").lower()
    if speaker in {"agent", "vapi_agent", "caller", "patient", "assistant", "bot"}:
        return "PATIENT_BOT"
    if speaker in {"user", "callee", "other", "office", "human"}:
        return "OFFICE_BOT"
    return str(raw_speaker or "UNKNOWN").upper()


def _format_event(event: dict[str, Any]) -> str:
    seconds = (
        event.get("start")
        or event.get("start_ms")
        or event.get("offset")
        or event.get("secondsFromStart")
        or 0
    )
    if isinstance(seconds, int | float) and seconds > 1000:
        seconds = seconds / 1000
    stamp = f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"
    speaker = _speaker_label(event.get("speaker") or event.get("role"))
    text = (
        event.get("text")
        or event.get("content")
        or event.get("message")
        or event.get("transcript")
        or ""
    )
    return f"[{stamp}] {speaker}: {text}".strip()


def _extract_transcript(call_data: dict[str, Any]) -> tuple[list[str], Any]:
    artifact = call_data.get("artifact") if isinstance(call_data.get("artifact"), dict) else {}
    structured = (
        call_data.get("transcript_object")
        or call_data.get("transcript_with_tool_calls")
        or call_data.get("transcript_events")
        or artifact.get("messages")
        or call_data.get("transcript")
        or artifact.get("transcript")
    )
    if isinstance(structured, list):
        return [
            _format_event(item)
            for item in structured
            if isinstance(item, dict) and str(item.get("role", "")).lower() != "system"
        ], structured
    if isinstance(structured, str):
        return [structured], None
    return ["No transcript was present in the Vapi call detail response."], None


def write_transcript(
    call_data: dict[str, Any],
    scenario: Scenario,
    output_dir: str | Path = "transcripts",
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    call_id = str(call_data.get("call_id") or call_data.get("id") or "unknown_call")
    lines, structured = _extract_transcript(call_data)
    started = call_data.get("start_timestamp") or call_data.get("started_at") or call_data.get("startedAt") or ""
    ended = call_data.get("end_timestamp") or call_data.get("ended_at") or call_data.get("endedAt") or ""
    status = call_data.get("call_status") or call_data.get("status") or "unknown"
    duration = call_data.get("duration_ms") or call_data.get("duration") or ""

    note = (
        "Speaker labels are inferred from Vapi transcript metadata and should be verified "
        "against the recording."
    )
    header = [
        f"Call ID: {call_id}",
        f"Scenario: {scenario.scenario_id}",
        f"Title: {scenario.title}",
        f"Started: {started}",
        f"Ended: {ended}",
        f"Duration: {duration}",
        f"Status: {status}",
        f"Written: {datetime.now(UTC).isoformat()}",
        f"Note: {note}",
        "",
    ]
    transcript_file = output_path / f"{scenario.scenario_id}_{call_id}.txt"
    transcript_file.write_text("\n".join(header + lines) + "\n", encoding="utf-8")

    if structured is not None:
        structured_file = output_path / f"{scenario.scenario_id}_{call_id}.json"
        structured_file.write_text(json.dumps(structured, indent=2), encoding="utf-8")
    return transcript_file
