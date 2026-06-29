from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.call_runner import CallRunner
from src.config import Settings
from src.logging_utils import configure_logging
from src.scenario_loader import load_scenarios


def main() -> None:
    parser = argparse.ArgumentParser(description="Run multiple Vapi patient scenarios.")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation for real calls.")
    parser.add_argument("--limit", type=int, help="Maximum number of scenarios to run.")
    parser.add_argument("--delay-seconds", type=float, default=5.0, help="Delay between scenarios.")
    parser.add_argument("--no-poll", action="store_true", help="Do not poll after each created call.")
    args = parser.parse_args()

    settings = Settings()
    configure_logging(settings.log_level)
    scenarios = load_scenarios()
    if args.limit:
        scenarios = scenarios[: args.limit]

    print("Safety: this project may only call +1-805-439-8008.")
    if not settings.dry_run and not args.yes:
        confirm = input(
            f"DRY_RUN=false. Place {len(scenarios)} real call(s) only to +1-805-439-8008? "
            "Type YES to continue: "
        )
        if confirm != "YES":
            print("Aborted before placing calls.")
            return

    runner = CallRunner(settings)
    failures: list[tuple[str, str]] = []
    for index, scenario in enumerate(scenarios, start=1):
        print(f"[{index}/{len(scenarios)}] Running {scenario.scenario_id}: {scenario.title}")
        try:
            result = runner.start_call(scenario, poll=not args.no_poll)
            print(result)
        except Exception as exc:  # noqa: BLE001
            message = f"{type(exc).__name__}: {exc}"
            failures.append((scenario.scenario_id, message))
            print(f"FAILED {scenario.scenario_id}: {message}")
        if index < len(scenarios):
            time.sleep(args.delay_seconds)

    if failures:
        print("\nFailures:")
        for scenario_id, message in failures:
            print(f"- {scenario_id}: {message}")


if __name__ == "__main__":
    main()
