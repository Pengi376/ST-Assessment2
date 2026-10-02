# Stage 5 Tutorial - Layered Architecture and Refactoring

## Activity 1 - Where Does This Belong?

| Responsibility                      | Layer        | Reason                                                             |
|-------------------------------------|--------------|--------------------------------------------------------------------|
| Read menu input                     | Presentation | Talking to the user is a user-interface concern.                   |
| Check appointment status transition | Domain       | A business rule (invariant) owned by Appointment.                  |
| Coordinate booking use case         | Service      | Workflow: find patient/practitioner, check conflict, create, save. |
| Execute SQLite INSERT               | Persistence  | A storage detail; only this layer should know SQL.                 |
| Format confirmation message         | Presentation | Output formatting is a UI concern.                                 |
| Find appointment by ID              | Repository   | Data-access contract used by services; implemented in Persistence. |

## Activity 2 - Architecture Smell Hunt

A SmartCare file contains input(), SQL, appointment conflict rules, printing and validation. Identify at least five architecture problems and propose a layer for each responsibility.

| **Architecture problem**                                                             | **Proposed layer**                                                          |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| input() mixed with business logic - cannot test rules without a keyboard             | Presentation (input/output only)                                            |
| SQL mixed with workflow - business code depends on the database                      | Persistence behind a repository contract                                    |
| Appointment conflict rules written in the script/UI - bypassable and duplicated      | Service (rule across appointments); Domain (single-appointment status rule) |
| print() mixed with processing - output formatting tangled with logic                 | Presentation                                                                |
| Validation duplicated in input code - invalid objects can still be created elsewhere | Domain (validate once when the object is created)                           |
| Everything in one file - low cohesion, hard to change or reuse                       | Split into presentation, service, domain, repository, persistence           |

## Activity 3 - SOLID Without Overengineering

ClinicManager handles every use case. Which principle is threatened?

**Answer:** Single Responsibility Principle (low cohesion): one class has many reasons to change.

AppointmentService imports sqlite3 directly. What dependency concern exists?

**Answer:** Dependency Inversion: the high-level workflow depends on a low-level detail. It becomes hard to test and to change the storage; it should depend on a repository abstraction instead.

A repository interface has 20 methods but a client needs two. What concern exists?

**Answer:** Interface Segregation: clients are forced to depend on methods they do not use. Use small interfaces shaped by the use case.

Should every class have an interface? Explain.

**Answer:** No. Add an abstraction only where it decouples something stable from something likely to change (such as storage) or makes testing possible. Otherwise it is needless complexity.

## Activity 4 - AI Architecture Critique

AI proposes microservices, an event bus, six interfaces and a dependency-injection framework. Decide what to reject, defer or keep using current requirements.

| **AI proposal**                | **Decision**               | **Reason (current requirements)**                                      |
|--------------------------------|----------------------------|------------------------------------------------------------------------|
| Microservices                  | Reject                     | A small single-clinic application has no distributed-system need.      |
| Event bus                      | Reject                     | No asynchronous or multi-subscriber requirement.                       |
| Six interfaces                 | Reject (keep what is used) | Keep only small repository contracts that the services actually use.   |
| Dependency-injection framework | Defer                      | Constructor injection in the composition root is enough at this scale. |
