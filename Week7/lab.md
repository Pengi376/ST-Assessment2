# Stage 4 Lab

DESIGN FIRST -> AI PAIR PROGRAMMING -> REVIEW -> VERIFY | 1hour

## A - Revisit Approved UML

Confirm responsibilities, attributes and relationships before coding.

**Done:** I re-read the approved v0.3 UML. Patient (patient_id, name), Practitioner (practitioner_id, name, specialty), Appointment (appointment_id, patient, practitioner, scheduled_at, status, cancel()), AppointmentStatus (SCHEDULED, CANCELLED); Patient 1 to 0..\* Appointment and Practitioner 1 to 0..\* Appointment.

## B - Implement Patient: AI OFF

Implement Patient with type hints and basic validation.

**Done (AI off):** frozen dataclass; patient_id and name must be non-empty strings (text is trimmed); no database logic.

## C - Implement Practitioner: AI OFF

Implement Practitioner with identifier, name and specialty; no database logic.

**Done (AI off):** frozen dataclass with the same validation for id, name and specialty; no database logic.

## D - Implement Appointment: AI ON

Give AI the approved Appointment UML, business rules and explicit constraints. Ask it to implement only Appointment and agreed enum/exception.

**What I did:** I used the suggested prompt below with the approved UML and business rules, and told the AI to implement only Appointment and the agreed enum/exception.

**Contribution:** a first Appointment class and AppointmentStatus enum. It stayed within scope but needed changes (see E).

## E - Review Generated Code

Check model consistency, unsupported features, public state mutation, unnecessary inheritance, invented dependencies and error handling.

**Review findings:** attributes and cancel() matched the UML; no database, UI, notification or service code was added; BUT status was a public attribute and cancel() raised a generic Exception.

**Decisions:** Modified (public status to private field and read-only property); Modified (generic Exception to InvalidStatusTransition); Rejected (SQL and notification ideas); Accepted (AppointmentStatus enum).

## F - Manual Behaviour Checks

Create valid objects, test invalid input, cancel a scheduled appointment and attempt an illegal repeated transition.

**Result:** All checks are automated in tests/test_domain.py - 16 tests passed (evidence.txt):

| **Check**                      | **Input**                                                                            | **Outcome**                                     |
|--------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------------|
| Valid objects                  | Patient("P1","Alice Smith"), Practitioner("D1","Dr John Doe","GP"), Appointment(...) | Created; status SCHEDULED                       |
| Invalid input                  | blank/None id or name, blank specialty, wrong types, empty appointment id            | ValueError / TypeError                          |
| Cancel a scheduled appointment | appointment.cancel()                                                                 | status becomes CANCELLED; object retained       |
| Illegal repeated transition    | cancel() a second time                                                               | InvalidStatusTransition; status stays CANCELLED |
| Protected state                | appointment.status = ... / patient.name = ...                                        | AttributeError / FrozenInstanceError            |

## G - Refactor

Remove unnecessary code and make implementation simpler and design-consistent.

**Done:** kept the domain deliberately small: one validation helper (`_required`), the enum, the exception and one state-changing operation, with no unused methods or extra getters. The domain module is about 90 lines with no I/O.

## H - AI Engineering Log

Record prompt, generated contribution, decisions and verification evidence.

**Prompt:** the "Suggested AI prompt" at the end of this handout, plus the UML and business rules.

**Generated:** Appointment class and AppointmentStatus enum.

**Decisions:** see section 4 of domain_implementation_v0.4.md.

**Verification:** UML-to-code trace, manual review checklist and 16 automated tests.

## Suggested AI prompt

Act as a Python pair programmer. Implement only the Appointment class from the approved SmartCare UML. Use type hints and an AppointmentStatus enum. Cancelled appointments remain as objects. Do not add database, UI, notification or service classes. Protect status transitions and explain any decision not directly visible in the UML.

## Reflection

Which AI-generated part did you modify or reject? Why? How did the approved design constrain the AI?

I modified two parts of the AI-generated Appointment and rejected one idea. First, the generated class exposed status as a public attribute, so any code could set it back to SCHEDULED; I made it a read-only property backed by a private field so only cancel() can change it. Second, the generated cancel() raised a generic exception; I replaced it with InvalidStatusTransition so callers and tests can recognise exactly this failure. I rejected the suggestion to put SQL and a notification call inside Appointment, because neither is in the approved UML and both would tie the domain to infrastructure. The approved design constrained the AI strongly: the prompt contained the UML, the business rules and an explicit list of things not to add, so the output stayed small and could be checked line by line against the UML-to-code trace. Without the design I would have had nothing to review the code against. The 16 tests in Week7 confirm the invariants.

## Evidence (captured output)

Run from the `Week7/` folder. The full log is in [`evidence.txt`](evidence.txt).

```text

$ python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/repo/Week7/stage04
collecting ... collected 16 items

tests/test_domain.py::test_valid_objects_are_created PASSED              [  6%]
tests/test_domain.py::test_text_is_trimmed PASSED                        [ 12%]
tests/test_domain.py::test_invalid_patient_rejected[-Alice] PASSED       [ 18%]
tests/test_domain.py::test_invalid_patient_rejected[P1-] PASSED          [ 25%]
tests/test_domain.py::test_invalid_patient_rejected[  -Alice] PASSED     [ 31%]
tests/test_domain.py::test_invalid_patient_rejected[None-Alice] PASSED   [ 37%]
tests/test_domain.py::test_invalid_patient_rejected[P1-None] PASSED      [ 43%]
tests/test_domain.py::test_invalid_practitioner_rejected[args0] PASSED   [ 50%]
tests/test_domain.py::test_invalid_practitioner_rejected[args1] PASSED   [ 56%]
tests/test_domain.py::test_invalid_practitioner_rejected[args2] PASSED   [ 62%]
tests/test_domain.py::test_invalid_practitioner_rejected[args3] PASSED   [ 68%]
tests/test_domain.py::test_appointment_requires_domain_objects_and_datetime PASSED [ 75%]
tests/test_domain.py::test_cancel_scheduled_appointment PASSED           [ 81%]
tests/test_domain.py::test_repeated_cancel_is_illegal_transition PASSED  [ 87%]
tests/test_domain.py::test_status_cannot_be_assigned_from_outside PASSED [ 93%]
tests/test_domain.py::test_patient_is_immutable PASSED                   [100%]

============================== 16 passed in 0.02s ==============================
```
