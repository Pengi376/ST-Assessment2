# Stage 1 Tutorial - Why Software Engineering Still Matters

## Activity 1 - Think-Pair-Share (10 minutes)

If ChatGPT or Copilot can produce a 100-line Python application very quickly, what knowledge does a software engineer still need?

1. Requirements analysis and stakeholder communication: deciding WHAT to build and checking it with the client.

2. Design, modelling and architectural judgement: structuring the system so it can be changed and tested.

3. Verification, risk management and accountability: testing, spotting wrong or unsafe AI output, and taking responsibility for it.

## Activity 2 - Is This Software Engineering? (10 minutes)

Scenario A: A student writes a 50-line Python calculator.  
Scenario B: A team develops a payroll system used by 5,000 employees.  
Scenario C: An AI assistant generates a simple appointment application from one prompt.

| Scenario | Programming?    | Software engineering? | Why?                                                                                                                        |
|----------|-----------------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------|
| A        | Yes             | Not really            | One person, one small purpose, no stakeholders or maintenance - it is just coding.                                          |
| B        | Yes             | Yes                   | Many users and stakeholders, requirements, security, testing, teamwork and long-term maintenance are all needed.            |
| C        | Yes (generated) | Only if engineered    | Generating code is programming. Software engineering is deciding requirements and scope, verifying it and owning the risks. |

## Activity 3 - SmartCare Problem Analysis (20 minutes)

Client statement: SmartCare Community Clinic currently uses spreadsheets and paper records to manage patients and appointments. The clinic wants new software to improve these processes.

### Task 1 - Identify stakeholders

| Stakeholder                 | What do they need?                                                               |
|-----------------------------|----------------------------------------------------------------------------------|
| Receptionist / clinic staff | Create and update appointments, find patients quickly, avoid duplicate bookings. |
| Practitioners               | View their schedule and availability and appointment details.                    |
| Patients                    | Accurate appointments and records; cancellations reflected correctly.            |
| Clinic management           | Reliable history, availability visibility and basic operational reports.         |

### Task 2 - Identify current problems

1. Duplicate appointment bookings.

2. Difficulty locating patient records in spreadsheets and paper files.

3. Inconsistent appointment status information (and manual cancellations).

4. Limited visibility of practitioner availability and no reliable appointment history.

### Task 3 - Ask client questions

1. Which patient details must be recorded, and how is a patient identified?

2. How long is an appointment, and what are each practitioner's working hours?

3. What counts as a duplicate booking, and can a cancelled slot be rebooked?

4. Who is allowed to book, change and cancel appointments?

5. Which reports does management need first, and how is privacy protected?

## Activity 4 - Critique an AI Response (15 minutes)

An AI assistant suggests: appointment management; facial-recognition login; AI diagnosis recommendations; patient search; online payment; practitioner schedule view; insurance processing; automatic treatment-plan generation.

| Suggestion                   | Client evidence?                                               | In scope? | Decision                                          |
|------------------------------|----------------------------------------------------------------|-----------|---------------------------------------------------|
| Appointment management       | Yes - brief says manage appointments; duplicates are a problem | Yes       | Accept                                            |
| Facial recognition login     | No                                                             | No        | Reject - no evidence; adds biometric/privacy risk |
| AI diagnosis recommendations | No                                                             | No        | Reject - unsupported, high clinical risk          |
| Patient search               | Yes - difficulty locating patient records                      | Yes       | Accept                                            |
| Online payment               | No                                                             | No        | Reject / defer - no payment requirement           |
| Practitioner schedule view   | Yes - limited visibility of availability                       | Yes       | Accept                                            |
| Insurance processing         | No                                                             | No        | Reject - outside small first version              |
| Treatment-plan generation    | No                                                             | No        | Reject - clinical risk, not requested             |

## Exit question

Write one activity that a software engineer must perform and that cannot safely be delegated entirely to AI.

**Answer:** Verifying the software against the client's real requirements (for example, testing that duplicate bookings are rejected) and taking accountability for the result. AI can draft code but cannot own the decision that the system is correct and safe.
