# SmartCare v0.2 - Requirements Specification

## 1. Problem and Scope

SmartCare is a small community clinic that provides GP consultations. It manages patients and appointments with spreadsheets, paper records and manual processes, which causes duplicate bookings, difficulty locating patient records, inconsistent appointment status, limited visibility of practitioner availability, manual cancellations and no reliable appointment history. Management wants a small, maintainable system - not a hospital information system.

**In scope:** patient and practitioner records; patient search by ID; practitioner availability/schedule view; appointment booking with conflict checking; cancellation with retained history; appointment history; input validation.

**Out of scope:** diagnosis and treatment recommendations, payments, insurance, facial-recognition login, SMS reminders and hospital-scale integration.

**Provisional (not yet confirmed):** exact reports, authentication and roles, retention period and detailed availability rules.

## 2. Stakeholders

| Stakeholder               | Need                                                                             | Evidence                                                                                                                                      |
|---------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------|
| Reception / clinic staff  | Create, search and cancel appointments; avoid duplicates; find patients quickly. | Brief: staff report duplicate bookings and difficulty finding patient information.                                                            |
| Practitioners (GPs)       | See their schedule and availability.                                             | Brief: limited visibility of practitioner availability.                                                                                       |
| Patients                  | Accurate appointment records and cancellation status.                            | Brief: inconsistent appointment status; lack of reliable history. Patients are affected users; no direct patient-facing feature is confirmed. |
| Clinic management         | Reliable history, small maintainable system, basic reports.                      | Brief: management wants a small, maintainable system and basic operational reports.                                                           |
| System owner / IT support | Software that is simple to maintain and test.                                    | Derived from "manageable application suitable for a small clinic"; marked as derived, not stated.                                             |

## 3. Functional Requirements

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

## 4. Non-Functional Requirements

NFR-01: Testability: the core business rules shall be testable without a user interface or a database.

NFR-02: Data integrity: appointment status shall stay consistent; the only legal transition is SCHEDULED to CANCELLED.

NFR-03: Maintainability: domain rules, workflow, storage and user interface shall be separate so a change in one does not force changes in the others.

NFR-04: Usability: an invalid entry shall produce an error message that names the field that is wrong.

NFR-05: Performance (provisional): patient search and schedule views shall respond without noticeable delay for a small clinic dataset; the exact target is an open question for the client.

NFR-06: Simplicity: the first version shall use only the Python standard library and no external services.

## 4a. Business Rules

Business rules are facts about how the clinic works. They are not features, but several requirements and acceptance criteria depend on them.

| ID | Business rule | Source | Related | Checked by |
| --- | --- | --- | --- | --- |
| BR-01 | Every patient and every practitioner has a unique ID. | Needed to find records (brief: difficulty locating patient information) | FR-01, FR-02, FR-03 | AC-05 |
| BR-02 | An appointment involves exactly one patient and one practitioner at one date/time. | Assumption A2 | FR-05 | AC-01 |
| BR-03 | A practitioner cannot have two SCHEDULED appointments at the same date/time. | Brief: duplicate bookings | FR-06 | AC-02 |
| BR-04 | Only a SCHEDULED appointment can be cancelled; CANCELLED is a final state. | Brief: inconsistent appointment status | FR-07 | AC-04 |
| BR-05 | A cancelled appointment is never deleted; it stays in history. | Brief: no reliable appointment history | FR-08, FR-10 | AC-03 |
| BR-06 | A cancelled slot becomes free again and can be rebooked. | Assumption A3 | FR-04, FR-06 | AC-06 |
| BR-07 | Required fields must be present and valid before a record is created. | Stage 1 testing (blank and None values were accepted) | FR-11 | Stage 4 and 5 tests |

## 5. User Stories

US-01: As a receptionist, I want create a patient record, so that patient information can be found consistently.

US-02: As a receptionist, I want search for a patient by ID, so that I can quickly locate the correct record.

US-03: As a receptionist, I want book an appointment for a patient with a practitioner, so that clinic visits are scheduled.

US-04: As a receptionist, I want conflicting practitioner bookings to be rejected, so that duplicate bookings are avoided.

US-05: As a receptionist, I want cancel an appointment while keeping its history, so that records stay accurate.

US-06: As a practitioner, I want view my scheduled appointments, so that I can see my workload and availability.

## 6. Acceptance Criteria

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

## 7. Assumptions and Open Questions

**Assumptions**

- A1: The first version is an internal tool used by clinic staff, not a patient-facing system.

