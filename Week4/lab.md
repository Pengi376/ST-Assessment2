# Stage 1 Lab

## Part A - Understand the Problem: AI OFF

SmartCare needs a small prototype that allows a receptionist to record patient appointments. Each appointment records patient name, practitioner name and appointment time.

What data must be stored?

**Answer:** Patient name, practitioner name and appointment time for each appointment (later: unique patient/practitioner IDs and an appointment status).

What functions might be useful?

**Answer:** book_appointment(), display_appointments(); later search by patient, cancel an appointment and a conflict check.

What could go wrong?

**Answer:** Blank or None values, an unclear time format, duplicate bookings for the same practitioner and time, two patients with the same name, and all data being lost when the program ends.

What requirements are unclear?

**Answer:** Which fields are mandatory, the time format and appointment length, the conflict policy, who may book or cancel, and how long records must be kept.

## Part B - Build a Human-Written Prototype: AI OFF

The two programs from the handout (Task 1 with plain variables, then the enhanced version using a list, dictionaries and functions) were typed in and run. The final code, including the Part G improvement, is in [`smartcare_v01.py`](smartcare_v01.py).

^ Now, run both programs , and identify at least five limitations.

**Result:** both programs were run with Python 3.

Task 1 output:

```text
Welcome to SmartCare: Community Clinic Appointment Booking System!
Patient: Alice Smith | Practitioner: Dr. John Doe | Time: 2024-07-20 10:00 AM
Patient: Bob Johnson | Practitioner: Dr. Jane Roe | Time: 2024-07-20 11:30 AM
```

Enhanced program output:

```text
Welcome to SmartCare: The Clinical Appointment Booking System!
Patient: Alice Smith | Practitioner: Dr. John Doe | Time: 2024-07-20 10:00 AM
Patient: Bob Johnson | Practitioner: Dr. Jane Roe | Time: 2024-07-20 11:30 AM
```

**Five limitations identified:**

1.  No persistent storage: everything is lost when the program ends.

2.  No patient or practitioner identifiers, so people with the same name cannot be told apart.

3.  No date/time validation: the time is free text.

4.  No duplicate/conflict detection: the same practitioner can be booked twice at the same time.

5.  No cancellation, search or appointment history.

6.  Only the patient name is validated; practitioner name and time can be blank or None (fixed in Part G).

## Part C - Use AI as Tutor: AI ON (Use only UC approved GenAI Tool such as Microsoft CoPilot)

**Suggested prompt structure:**  
Act as a Python tutor.  
I am learning introductory software technology.  
Here is a small appointment-booking function.  
1. Explain what the code does.  
2. Identify three limitations.  
3. Suggest improvements.  
4. Do not rewrite the whole application.  
5. Ask me two questions to test my understanding.

**What I did:** I gave the AI tutor my enhanced program using the prompt structure above (explain, three limitations, improvements, no full rewrite, two questions for me). In summary it:

- Explained that the program stores each appointment as a dictionary in a list and prints them with a loop.

- Identified limitations: no validation of practitioner/time, no duplicate-booking check, no persistence.

- Suggested improvements: validate every field, consider IDs, and add a conflict check later.

- Asked me two questions, which I answered myself: (1) What happens if two people book the same practitioner at the same time? - Both are stored, because nothing compares them. (2) Why raise ValueError instead of ignoring a blank name? - Silent failure would hide bad data; an error makes the problem visible.

## Part D - Generate an Alternative: AI ON

Ask AI to create a simple beginner-friendly Python function that stores patient name, practitioner name and appointment time. Explicitly prohibit a database or GUI.

**Result:** The constrained prompt (no database, no GUI) produced a short function that stores the three values in a dictionary and appends it to a list passed in as a parameter. The full code and comparison are in comparison.md:

```
def add_appointment(appointments, patient_name, practitioner_name, appointment_time):
    appointment = {"patient": patient_name.strip(),
                   "practitioner": practitioner_name.strip(),
                   "time": appointment_time}
    appointments.append(appointment)
    return appointment
```

## Part E - Compare Human and AI Versions

| Question                     | Human version                                                                           | AI version                                                                       |
|------------------------------|-----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| Easy to understand?          | Yes. Two short functions and a global list.                                             | Yes, with a docstring; passing the list as a parameter is one extra idea.        |
| Runs successfully?           | Yes (after fixing indentation copied from the handout).                                 | Yes for normal strings; crashes with AttributeError on None because of .strip(). |
| Uses only required features? | Yes: lists, dictionaries and functions only.                                            | Mostly; adds .strip(), a return value and a time-format assumption.              |
| Adds assumptions?            | Few: time is free text; practitioner is just a name.                                    | More: assumes a time format and that names are always strings.                   |
| Handles errors?              | Yes after Part G: blank, whitespace and None raise ValueError. Duplicates not detected. | No validation: blank names are stored and None crashes.                          |
| Could I explain it?          | Yes, every line.                                                                        | Yes after careful reading, but I would have to justify its assumptions.          |

