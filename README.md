# AI Patient Voice Agent for Autonomous Voice Bot Evaluation

A Python scenario runner that uses Vapi to place realistic patient calls to Pretty Good AI's office bot, then saves transcripts, recording metadata, call logs, and bug-report drafts.

## Why Vapi

Vapi handles outbound phone calls, speech-to-text, text-to-speech, turn-taking, call audio, recordings, and transcripts. Python stays focused on experiment control, strict phone-number safety, API integration, and local evidence collection.

## Safety

This project may only call the assessment number: `+1-805-439-8008`, normalized internally as `+18054398008`.

`DRY_RUN=true` is the default. In dry-run mode, the runner validates the number, builds the Vapi payload, writes a call log, and does not contact Vapi.

## Prerequisites

- Python 3.11+
- A Vapi account
- A Vapi assistant configured with `prompts/vapi_assistant_prompt.md`
- A Vapi phone number ID, such as a free Vapi number if available on your account

## Vapi Setup

1. Create a Vapi assistant.
2. Paste `prompts/vapi_assistant_prompt.md` into the assistant prompt/system instructions.
3. Set the assistant first message/welcome message to `{{starting_message}}`.
4. Create or claim a Vapi phone number.
5. Copy your private API key, assistant ID, and phone number ID into `.env`.

## Install

```bash
cd vapi-patient-voice-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Never commit `.env` or real API keys.

## Environment Variables

```bash
VOICE_PROVIDER=vapi
VAPI_API_KEY=
VAPI_ASSISTANT_ID=
VAPI_PHONE_NUMBER_ID=
VAPI_BASE_URL=https://api.vapi.ai
ALLOWED_TARGET_NUMBER=+18054398008
DRY_RUN=true
POLL_INTERVAL_SECONDS=10
POLL_TIMEOUT_SECONDS=600
LOG_LEVEL=INFO
```

## Dry Run

```bash
python scripts/run_call.py --scenario scenario_01_simple_scheduling
```

This writes a dry-run call log under `call_logs/` and places no real call.

## One Real Call

Set Vapi credentials in `.env`, set `DRY_RUN=false`, then run:

```bash
python scripts/run_call.py --scenario scenario_01_simple_scheduling
```

The phone guard still blocks every destination except `+18054398008`.

## All Scenarios

```bash
python scripts/run_all_scenarios.py --limit 10
```

When `DRY_RUN=false`, the script asks for explicit confirmation before placing calls. Use `--yes` only after verifying your `.env`.

## Fetch Result Later

```bash
python scripts/fetch_call_result.py --call-id <vapi_call_id> --scenario scenario_01_simple_scheduling
```

Outputs are saved to:

- `transcripts/` for clean `.txt` transcripts and structured transcript JSON when present
- `recordings/` for recording URL metadata
- `call_logs/` for dry-run logs, create-call responses, and raw call details

## Bug Report Draft

```bash
python scripts/generate_bug_report.py
```

This creates `bug_report_draft.md` using simple offline heuristics. It flags possible issues but does not claim bugs with certainty.

## Tests

```bash
pytest
```

Unit tests do not call Vapi.

## Vapi Payload Shape

The runner creates calls with:

```json
{
  "assistantId": "your-assistant-id",
  "phoneNumberId": "your-phone-number-id",
  "customer": {
    "number": "+18054398008"
  },
  "assistantOverrides": {
    "variableValues": {
      "patient_name": "Maya Patel",
      "starting_message": "Hi, I wanted to see if I can come in this Sunday around 10 in the morning."
    }
  }
}
```
