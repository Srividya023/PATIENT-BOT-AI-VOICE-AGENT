from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.call_runner import CallRunner
from src.config import Settings
from src.logging_utils import configure_logging
from src.scenario_loader import get_scenario_by_id


def main() -> None:
    parser = argparse.ArgumentParser(description="Run one Vapi patient scenario.")
    parser.add_argument("--scenario", required=True, help="Scenario ID, e.g. scenario_01_simple_scheduling")
    parser.add_argument("--no-poll", action="store_true", help="Create the call but do not poll for results.")
    parser.add_argument("--target-number", help="Optional target override; still must pass safety guard.")
    args = parser.parse_args()

    settings = Settings()
    configure_logging(settings.log_level)
    scenario = get_scenario_by_id(args.scenario)
    runner = CallRunner(settings)
    result = runner.start_call(
        scenario,
        target_number_override=args.target_number,
        poll=not args.no_poll,
    )
    print(json.dumps(result, indent=2))
    if settings.dry_run:
        print("DRY_RUN=true, so no live Vapi call was placed.")


if __name__ == "__main__":
    main()
