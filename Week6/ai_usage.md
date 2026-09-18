# AI Usage Log - Stage 3

## Tools used

| Tool | Purpose | How used |
| --- | --- | --- |
| Claude (Anthropic), claude.ai chat | Reviewing my Stage 3 domain model. |
| AI assistant used for the lab's "AI ON" steps | Part E: AI design review | Given the confirmed requirements and asked to propose classes and relationships with supporting requirement IDs. |

## What the AI contributed

- Proposed an AppointmentStatus enum.
- Proposed Manager, Controller and Notification classes, a Clinic aggregate and a Person superclass.

## What I did with it

**Accepted**

- AppointmentStatus enum (FR-07 and FR-08 define two named states).

**Modified**

- The Clinic aggregate was deferred: collections can be held by repositories later.

**Rejected or left unverified**

- Manager, Controller and Notification classes (no requirement).
- Person superclass (only the name is shared; no useful behaviour).

### Assumptions the AI made

The AI added structure (managers, controllers, a clinic owner) with no requirement behind it. Any suggestion that could not cite a requirement ID was treated as unsupported.

### How the AI output was verified

`python -m pytest -q` in `Week6/` (6 passed); the tests check classes, constructor attributes, operations, enum values and that associations hold objects, not IDs. Details in `evidence.txt`.

### What remained my responsibility

Deciding scope and what counted as correct, checking every suggestion against the client brief or the approved design, running the tests, and being able to explain every line I submit.


---

## Detailed record

### E - AI Design Review

Ask AI to suggest classes and relationships using only confirmed requirements; require supporting requirement IDs.

**What I did:** I gave the AI the confirmed requirements (FR-01 to FR-12) and asked for classes and relationships with supporting requirement IDs. Where it could not cite a requirement ID, I treated the suggestion as unsupported.

### F - Compare and Decide

Record at least one accepted, modified and rejected AI suggestion.

| **AI suggestion**                              | **Decision**        | **Supporting evidence / reason**                                                                   |
|------------------------------------------------|---------------------|----------------------------------------------------------------------------------------------------|
| AppointmentStatus enum                         | Accepted            | FR-07/FR-08 define two named states; an enum makes them explicit.                                  |
| Clinic aggregate owning all objects            | Modified (deferred) | No requirement needs it; collections can be handled by repositories later, so no Clinic class now. |
| Manager, Controller and Notification classes   | Rejected            | No requirement; they add orchestration and unsupported features.                                   |
| Person superclass for Patient and Practitioner | Rejected            | Only the name is shared; inheritance would not add useful behaviour.                               |

### AI Design Review Record

| AI suggestion                                      | Evidence                       | Decision       | Reason                                                          | Model change           |
|----------------------------------------------------|--------------------------------|----------------|-----------------------------------------------------------------|------------------------|
| AppointmentStatus enum                             | FR-07, FR-08: two named states | Accept         | Makes states explicit and prevents invalid values.              | Status becomes an enum |
| Clinic aggregate owning everything                 | No requirement                 | Modify (defer) | Collections can be held by repositories later.                  | No Clinic class        |
| Manager classes (Patient/Practitioner/Appointment) | Weak - no requirement          | Reject         | Add orchestration without a need and weaken the domain objects. | No change              |
| ClinicController                                   | None                           | Reject         | Premature application-layer class.                              | No change              |
| NotificationManager                                | None - no reminder requirement | Reject         | Unsupported feature.                                            | No change              |
| Inheritance between Patient and Appointment        | None                           | Reject         | Not an "is-a" relationship.                                     | Keep association       |
| Person superclass for Patient and Practitioner     | None - only name is shared     | Reject         | Adds hierarchy without shared behaviour.                        | No change              |
