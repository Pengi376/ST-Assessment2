# Stage 4 Tutorial - Object-Oriented Design Decisions

## Activity 1 - Encapsulation Review

| Class        | Protected state / invariant                                                                                                               | Public operations                                                            |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| Patient      | patient_id and name must be non-empty strings and cannot be changed afterwards (immutable).                                               | Constructor (validates); read access to patient_id and name                  |
| Practitioner | practitioner_id, name and specialty must be non-empty strings; immutable.                                                                 | Constructor (validates); read access to its fields                           |
| Appointment  | Status starts SCHEDULED and can only change SCHEDULED to CANCELLED; patient, practitioner and time must be valid domain objects/datetime. | cancel(); read-only properties (status, patient, practitioner, scheduled_at) |

## Activity 2 - Composition or Inheritance?

Appointment and Patient -> ☑ Composition/association □ Inheritance Reason: An appointment is not a kind of patient (fails the is-a test); it refers to one patient.

Appointment and Practitioner -> ☑ Composition/association □ Inheritance Reason: An appointment is not a kind of practitioner; it refers to one practitioner.

Doctor and Practitioner (hypothetical) -> □ Composition/association ☑ Inheritance Reason: A doctor IS-A practitioner, so inheritance would be valid, but only if doctors need extra behaviour. Today a specialty attribute is enough, so no subclass yet.

Clinic and Appointment -> ☑ Composition/association □ Inheritance Reason: A clinic has appointments (association/aggregation at most). No requirement needs Clinic to own every appointment.

## Activity 3 - Responsibility Allocation

Who decides whether SCHEDULED can become CANCELLED?

**Answer:** The Appointment itself (its cancel() method). The rule is an invariant of the appointment, so it must be enforced where the state lives.

Who validates a patient name?

**Answer:** The Patient class, when it is created. Then no invalid Patient can exist, whichever layer creates one.

Should Appointment execute SQL? Why?

**Answer:** No. SQL is a persistence concern. Putting it in Appointment couples the domain to a database and makes the rules hard to test.

Should the UI decide whether a status transition is legal?

**Answer:** No. The UI can show the error but must not own the rule; otherwise another UI or script could bypass it.

## Activity 4 - AI Code Critique

AI generates an Appointment class with public status mutation, SQL inside cancel(), a NotificationManager dependency and inheritance from PatientRecord. Identify at least five design problems and corrections.

| **Design problem in the AI code**                                              | **Correction**                                                                 |
|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| Public status mutation: anyone can set status to any value                     | Private field with a read-only property; change state only through cancel().   |
| SQL inside cancel(): domain tied to the database                               | Move storage to a repository/persistence layer; cancel() only changes state.   |
| NotificationManager dependency: unsupported requirement and hidden side effect | Remove it; add notification only if a requirement appears, outside the domain. |
| Inheritance from PatientRecord: an appointment is not a patient record         | Use association: Appointment holds a Patient.                                  |
| No validation or illegal-transition check                                      | Validate in the constructor; reject cancelling a non-SCHEDULED appointment.    |
| Tight coupling makes it impossible to unit-test without a database             | Keep the domain free of I/O so it can be tested directly.                      |

## Exit question

Why can code be object-oriented syntactically but still have poor object-oriented design?

**Answer:** Using classes and methods does not make a design object-oriented. Good design also needs meaningful responsibilities, encapsulation, low coupling, correct relationships and enforceable invariants. A class with public fields, SQL and unrelated dependencies is really a procedural data container with scattered rules.
