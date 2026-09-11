# Stage 2 Lab

AI OFF -> AI ON -> VERIFY | 1 hour

## Part A - Client Brief: AI OFF

SmartCare uses spreadsheets and paper records. Staff report duplicate bookings, difficulty finding patient information, inconsistent appointment status and limited appointment history. Management wants a small, maintainable patient, practitioner and appointment system.

**My reading of the brief:** Key evidence: duplicate bookings; difficulty finding patient information; inconsistent appointment status; limited appointment history; management wants a small, maintainable patient, practitioner and appointment system.

## Part B - Stakeholders and Scope: AI OFF

Identify at least four stakeholders. Create In Scope and Out of Scope lists. Label uncertain features as provisional rather than confirmed.

**Stakeholders:** Reception/clinic staff; practitioners (GPs); patients; clinic management; system owner/IT support (derived).

**In scope:** patient, practitioner and appointment records; patient search; practitioner availability and schedule view; booking with conflict checking; cancellation with retained history; appointment history; validation.

**Out of scope:** diagnosis and treatment recommendations; payments; insurance processing; facial-recognition login; SMS reminders; hospital-scale integration.

**Provisional:** exact reports; authentication/roles; retention period; detailed availability rules (working hours, appointment length); performance target.

## Part C - Functional Requirements: AI OFF

Write 8-12 numbered functional requirements using FR-01, FR-02 and so on. Each should describe one observable capability.

FR-01: The system shall allow staff to create a patient record with a unique patient ID and a name.

FR-02: The system shall allow staff to search for a patient by patient ID.

FR-03: The system shall allow staff to create a practitioner record with a unique practitioner ID, name and specialty.

FR-04: The system shall show whether a practitioner is available (not already booked) at a given date and time.

FR-05: The system shall allow staff to create an appointment linking one patient, one practitioner and a date/time, with initial status SCHEDULED.

FR-06: The system shall reject an appointment that would give a practitioner two SCHEDULED appointments at the same date and time.

FR-07: The system shall allow staff to cancel a SCHEDULED appointment and shall reject cancelling an appointment that is already CANCELLED.

FR-08: The system shall retain cancelled appointments as history with status CANCELLED instead of deleting them.

FR-09: The system shall allow staff to view a practitioner's scheduled appointments in date/time order.

FR-10: The system shall allow staff to view a patient's appointment history, including cancelled appointments.

FR-11: The system shall validate required fields (IDs, names, specialty, date/time) and reject missing, blank or invalid values with a clear error message.

FR-12: The system shall display each appointment's current status (SCHEDULED or CANCELLED) consistently wherever it is shown.

## Part D - Non-Functional Requirements: AI OFF

Write 4-6 numbered non-functional requirements covering appropriate qualities such as reliability, maintainability, usability, data integrity or testability.

NFR-01: Testability: the core business rules shall be testable without a user interface or a database.

NFR-02: Data integrity: appointment status shall stay consistent; the only legal transition is SCHEDULED to CANCELLED.

NFR-03: Maintainability: domain rules, workflow, storage and user interface shall be separate so a change in one does not force changes in the others.

NFR-04: Usability: an invalid entry shall produce an error message that names the field that is wrong.

NFR-05: Performance (provisional): patient search and schedule views shall respond without noticeable delay for a small clinic dataset; the exact target is an open question for the client.

NFR-06: Simplicity: the first version shall use only the Python standard library and no external services.

## Part E - User Stories and Acceptance Criteria: AI OFF

Write 4-6 user stories. For at least three, create Given-When-Then acceptance criteria including one negative or failure scenario.

US-01: As a receptionist, I want create a patient record, so that patient information can be found consistently.

US-02: As a receptionist, I want search for a patient by ID, so that I can quickly locate the correct record.

US-03: As a receptionist, I want book an appointment for a patient with a practitioner, so that clinic visits are scheduled.

US-04: As a receptionist, I want conflicting practitioner bookings to be rejected, so that duplicate bookings are avoided.

US-05: As a receptionist, I want cancel an appointment while keeping its history, so that records stay accurate.

US-06: As a practitioner, I want view my scheduled appointments, so that I can see my workload and availability.

**Acceptance criteria (Given-When-Then) - six criteria, three of them negative or failure scenarios:**

AC-01 [US-03 / FR-05]  
GIVEN a valid patient, a valid practitioner and a time the practitioner is free  
WHEN staff create an appointment  
THEN the system creates it with status SCHEDULED.

