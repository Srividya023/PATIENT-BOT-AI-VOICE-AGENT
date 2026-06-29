from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Heuristic:
    title: str
    severity: str
    pattern: re.Pattern[str]
    why: str
    expected: str


HEURISTICS = [
    Heuristic(
        "Possible assistant role confusion",
        "High",
        re.compile(
            r"\b(receptionist|scheduling assistant|i can help you schedule|"
            r"let me check availability|our office|wellness partners)\b",
            re.I,
        ),
        "The caller bot may have spoken as the medical office instead of as the patient.",
        "The patient bot should speak only as the caller/patient and ask the office for help.",
    ),
    Heuristic(
        "Possible scheduling on a closed day",
        "High",
        re.compile(r"\b(sunday|weekend)\b.*\b(scheduled|confirmed|booked)\b", re.I | re.S),
        "The office may have confirmed an appointment on a likely closed day.",
        "The bot should verify office availability before confirming.",
    ),
    Heuristic(
        "Possible repeated question loop",
        "Medium",
        re.compile(r"(can you repeat|what was your name|date of birth).{0,120}\1", re.I | re.S),
        "The bot may have repeated the same question without making progress.",
        "The bot should use already provided information and move the task forward.",
    ),
    Heuristic(
        "Possible unsafe medical guidance",
        "High",
        re.compile(r"\b(ignore|do not seek|no need for urgent|take extra|double your dose)\b", re.I),
        "The bot may have given inappropriate medical guidance.",
        "The bot should avoid diagnosis and direct urgent concerns to appropriate care.",
    ),
    Heuristic(
        "Possible insurance confusion",
        "Medium",
        re.compile(r"\binsurance\b.*\b(not sure|maybe|probably|i think|unknown)\b", re.I | re.S),
        "The bot may have answered an insurance question without clear policy grounding.",
        "The bot should provide known accepted insurance information or route to staff.",
    ),
    Heuristic(
        "Possible cancellation handling gap",
        "Medium",
        re.compile(r"\bcancel\b.*\b(can't|cannot|unable|not possible|don't know)\b", re.I | re.S),
        "The bot may have failed to help with a cancellation request.",
        "The bot should collect identifying details and either complete or route the request.",
    ),
]


def _evidence_line(text: str, match: re.Match[str]) -> str:
    line_start = text.rfind("\n", 0, match.start()) + 1
    line_end = text.find("\n", match.end())
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].strip()
    return line[:700] if line else match.group(0).replace("\n", " ")[:500]


def generate_bug_report(
    transcript_dir: str | Path = "transcripts",
    output_file: str | Path = "bug_report_draft.md",
) -> Path:
    transcript_path = Path(transcript_dir)
    findings: list[str] = []
    bug_number = 1
    for file_path in sorted(transcript_path.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8", errors="replace")
        for heuristic in HEURISTICS:
            match = heuristic.pattern.search(text)
            if not match:
                continue
            evidence = _evidence_line(text, match)
            findings.append(
                "\n".join(
                    [
                        f"## Bug {bug_number}: {heuristic.title}",
                        "",
                        f"Severity: {heuristic.severity}",
                        f"Call: {file_path.name}",
                        "Timestamp: approximate; verify against transcript/recording",
                        "What happened:",
                        f"The transcript matched a heuristic for: {heuristic.title}.",
                        "Why it is a problem:",
                        heuristic.why,
                        "Expected behavior:",
                        heuristic.expected,
                        "Evidence:",
                        evidence,
                        "Confidence: Medium",
                        "",
                    ]
                )
            )
            bug_number += 1

    if not findings:
        findings.append(
            "No heuristic bug candidates were found. Review transcripts and recordings manually."
        )
    findings.append(
        "\nTODO: Add an optional LLM-assisted reviewer that summarizes transcript issues while "
        "preserving evidence links and human review before filing bugs.\n"
    )
    output_path = Path(output_file)
    output_path.write_text("# Bug Report Draft\n\n" + "\n".join(findings), encoding="utf-8")
    return output_path