- A2: An appointment has exactly one patient and one practitioner.

- A3: Only SCHEDULED appointments block a time slot; a cancelled slot can be rebooked.

- A4: Two appointments conflict when they have the same practitioner and exactly the same date/time (appointment length is not modelled yet).

**Open questions for the client**

- Q1: Which patient details are mandatory, and how is a patient uniquely identified?

- Q2: Is a login required, and which roles may book, cancel and view schedules?

- Q3: How is availability defined (working hours, appointment length, leave)?

- Q4: How long must records be retained, and must existing spreadsheet data be imported?

- Q5: Which reports does management need in the first version?

- Q6: What response time is acceptable (NFR-05)?

## 8. AI Requirements Review Record

AI was used only to review for ambiguity, inconsistency, missing questions and testability. Suggestions that introduced new features were not accepted as requirements without client evidence.

| AI suggestion                                                   | Evidence?                                         | Decision            | Reason                                                                           | Verification                                                 |
|-----------------------------------------------------------------|---------------------------------------------------|---------------------|----------------------------------------------------------------------------------|--------------------------------------------------------------|
| SMS reminders                                                   | No - not in the brief                             | Rejected (for v0.2) | Feature invention; could be raised as a client question later.                   | Re-read brief; nothing mentions reminders.                   |
| Add a numeric performance target (e.g. "under 2 s")             | Partial - brief asks for a manageable system only | Modified            | Kept as a clarification question; no invented number is treated as confirmed.    | NFR-05 reworded as provisional.                              |
| Add authentication and user roles                               | No confirmed evidence                             | Unverified          | Important security question, but the client has not supplied a policy.           | Kept as an open question (section 7).                        |
| Explicit conflict prevention for the same practitioner and time | Yes - duplicate bookings are an explicit problem  | Accepted            | Directly addresses a stated problem and is testable.                             | FR-06, AC-02; tested in test_acceptance_criteria.py. |
| AI diagnosis / treatment recommendations                        | No                                                | Rejected            | Unsupported and high clinical risk; the client wants no complex hospital system. | Checked against brief and scope list.                        |

### Traceability: requirement to evidence to test

| Requirement | Evidence in the client brief | Acceptance criterion | Automated test |
| --- | --- | --- | --- |
| FR-01 | Difficulty locating patient information | AC-05 (setup) | Week8 `test_directory_find_and_duplicates` |
| FR-02 | Difficulty locating patient information | AC-05 | Week5 `test_AC05_patient_search_found_and_not_found` |
| FR-03 | Practitioners must exist before they can be booked | none at Stage 2 | Week8 service test fixtures |
| FR-04 | Limited visibility of practitioner availability | AC-06 | Week8 `test_cancel_retains_history_and_frees_slot` |
| FR-05 | Manage appointments | AC-01 | Week5 `test_AC01_valid_booking_is_scheduled` |
| FR-06 | Duplicate bookings | AC-02 | Week5 `test_AC02_...`; Week8 `test_conflicting_booking_rejected` |
| FR-07 | Manual cancellation; inconsistent status | AC-03, AC-04 | Week5 `test_AC03_...`, `test_AC04_...`; Week7 `test_repeated_cancel_is_illegal_transition` |
| FR-08 | No reliable appointment history | AC-03 | Week5 `test_AC03_cancel_keeps_appointment_in_history` |
| FR-09 | Limited visibility of practitioner availability | none at Stage 2 | Week8 `test_schedule_shows_only_scheduled_sorted_by_time` |
| FR-10 | No reliable appointment history | AC-03 | Week8 `test_patient_history_includes_cancelled` |
| FR-11 | Blank and None values accepted in Stage 1 | none at Stage 2 | Week4 and Week7 invalid-input tests; Week8 `test_directory_find_and_duplicates` |
| FR-12 | Inconsistent appointment status | AC-01, AC-03 | Week7 `test_cancel_scheduled_appointment` |

FR-03, FR-09 and FR-11 had no acceptance criterion at Stage 2. They are first covered by tests in later stages, which is a gap to close if the specification is revised.

### Changes made to this specification as a result of the AI review

- FR-07 now rejects cancelling an appointment that is already CANCELLED (the AI asked what happens on a second cancel), and AC-04 was added.
- NFR-05 was reworded as provisional because the brief gives no response-time target.
- SMS reminders were added to the out-of-scope list and authentication/roles became open question Q2, because neither appears in the client brief.