AC-02 [US-04 / FR-06 (negative)]  
GIVEN a practitioner already has a SCHEDULED appointment at 10:00  
WHEN staff try to book another appointment at 10:00  
THEN the system rejects the booking and the existing appointment is unchanged.

AC-03 [US-05 / FR-07, FR-08]  
GIVEN an appointment with status SCHEDULED  
WHEN authorised staff cancel it  
THEN its status becomes CANCELLED and it remains in the patient's history.

AC-04 [US-05 / FR-07 (negative)]  
GIVEN an appointment that is already CANCELLED  
WHEN staff try to cancel it again  
THEN the system rejects the request and the status stays CANCELLED.

AC-05 [US-02 / FR-02 (includes negative)]  
GIVEN a registered patient with ID P1  
WHEN staff search for P1 and for an unknown ID  
THEN the patient is shown for P1 and "not found" is reported for the unknown ID.

AC-06 [Assumption A3 / FR-06]  
GIVEN a CANCELLED appointment at 10:00 for a practitioner  
WHEN staff book a new appointment at 10:00 for that practitioner  
THEN the booking succeeds because only SCHEDULED appointments block a slot.

## Part F - AI Requirements Review: AI ON

Prompt: Act as a software requirements reviewer. Review the SmartCare requirements for ambiguity, inconsistency, missing clarification questions and testability. Do NOT invent new client requirements. For every suggestion, state whether it is based on evidence or is only a question/assumption requiring validation.

**What I did:** I gave the AI reviewer my requirements with the prompt above. In summary it:

- Flagged vague wording ("easy to use", "fast", "secure") as untestable and asked clarification questions - based on my own wording, so useful.

- Asked what happens when an appointment is cancelled twice - useful; this tightened FR-07.

- Suggested SMS reminders, authentication roles and a response-time target - none is in the client brief, so these are assumptions/questions, not evidence.

- Suggested AI diagnosis support - unsupported and unsafe for this scope.

## Part G - VERIFY the AI Review

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

## Part H - Finalise SmartCare v0.2

Submit stakeholder analysis, scope, 8-12 FRs, 4-6 NFRs, 4-6 user stories, acceptance criteria, assumptions/open questions and selected AI review evidence.

**Result:** Submitted as requirements_v0.2.md (stakeholders, scope, 12 FRs, 6 NFRs, 6 user stories, 6 acceptance criteria, assumptions/open questions and the AI review record). Technical evidence: smartcare_v02.py is a small prototype and test_acceptance_criteria.py turns the six acceptance criteria into tests (6 passed - see evidence.txt).

## Reflection

In 150-250 words: What did AI notice that you missed? What did AI invent or overreach on? Which requirement changed after review? Why must requirements have evidence?

AI noticed that several statements were still too vague to test, especially "easy to use", "fast" and "secure". That was useful because it pushed me to turn vague quality goals into clarification questions instead of pretending an arbitrary number was confirmed. AI also overreached by suggesting features such as SMS reminders, authentication roles and other common clinic-system functions that the client never mentioned; I rejected them for v0.2 or kept them as open questions. The requirement that changed most was duplicate-booking prevention: it became an explicit, testable FR-06 with a negative acceptance criterion, and cancellation became stricter in FR-07 after the review asked what happens when an appointment is cancelled twice. Requirements must have evidence because they control scope, cost and risk and are the basis for design and tests. An AI-generated idea is not a stakeholder commitment, so every accepted item was traced to the client brief or recorded as an assumption or open question to validate.

## Evidence (captured output)

Run from the `Week5/` folder. The full log is in [`evidence.txt`](evidence.txt).

```text

$ python smartcare_v02.py
Rejected: Practitioner already booked at that time
[{'id': 'A1', 'patient_id': 'P1', 'practitioner': 'Dr. John Doe', 'time': '2026-10-08 10:00', 'status': 'CANCELLED'}]

$ python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/repo/Week5/stage02
collecting ... collected 6 items

test_acceptance_criteria.py::test_AC01_valid_booking_is_scheduled PASSED [ 16%]
test_acceptance_criteria.py::test_AC02_conflicting_booking_rejected_and_existing_unchanged PASSED [ 33%]
test_acceptance_criteria.py::test_AC03_cancel_keeps_appointment_in_history PASSED [ 50%]
test_acceptance_criteria.py::test_AC04_cancelling_twice_is_rejected PASSED [ 66%]
test_acceptance_criteria.py::test_AC05_patient_search_found_and_not_found PASSED [ 83%]
test_acceptance_criteria.py::test_AC06_cancelled_slot_can_be_rebooked PASSED [100%]

============================== 6 passed in 0.01s ===============================
```
