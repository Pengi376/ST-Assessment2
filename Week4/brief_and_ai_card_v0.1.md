# SmartCare v0.1 - Initial Engineering Brief and AI Activity Card

## SmartCare scenario

SmartCare Community Clinic currently uses spreadsheets and paper records to manage patients and appointments. The client says: 'We need software to help manage patients, practitioners and appointments.'

## Initial Engineering Brief

### 1. Problem summary

SmartCare is a small community clinic that books consultations with GPs using spreadsheets, paper records and manual processes. Staff report duplicate bookings, difficulty finding patient records, inconsistent appointment status, little visibility of practitioner availability, manual cancellations, no reliable appointment history and difficulty producing basic reports. Management wants a simple, maintainable system that first supports patient, practitioner and appointment management - not a complex hospital system. The client statement is not yet a specification: mandatory data, rules for conflicts and cancellation, access control and reporting needs still have to be confirmed before design starts.

### 2. Initial stakeholders

| Stakeholder              | Possible need                                                                           |
|--------------------------|-----------------------------------------------------------------------------------------|
| Reception / clinic staff | Create, search and cancel appointments; avoid duplicates; find patient records quickly. |
| Practitioners (GPs)      | See their schedule and availability and accurate appointment details.                   |
| Patients                 | Accurate appointment records; cancellations reflected consistently.                     |
| Clinic management        | Reliable appointment history and basic operational reports.                             |

### 3. Initial features

| Feature                                              | Confirmed or provisional? | Why?                                                                                 |
|------------------------------------------------------|---------------------------|--------------------------------------------------------------------------------------|
| Patient records and search                           | Confirmed                 | Brief reports difficulty locating patient records.                                   |
| Appointment booking with duplicate/conflict checking | Confirmed                 | Duplicate bookings are an explicit problem; management wants appointment management. |
| Cancellation with retained history                   | Confirmed                 | Manual cancellation and lack of reliable history are explicit problems.              |
| Practitioner schedule / availability view            | Confirmed                 | Limited visibility of availability is an explicit problem; details still unclear.    |
| Basic operational reports                            | Provisional               | Management wants reports but the content of the reports is not specified.            |

### 4. Questions for the client

1. Which patient details are mandatory, and how is a patient uniquely identified?

2. How is practitioner availability defined (working hours, appointment length, leave)?

3. What counts as a duplicate or conflicting appointment, and should a cancelled slot be rebookable?

4. Who may create, change and cancel appointments, and is a login required?

5. Which reports does management need in the first version?

### 5. What we do not yet know

1. Privacy, authentication and role requirements for patient data.

2. How long records must be kept and whether existing spreadsheet data must be imported.

3. Whether reminders, payments or integration with other systems are wanted (nothing in the brief says so).

## AI Activity Card - Ask, Check, Explain

### Before AI

What do I think the code does? What problems can I already identify?

**My answer:** I expect the prototype to store each appointment (patient, practitioner, time) in a list and print them. Problems I can already see: no duplicate/conflict check, no identifiers, blank or None values, free-text time, and nothing is saved when the program ends.

### AI request

Act as a tutor. Explain this code and identify potential problems. Do not provide a complete replacement. Ask me questions that help me reason about the solution.

*Used with my Stage 1 prototype (smartcare_v01.py) in an approved GenAI tool; see ai_usage.md.*

### Evaluate

| Suggestion                              | Useful | Unclear | Incorrect | Out of scope |
|-----------------------------------------|--------|---------|-----------|--------------|
| Validate patient, practitioner and time | ✓      |         |           |              |
| Add duplicate/conflict checking         | ✓      |         |           |              |
| Add patient search                      | ✓      |         |           |              |
| Use a database for storage              |        | ✓       |           |              |
| Add facial-recognition login            |        |         |           | ✓            |
| Add AI diagnosis recommendations        |        |         | ✓         | ✓            |

### Decide

For each significant suggestion: Accept / Modify / Reject / Keep unverified.

**Validate all fields:** ACCEPT - implemented as the single Part G improvement.

**Conflict checking:** KEEP for later - directly addresses the duplicate-booking problem; becomes FR-06 in Stage 2.

**Patient search:** KEEP for later - addresses the record-location problem (FR-02).

**Database:** KEEP UNVERIFIED - may be needed, but no storage requirement has been confirmed yet.

**Facial recognition / AI diagnosis:** REJECT - no client evidence, privacy and clinical risk.

### Verify

- Run the code: Done: both versions run; output matches expectations.

- Test normal input: Done: valid appointments stored and displayed.

- Test unusual input: Done: blank, whitespace and None are rejected; duplicates are accepted (known gap).

- Compare with requirements: Done: each accepted idea traced to the client brief.

- Ask tutor/peer: To do in class: confirm the open client questions.

- Check documentation: Done: Python docs for list, dict, isinstance and ValueError.

### Explain

Can I explain the final code without reading the AI response? What do I still need to understand?

**My answer:** Yes. I can explain the list of dictionaries, the validation helper and why each rule exists without reading the AI response. I still need to understand access control, data retention and the exact conflict policy.
