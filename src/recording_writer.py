from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

import httpx

from src.scenario_loader import Scenario


def _audio_suffix(recording_url: str) -> str:
    suffix = Path(urlparse(recording_url).path).suffix
    return suffix if suffix in {".wav", ".mp3", ".m4a", ".ogg"} else ".wav"


def _download_recording(recording_url: str, output_path: Path, scenario: Scenario, call_id: str) -> Path:
    audio_path = output_path / f"{scenario.scenario_id}_{call_id}{_audio_suffix(recording_url)}"
    with httpx.stream("GET", recording_url, timeout=60, follow_redirects=True) as response:
        response.raise_for_status()
        with audio_path.open("wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)
    return audio_path


def write_recording_metadata(
    call_data: dict[str, Any],
    scenario: Scenario,
    output_dir: str | Path = "recordings",
    download_audio: bool = True,
) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    call_id = str(call_data.get("call_id") or call_data.get("id") or "unknown_call")
    artifact = call_data.get("artifact") if isinstance(call_data.get("artifact"), dict) else {}
    recording = artifact.get("recording") if isinstance(artifact.get("recording"), dict) else {}
    mono = recording.get("mono") if isinstance(recording.get("mono"), dict) else {}
    recording_url = (
        call_data.get("recording_url")
        or call_data.get("recording")
        or call_data.get("recordingUrl")
        or call_data.get("stereoRecordingUrl")
        or artifact.get("recordingUrl")
        or artifact.get("stereoRecordingUrl")
        or recording.get("stereoUrl")
        or mono.get("combinedUrl")
    )
    local_audio_file = None
    recording_download_error = None
    if download_audio and recording_url:
        try:
            local_audio_file = str(_download_recording(recording_url, output_path, scenario, call_id))
        except httpx.HTTPError as exc:
            recording_download_error = str(exc)

    metadata = {
        "call_id": call_id,
        "scenario_id": scenario.scenario_id,
        "scenario_title": scenario.title,
        "call_status": call_data.get("call_status") or call_data.get("status"),
        "recording_url": recording_url,
        "local_audio_file": local_audio_file,
        "recording_download_error": recording_download_error,
        "public_log_url": call_data.get("public_log_url"),
        "start_timestamp": call_data.get("start_timestamp") or call_data.get("started_at") or call_data.get("startedAt"),
        "end_timestamp": call_data.get("end_timestamp") or call_data.get("ended_at") or call_data.get("endedAt"),
        "duration": call_data.get("duration") or call_data.get("duration_ms"),
        "written_at": datetime.now(UTC).isoformat(),
        "note": "Audio is downloaded when Vapi provides a public recording URL. If download fails, use recording_url or the Vapi dashboard.",
    }
    file_path = output_path / f"{scenario.scenario_id}_{call_id}.json"
    file_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return file_path
