# Bug Report Draft

## Bug 1: Possible repeated question loop

Severity: Medium
Call: scenario_02_reschedule_with_time_constraint_memory_019f101f-2ccd-733a-baed-b2e3b94cc686.txt
Timestamp: approximate; verify against transcript/recording
What happened:
The transcript matched a heuristic for: Possible repeated question loop.
Why it is a problem:
The bot may have repeated the same question without making progress.
Expected behavior:
The bot should use already provided information and move the task forward.
Evidence:
[00:18] OFFICE_BOT: Please provide your date of birth.
[00:21] PATIENT_BOT: Sure. My date of birth is April eighteenth nineteen ninety six.
Confidence: Medium

## Bug 2: Possible cancellation handling gap

Severity: Medium
Call: scenario_03_cancellation_fee_policy_hallucination_019f1022-3b5f-7aa8-9963-a6648fc47681.txt
Timestamp: approximate; verify against transcript/recording
What happened:
The transcript matched a heuristic for: Possible cancellation handling gap.
Why it is a problem:
The bot may have failed to help with a cancellation request.
Expected behavior:
The bot should collect identifying details and either complete or route the request.
Evidence:
[00:01] PATIENT_BOT: Hi. I need to cancel my appointment for tomorrow, and I wanted to check if there's any cancellation fee.
[00:07] OFFICE_BOT: calling Pivot Point Orthopedics, part of Pretty Good AI. Am I speaking with Pravis?
[00:15] PATIENT_BOT: Yes. This is Pravas Raju.
[00:20] OFFICE_BOT: Please provide your date of birth.
[00:23] PATIENT_BOT: Sure. It's April eighteen nineteen ninety six.
[00:29] OFFICE_BOT: The birthday doesn't match our records, but for demo purposes, I'll accept it. How can I help you today?
[00:37] PATIENT_BOT: I'd like to cancel my appointment for tomorrow, and I wanted to check if there's any cancellation fee or policy I should know about.
[00:49] OFFICE_BOT: Y
Confidence: Medium

## Bug 3: Possible repeated question loop

Severity: Medium
Call: scenario_08_identity_correction_memory_trap_019f102f-78b5-7559-adf9-67a26bf7eade.txt
Timestamp: approximate; verify against transcript/recording
What happened:
The transcript matched a heuristic for: Possible repeated question loop.
Why it is a problem:
The bot may have repeated the same question without making progress.
Expected behavior:
The bot should use already provided information and move the task forward.
Evidence:
[01:12] OFFICE_BOT: I have your phone number as seven seven four three three four eight nine zero nine, and your date of birth as April seventeenth. nineteen ninety Is that correct?
[01:24] PATIENT_BOT: Actually, my date of birth is April eighteenth nineteen ninety six. Can you confirm you have the corrected date of birth and phone number
Confidence: Medium

## Bug 4: Possible insurance confusion

Severity: Medium
Call: scenario_09_multi_intent_context_retention_trap_019f1034-8702-7aa8-99a0-b3db700f4775.txt
Timestamp: approximate; verify against transcript/recording
What happened:
The transcript matched a heuristic for: Possible insurance confusion.
Why it is a problem:
The bot may have answered an insurance question without clear policy grounding.
Expected behavior:
The bot should provide known accepted insurance information or route to staff.
Evidence:
[00:14] PATIENT_BOT: Thank you. I wanted to reschedule my appointment and also check if you accept Aetna PPO insurance.
[00:23] OFFICE_BOT: Can you please provide your date of birth?
[00:27] PATIENT_BOT: Sure. It's April eighteenth nineteen ninety six.
[00:35] OFFICE_BOT: Probably I see you don't have any upcoming appointments to reschedule. Would you like to book a new appointment instead? And, yes, pivot point orthopedics accepts most insurance plans, including Aetna PPO.
Confidence: Medium
