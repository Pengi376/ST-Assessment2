# Stage 3 Tutorial - From Requirements to Domain Model

## Candidate Concepts

| Candidate    | Class?     | Reason                                                                                                              |
|--------------|------------|---------------------------------------------------------------------------------------------------------------------|
| Patient      | Yes        | Real-world thing with identity, data and relationships (FR-01, FR-02).                                              |
| Practitioner | Yes        | Real-world thing with identity, data and relationships (FR-03).                                                     |
| Appointment  | Yes        | Core concept linking patient, practitioner and time; has status and behaviour (FR-05 to FR-08).                     |
| Name         | No         | A simple attribute (value) of Patient or Practitioner, with no behaviour of its own.                                |
| Clinic       | Not yet    | No requirement needs an object that owns everything; avoid a "god" class. Reconsider only if a requirement appears. |
| Database     | No         | A technical/storage concern, not part of the problem domain; belongs in persistence (Stage 5).                      |
| Cancellation | No         | An action on Appointment (cancel()), not a thing; the result is recorded as status CANCELLED.                       |
| Status       | Yes (enum) | A fixed set of named states, SCHEDULED and CANCELLED; modelled as AppointmentStatus, not a full entity class.       |

## CRC Cards

### Patient

| Responsibilities                                                   | Collaborators                                     |
|--------------------------------------------------------------------|---------------------------------------------------|
| Hold the patient's ID and name (required fields)                   | Appointment (is referred to by many appointments) |
| Provide a stable identity (patient_id) that search and history use | None                                              |

### Practitioner

| Responsibilities                                                           | Collaborators                                     |
|----------------------------------------------------------------------------|---------------------------------------------------|
| Hold the practitioner's ID, name and specialty                             | Appointment (is referred to by many appointments) |
| Provide a stable identity (practitioner_id) for booking and schedule views | None                                              |

### Appointment

| Responsibilities                                                          | Collaborators         |
|---------------------------------------------------------------------------|-----------------------|
| Hold patient, practitioner, scheduled time and status                     | Patient, Practitioner |
| Cancel itself: SCHEDULED to CANCELLED only, and stay on record as history | AppointmentStatus     |

## Relationship Reasoning

Patient to Appointment: which relationship and why?

**Answer:** Association, one-to-many: one patient can have many appointments, and each appointment has exactly one patient (1 to 0..\*). A patient is not part of an appointment and an appointment does not own a patient, so it is not composition.

Practitioner to Appointment: what multiplicity?

**Answer:** One practitioner to zero or many appointments (1 to 0..\*); each appointment has exactly one practitioner. A practitioner can have many appointments over time but only one SCHEDULED at any given time (the FR-06 rule).

Should Appointment inherit from Patient?

**Answer:** No. An appointment is not a kind of patient (fails the "is-a" test). It refers to a patient, so use association. Inheritance would wrongly give appointments patient data and behaviour.

Does Clinic need to own every object?

**Answer:** No. Nothing in FR-01 to FR-12 needs it. A Clinic owner would become a god class; later, repositories can hold the collections.

## AI Model Critique

Critique AI proposals: PatientManager, PractitionerManager, AppointmentManager, ClinicController, NotificationManager, ScheduleEngine.

| **AI proposal**                                           | **Decision**   | **Reason**                                                                                                                                                 |
|-----------------------------------------------------------|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PatientManager / PractitionerManager / AppointmentManager | Reject         | Add orchestration with no requirement; they pull behaviour away from the domain objects ("manager" smell). Workflow can be a single focused service later. |
| ClinicController                                          | Reject (defer) | A controller is an application-layer concern, premature in a domain model.                                                                                 |
| NotificationManager                                       | Reject         | No reminder or notification requirement in the brief.                                                                                                      |
| ScheduleEngine                                            | Reject         | No scheduling-algorithm requirement; availability is derived from existing appointments (FR-04).                                                           |
