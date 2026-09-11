# Stage 2 Tutorial - From Problems to Requirements

## Activity 1 - Stakeholder Map

| Stakeholder               | Need                                       | Potential conflict                                                      |
|---------------------------|--------------------------------------------|-------------------------------------------------------------------------|
| Reception staff           | Fast, accurate booking and patient search  | Practitioner availability limits what can be booked.                    |
| Practitioners             | Accurate, up-to-date schedules             | Want visibility of their day without exposing unnecessary patient data. |
| Patients                  | Correct appointments and a reliable record | Their privacy may conflict with wide staff access.                      |
| Clinic management         | Reliable history and basic reports         | May want reports that go beyond a small first version.                  |
| System owner / IT support | Simple, maintainable, testable software    | Keeping it simple conflicts with feature requests.                      |

## Activity 2 - Functional or Non-Functional?

☑ Functional □ Non-functional The system shall allow staff to cancel an appointment.

□ Functional ☑ Non-functional The system should remain responsive for the course-scale dataset.

☑ Functional □ Non-functional The system shall retain cancelled appointments.

□ Functional ☑ Non-functional Core business logic should be independently testable.

☑ Functional □ Non-functional The system shall search for a patient by ID.

## Activity 3 - Repair Ambiguous Requirements

The system should be easy to use.

Problem: "Easy to use" is subjective and cannot be tested.  
Clarification question: Who are the users, and what task should a new receptionist be able to complete, in what time, with what training?

Patient search should be fast.

Problem: "Fast" has no measurable threshold or dataset size.  
Clarification question: What response time is acceptable, for how many patient records?

The system should securely manage data.

Problem: "Securely" covers many different things and is not testable.  
Clarification question: Which roles may see or change which data, and what privacy rules and retention apply?

Appointments should normally be easy to cancel.

Problem: "Normally" hides the exceptions.  
Clarification question: Who may cancel, in how many steps, and are there exceptions (for example a cancellation very close to the appointment time)?

## Activity 4 - AI Requirements Audit

Classify each suggestion: Confirmed / Assumption requiring validation / Unsupported / Out of scope.

| AI suggestion                             | Classification                             | Evidence / reason                                               |
|-------------------------------------------|--------------------------------------------|-----------------------------------------------------------------|
| Patients receive SMS reminders.           | Assumption requiring validation            | Not in the brief; plausible, but nobody has asked for it.       |
| Facial recognition login.                 | Unsupported / out of scope                 | No evidence; adds biometric privacy risk and complexity.        |
| Receptionists create appointments.        | Confirmed                                  | Staff manage bookings today and report duplicate bookings.      |
| Online payment.                           | Out of scope                               | No payment requirement; not a small first-version need.         |
| Practitioners view schedules.             | Confirmed (need) - viewer is an assumption | Brief reports limited visibility of availability.               |
| AI recommends treatments.                 | Unsupported / out of scope                 | Clinical decision support is high risk and not requested.       |
| Cancelled appointments remain in history. | Confirmed                                  | Brief reports manual cancellation and lack of reliable history. |

## Exit question

Why is 'AI suggested it' not sufficient evidence for a requirement?

**Answer:** An AI suggestion is only a possibility. A requirement needs evidence of a real stakeholder need (the client brief, stakeholder confirmation, policy or law) so that it can be traced, justified, tested and, if necessary, rejected. AI can invent plausible but unwanted features.
