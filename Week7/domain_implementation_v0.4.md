# SmartCare v0.4 - Domain Implementation Workbook

## 1. UML-to-Code Trace

| UML element                            | Python element                                              | Implemented? | Notes                                                       |
|----------------------------------------|-------------------------------------------------------------|--------------|-------------------------------------------------------------|
| Patient.patient_id                     | Patient.patient_id (frozen dataclass field)                 | Yes          | Non-empty string, trimmed; immutable                        |
| Patient.name                           | Patient.name                                                | Yes          | Non-empty string, trimmed; immutable                        |
| Practitioner.practitioner_id           | Practitioner.practitioner_id                                | Yes          | Non-empty string; immutable                                 |
| Practitioner.name                      | Practitioner.name                                           | Yes          | Non-empty string; immutable                                 |
| Practitioner.specialty                 | Practitioner.specialty                                      | Yes          | Non-empty string; immutable                                 |
| Appointment.appointment_id             | Appointment.appointment_id (property over `_appointment_id`) | Yes          | Required non-empty string                                   |
| Appointment.patient (association)      | Appointment.patient (property)                              | Yes          | Must be a Patient object, not an ID (TypeError)             |
| Appointment.practitioner (association) | Appointment.practitioner (property)                         | Yes          | Must be a Practitioner object (TypeError)                   |
| Appointment.scheduled_at               | Appointment.scheduled_at (property)                         | Yes          | Must be a datetime (TypeError)                              |
| Appointment.status                     | Appointment.status (read-only property over `_status`)       | Yes          | Starts SCHEDULED; cannot be assigned from outside           |
| Appointment.cancel()                   | Appointment.cancel()                                        | Yes          | SCHEDULED to CANCELLED only                                 |
| AppointmentStatus (enum)               | AppointmentStatus                                           | Yes          | SCHEDULED, CANCELLED                                        |
| (not in UML) agreed exception          | InvalidStatusTransition(ValueError)                         | Added        | Named error for an illegal transition; no structural change |

## 2. Domain Invariants

| Class        | Invariant / rule                                                           | How protected                                            |
|--------------|----------------------------------------------------------------------------|----------------------------------------------------------|
| Patient      | patient_id and name are valid, non-empty strings and never change          | Constructor validation; frozen (immutable) dataclass     |
| Practitioner | practitioner_id, name and specialty are valid and never change             | Constructor validation; frozen dataclass                 |
| Appointment  | patient and practitioner are domain objects and scheduled_at is a datetime | Type checks in the constructor                           |
| Appointment  | The only legal status change is SCHEDULED to CANCELLED                     | cancel() checks the current status; status has no setter |
| Appointment  | A cancelled appointment remains as an object (history)                     | Nothing deletes it; cancel() only changes status         |
| Appointment  | No repeated cancellation                                                   | cancel() raises InvalidStatusTransition                  |

## 3. Composition / Inheritance Decisions

| Relationship                   | Decision                                       | Rationale                                                                                  |
|--------------------------------|------------------------------------------------|--------------------------------------------------------------------------------------------|
| Patient - Appointment          | Association (Appointment holds a Patient)      | An appointment is not a kind of patient; many appointments share one patient.              |
| Practitioner - Appointment     | Association (Appointment holds a Practitioner) | Same reasoning; a practitioner exists independently of any appointment.                    |
| Appointment - status           | Composition of a value (enum field)            | Status is part of the appointment's own state and has no life of its own.                  |
| Domain - persistence           | Separate concern (no inheritance or import)    | No SQL or database code in the domain; storage comes in Stage 5.                           |
| Doctor / Clinic / Notification | Not modelled                                   | No requirement; Doctor would be a Practitioner subclass only if it needed extra behaviour. |

## 4. AI Pair-Programming Record

| AI contribution                                              | Conforms? | Decision | Reason                                         | Verification                                                               |
|--------------------------------------------------------------|-----------|----------|------------------------------------------------|----------------------------------------------------------------------------|
| Appointment class                                            | Partly    | Modify   | Matched the UML but exposed public status.     | Status made private/read-only; test_status_cannot_be_assigned_from_outside |
| Generic Exception on illegal cancel()                        | Partly    | Modify   | Callers cannot recognise the specific failure. | InvalidStatusTransition; test_repeated_cancel_is_illegal_transition        |
| AppointmentStatus enum                                       | Yes       | Accept   | Makes the two states explicit.                 | UML-to-code trace; transition tests                                        |
| SQL persistence inside Appointment                           | No        | Reject   | Not in the UML; couples domain to a database.  | Review: no sqlite3 or SQL in domain.py                                     |
| NotificationManager dependency and PatientRecord inheritance | No        | Reject   | No requirement; wrong relationship (not is-a). | Review: no extra imports; UML association kept                             |

## 5. Updated UML

No justified structural change from v0.3, so the UML is not redrawn (see domain_model_v0.3.md, Figure 1). The implementation added only details that do not change classes, attributes or multiplicities:

- InvalidStatusTransition exception - agreed in the lab prompt ("enum/exception"); makes the illegal-transition failure explicit.

- Patient and Practitioner are immutable (frozen) and Appointment exposes read-only properties - enforces the encapsulation the UML implies.

- FR-06 (no double booking) is still not in Appointment: one appointment cannot see the others. It is deliberately left for the service layer in Stage 5.
