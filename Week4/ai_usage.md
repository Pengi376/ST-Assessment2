# AI Usage Log - Stage 1

## Tools used

| Tool | Purpose | How used |
| --- | --- | --- |
| Claude (Anthropic), claude.ai chat | Reviewing and correcting my Stage 1 package
| AI assistant used for the lab's "AI ON" steps | Part C (tutor) and Part D (alternative version) | Explained my prototype, listed limitations, asked me two questions, and produced a short alternative `add_appointment()` function under a "no database, no GUI" constraint. |

## What the AI contributed

- Explained what my list-of-dictionaries prototype does.
- Listed limitations: missing validation, no duplicate-booking check, no persistence, `None` inputs.

## What I did with it

**Accepted**

- Validation of all three required fields (the single Part G improvement).

**Modified**

- The AI version's `.strip()` calls were not adopted: they crash on `None` (shown in the real output below).

**Rejected or left unverified**

- Facial recognition, AI diagnosis, payments and a database: no evidence in the client brief (Stage 1 tutorial, Activity 4).

### Assumptions the AI made

The AI version assumed the caller owns the list, assumed names are always strings, and assumed no validation was wanted. None of these came from the brief.

### How the AI output was verified

`python -m pytest -q` in `Week4/` (7 passed), and the five Part F cases run against both versions (output below). Details in `evidence.txt`.

### What remained my responsibility

Deciding scope and what counted as correct, checking every suggestion against the client brief or the approved design, running the tests, and being able to explain every line I submit.


---

## Detailed record

### Part F applied to both versions (real output)

The same five test cases were run against the AI-generated `add_appointment()` and against the human version in `smartcare_v01.py`.

```text
AI version
Normal appointment                         -> stored, list length now 1
Blank patient name                         -> stored, list length now 2
Same practitioner + time (2nd booking)     -> stored, list length now 3
patient_name=None                          -> AttributeError: 'NoneType' object has no attribute 'strip'
appointment_time=None                      -> stored, list length now 4

Human version (with the Part G improvement)
Normal appointment                         -> stored, list length now 1
Blank patient name                         -> ValueError: Patient name cannot be empty
Same practitioner + time (2nd booking)     -> stored, list length now 2
patient_name=None                          -> ValueError: Patient name cannot be empty
appointment_time=None                      -> ValueError: Appointment time cannot be empty
```

Both versions accept a duplicate practitioner and time. The AI version also stores blank names and a `None` time, and crashes on a `None` patient name.
