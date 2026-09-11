# AI Usage Log - Stage 2

## Tools used

| Tool | Purpose | How used |
| --- | --- | --- |
| Claude (Anthropic), claude.ai chat | Reviewing my Stage 2 requirements
| AI assistant used for the lab's "AI ON" steps | Part F: AI requirements review | Reviewed my requirements for ambiguity, inconsistency, missing questions and testability. |

## What the AI contributed

- Flagged untestable wording such as "easy to use", "fast" and "secure".
- Asked what happens when an appointment is cancelled twice.
- Suggested SMS reminders, authentication roles and a response-time target.

## What I did with it

**Accepted**

- Conflict prevention for the same practitioner and time (FR-06, AC-02).
- The cancel-twice scenario (FR-07, AC-04).

**Modified**

- The response-time target became a provisional NFR and an open question, because the brief gives no number.

**Rejected or left unverified**

- SMS reminders (not in the brief).
- AI diagnosis support (unsupported and high clinical risk).
- Authentication roles stayed Unverified: recorded as an open question, not a requirement.

### Assumptions the AI made

The AI assumed features common to clinic systems (reminders, roles, performance numbers) that the client never mentioned. I treated each as an assumption to validate, not as evidence.

### How the AI output was verified

`python -m pytest -q` in `Week5/` (6 passed); each acceptance criterion AC-01 to AC-06 has a matching test. Details in `evidence.txt`.

### What remained my responsibility

Deciding scope and what counted as correct, checking every suggestion against the client brief or the approved design, running the tests, and being able to explain every line I submit.


---

## Detailed record

### Part F - AI Requirements Review: AI ON

Prompt: Act as a software requirements reviewer. Review the SmartCare requirements for ambiguity, inconsistency, missing clarification questions and testability. Do NOT invent new client requirements. For every suggestion, state whether it is based on evidence or is only a question/assumption requiring validation.

**What I did:** I gave the AI reviewer my requirements with the prompt above. In summary it:

- Flagged vague wording ("easy to use", "fast", "secure") as untestable and asked clarification questions - based on my own wording, so useful.

- Asked what happens when an appointment is cancelled twice - useful; this tightened FR-07.

- Suggested SMS reminders, authentication roles and a response-time target - none is in the client brief, so these are assumptions/questions, not evidence.

- Suggested AI diagnosis support - unsupported and unsafe for this scope.

### Part G - VERIFY the AI Review

Classify each significant AI suggestion as Accepted, Modified, Rejected, or Unverified. Explain the evidence used.

**Result:** The full record is in section 8 of the v0.2 specification. Summary:

| **AI suggestion**                              | **Decision**        | **Evidence used**                                                          |
|------------------------------------------------|---------------------|----------------------------------------------------------------------------|
| Conflict prevention for same practitioner/time | Accepted            | Duplicate bookings are an explicit problem in the brief.                   |
| Cancel-twice scenario                          | Accepted            | Brief mentions inconsistent appointment status; becomes FR-07 and AC-04.   |
| Response-time target                           | Modified            | Brief only says "manageable"; kept as a provisional NFR and open question. |
| Authentication roles                           | Unverified          | No policy supplied; open question.                                         |
| SMS reminders                                  | Rejected (for v0.2) | No evidence in the brief.                                                  |
| AI diagnosis                                   | Rejected            | Unsupported, high clinical risk.                                           |

### 8. AI Requirements Review Record

AI was used only to review for ambiguity, inconsistency, missing questions and testability. Suggestions that introduced new features were not accepted as requirements without client evidence.

| AI suggestion                                                   | Evidence?                                         | Decision            | Reason                                                                           | Verification                                                 |
|-----------------------------------------------------------------|---------------------------------------------------|---------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------|
| SMS reminders                                                   | No - not in the brief                             | Rejected (for v0.2) | Feature invention; could be raised as a client question later.                   | Re-read brief; nothing mentions reminders.                   |
| Add a numeric performance target (e.g. "under 2 s")             | Partial - brief asks for a manageable system only | Modified            | Kept as a clarification question; no invented number is treated as confirmed.    | NFR-05 reworded as provisional.                              |
| Add authentication and user roles                               | No confirmed evidence                             | Unverified          | Important security question, but the client has not supplied a policy.           | Kept as an open question (section 7).                        |
| Explicit conflict prevention for the same practitioner and time | Yes - duplicate bookings are an explicit problem  | Accepted            | Directly addresses a stated problem and is testable.                             | FR-06, AC-02; tested in test_acceptance_criteria.py. |
| AI diagnosis / treatment recommendations                        | No                                                | Rejected            | Unsupported and high clinical risk; the client wants no complex hospital system. | Checked against brief and scope list.                        |
