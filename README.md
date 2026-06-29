# AI Patient Voice Agent for Autonomous Voice Bot Evaluation

A Python-based AI patient voice bot testing framework that uses Vapi to place realistic patient phone calls, collect transcripts, save call evidence, and generate bug report drafts for healthcare office voice agents.

This project was built for evaluating an AI receptionist / medical office phone bot using structured patient scenarios, safety controls, dry-run testing, transcript analysis, and reproducible evidence collection.

## Features

- Runs realistic patient call scenarios against an office voice bot
- Uses Vapi for outbound calls, speech-to-text, text-to-speech, recordings, and transcripts
- Includes a strict phone-number safety guard
- Supports dry-run mode by default so no real calls are placed accidentally
- Saves structured call logs for every run
- Stores transcripts and recording metadata
- Includes reusable patient scenarios for scheduling, cancellation, insurance, policy, and memory tests
- Generates bug report drafts from collected call evidence
- Includes unit tests for configuration, safety, payload generation, and scenario loading

## Project Purpose

The goal of this project is to test how well a healthcare office AI voice bot handles realistic patient conversations.

It checks for issues such as:

- Appointment scheduling mistakes
- Incorrect cancellation or fee policy answers
- Insurance and location confusion
- Poor memory across multi-turn conversations
- Unsafe or hallucinated medical guidance
- Mishandling caller identity or proxy callers
- Incorrect handling of relative dates like “tomorrow” or “next Monday”

## Tech Stack

- Python 3.11+
- Vapi API
- python-dotenv
- Pydantic
- HTTPX
- Pytest

## Safety First

This project is designed with strict call safety.

The runner only allows calls to the approved assessment number:

```text
+1-805-439-8008
