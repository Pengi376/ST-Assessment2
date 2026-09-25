# AI Usage Log - Stage 4

## Tools used

| Tool | Purpose | How used |
| --- | --- | --- |
| Claude (Anthropic), claude.ai chat | Reviewing my Stage 4 implementation. |
| AI assistant used for the lab's "AI ON" steps | Part D: AI pair programmer for the Appointment class | Given the approved UML, business rules and explicit constraints (no database, UI, notification or service classes), and asked to implement only Appointment. |

## What the AI contributed

- A first Appointment class and AppointmentStatus enum.

## What I did with it

**Accepted**

- AppointmentStatus enum.

**Modified**

- Status was a public attribute, so I made it a read-only property over a private field.
- cancel() raised a generic exception, so I replaced it with InvalidStatusTransition.

**Rejected or left unverified**

- SQL inside cancel() and a NotificationManager dependency (neither is in the UML).

### Assumptions the AI made

The generated class assumed status could be changed from outside and that storage and notifications belonged in the domain. The UML says neither.

### How the AI output was verified

`python -m pytest -q` in `Week7/` (16 passed): valid and invalid objects, repeated cancel, protected status and immutability. Details in `evidence.txt`.

### What remained my responsibility

Deciding scope and what counted as correct, checking every suggestion against the client brief or the approved design, running the tests, and being able to explain every line I submit.


---

## Detailed record

### D - Implement Appointment: AI ON

Give AI the approved Appointment UML, business rules and explicit constraints. Ask it to implement only Appointment and agreed enum/exception.

**What I did:** I used the suggested prompt below with the approved UML and business rules, and told the AI to implement only Appointment and the agreed enum/exception.

**Contribution:** a first Appointment class and AppointmentStatus enum. It stayed within scope but needed changes (see E).

### E - Review Generated Code

Check model consistency, unsupported features, public state mutation, unnecessary inheritance, invented dependencies and error handling.

**Review findings:** attributes and cancel() matched the UML; no database, UI, notification or service code was added; BUT status was a public attribute and cancel() raised a generic Exception.

**Decisions:** Modified (public status to private field and read-only property); Modified (generic Exception to InvalidStatusTransition); Rejected (SQL and notification ideas); Accepted (AppointmentStatus enum).

### H - AI Engineering Log

Record prompt, generated contribution, decisions and verification evidence.

**Prompt:** the "Suggested AI prompt" at the end of this handout, plus the UML and business rules.

**Generated:** Appointment class and AppointmentStatus enum.

**Decisions:** see section 4 of domain_implementation_v0.4.md.

**Verification:** UML-to-code trace, manual review checklist and 16 automated tests.

### 4. AI Pair-Programming Record

| AI contribution                                              | Conforms? | Decision | Reason                                         | Verification                                                               |
|--------------------------------------------------------------|-----------|----------|------------------------------------------------|----------------------------------------------------------------------------|
| Appointment class                                            | Partly    | Modify   | Matched the UML but exposed public status.     | Status made private/read-only; test_status_cannot_be_assigned_from_outside |
| Generic Exception on illegal cancel()                        | Partly    | Modify   | Callers cannot recognise the specific failure. | InvalidStatusTransition; test_repeated_cancel_is_illegal_transition        |
| AppointmentStatus enum                                       | Yes       | Accept   | Makes the two states explicit.                 | UML-to-code trace; transition tests                                        |
| SQL persistence inside Appointment                           | No        | Reject   | Not in the UML; couples domain to a database.  | Review: no sqlite3 or SQL in domain.py                                     |
| NotificationManager dependency and PatientRecord inheritance | No        | Reject   | No requirement; wrong relationship (not is-a). | Review: no extra imports; UML association kept                             |
