from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.config import Settings
from src.logging_utils import configure_logging
from src.recording_writer import write_recording_metadata
from src.scenario_loader import get_scenario_by_id
from src.transcript_writer import write_transcript
from src.vapi_client import VapiClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch and save a completed Vapi call result.")
    parser.add_argument("--call-id", required=True)
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()

    settings = Settings()
    configure_logging(settings.log_level)
    scenario = get_scenario_by_id(args.scenario)
    client = VapiClient(settings)
    call_data = client.get_call(args.call_id)
    transcript_file = write_transcript(call_data, scenario)
    recording_file = write_recording_metadata(call_data, scenario)
    raw_file = Path("call_logs") / f"{scenario.scenario_id}_{args.call_id}_raw.json"
    raw_file.parent.mkdir(parents=True, exist_ok=True)
    raw_file.write_text(json.dumps(call_data, indent=2), encoding="utf-8")
    print(f"Transcript: {transcript_file}")
    print(f"Recording metadata: {recording_file}")
    print(f"Raw call JSON: {raw_file}")


if __name__ == "__main__":
    main()