## Part F - Verify Behaviour

- Normal appointment

- Blank patient name

- Two appointments for the same practitioner/time

- Strange input such as patient_name=None or appointment_time=None

| **Test**                 | **Input**                                            | **Result**                                                                                                       | **Meaning**                                |
|--------------------------|------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| Normal appointment       | 'Alice Smith', 'Dr. John Doe', '2024-07-20 10:00 AM' | Stored and displayed                                                                                             | Works as intended                          |
| Blank patient name       | '' (and ' ')                                         | ValueError: Patient name cannot be empty                                                                         | Original check works                       |
| Same practitioner + time | Two bookings for Dr. John Doe at 10:00               | Both accepted (len = 2)                                                                                          | Missing conflict rule - future requirement |
| patient_name=None        | None                                                 | Original: ValueError (None is falsy, so the original check caught it). After Part G: ValueError (explicit check) | Already safe; now explicit                 |
| appointment_time=None    | None                                                 | Original: stored silently (no check). After Part G: ValueError                                                   | Real gap, fixed by the one improvement     |
| practitioner_name=None   | None                                                 | Original: stored silently. After Part G: ValueError                                                              | Real gap, fixed by the one improvement     |

## Part G - Improve One Thing

Choose exactly one controlled improvement, for example: if not patient_name: raise ValueError("Patient name cannot be empty")

**Improvement chosen:** All three required fields (patient name, practitioner name, appointment time) must be non-empty strings; this also rejects None. It improves data integrity without changing the design.

```
def _is_blank(value):
    return not isinstance(value, str) or not value.strip()

# inside book_appointment():
if _is_blank(patient_name):
    raise ValueError("Patient name cannot be empty")
if _is_blank(practitioner_name):
    raise ValueError("Practitioner name cannot be empty")
if _is_blank(appointment_time):
    raise ValueError("Appointment time cannot be empty")
```

Verified by test_smartcare_v01.py (7 tests pass, see evidence.txt). Conflict detection was deliberately NOT added: exactly one improvement was requested.

## Part H - Reflection (150-250 words)

What did you build before using AI?

What did AI help you understand?

Did AI make assumptions?

How did you verify the AI output?

What engineering work remained for you?

Before using AI, I built a small appointment prototype with variables, then a list of dictionaries and functions (book_appointment, display_appointments). AI helped me understand why this design is easy to extend but incomplete: it pointed out missing validation, duplicate bookings and unusual inputs such as None. AI also made assumptions. Some suggestions went beyond the client evidence, such as databases, authentication and extra clinic services, so I treated those as assumptions rather than requirements. I verified the AI's ideas by running normal and unusual inputs (see test_smartcare_v01.py) and comparing the results with the client brief. The most important finding was that a program can run successfully and still break an important business rule: two bookings for the same practitioner and time are still accepted. The engineering work that remained mine was deciding scope, identifying missing requirements, choosing exactly one controlled improvement (validating all three fields as non-empty strings), testing behaviour and documenting limitations. AI acted as a tutor and review aid, not the owner of the design.

## Submission checklist [GitHub Commit]

- ☑ Python file runs.

- ☑ Comparison table completed.

- ☑ Normal and unusual inputs tested.

- ☑ AI assistance documented.

- ☑ Reflection completed.

- ☑ I can explain my code.

## Evidence (captured output)

Run from the `Week4/` folder. The full log is in [`evidence.txt`](evidence.txt).

```text

$ python smartcare_v01.py
Welcome to SmartCare: Community Clinic Appointment Booking System!
Patient: Alice Smith | Practitioner: Dr. John Doe | Time: 2024-07-20 10:00 AM
Patient: Bob Johnson | Practitioner: Dr. Jane Roe | Time: 2024-07-20 11:30 AM

$ python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0 -- /usr/bin/python
cachedir: .pytest_cache
rootdir: /home/claude/repo/Week4/stage01
collecting ... collected 7 items

test_smartcare_v01.py::test_normal_appointment_is_stored PASSED          [ 14%]
test_smartcare_v01.py::test_blank_or_none_patient_rejected[] PASSED      [ 28%]
test_smartcare_v01.py::test_blank_or_none_patient_rejected[   ] PASSED   [ 42%]
test_smartcare_v01.py::test_blank_or_none_patient_rejected[None] PASSED  [ 57%]
test_smartcare_v01.py::test_none_appointment_time_rejected PASSED        [ 71%]
test_smartcare_v01.py::test_none_practitioner_rejected PASSED            [ 85%]
test_smartcare_v01.py::test_same_practitioner_and_time_is_STILL_accepted_known_limitation PASSED [100%]

============================== 7 passed in 0.01s ===============================
```
