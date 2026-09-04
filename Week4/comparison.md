# Stage 1 - Human vs AI comparison (Part E)

## The two versions

**Human version** - `smartcare_v01.py` in this folder (list of dictionaries, `book_appointment()`, `display_appointments()`, plus the Part G validation).

**AI version** - produced from the Part D prompt: *"Create a simple beginner-friendly Python function that stores patient name, practitioner name and appointment time. Do not use a database or a GUI."*

```python
def add_appointment(appointments, patient_name, practitioner_name, appointment_time):
    """Store one appointment in the given list and return it.

    appointment_time is expected as text such as '2024-07-20 10:00'.
    """
    appointment = {
        "patient": patient_name.strip(),
        "practitioner": practitioner_name.strip(),
        "time": appointment_time,
    }
    appointments.append(appointment)
    return appointment
```

## Comparison table

| Question | Human version | AI version |
| --- | --- | --- |
| Easy to understand? | Yes. Two short functions and a global list; a beginner can follow it. | Yes, and the docstring helps, but passing the list in as a parameter is an extra idea to explain. |
| Runs successfully? | Yes. Runs and prints both appointments (after fixing the indentation copied from the handout). | Yes for normal strings. Crashes with `AttributeError` if a name is `None` because `.strip()` is called on it. |
| Uses only required features? | Yes: lists, dictionaries and functions only. | Mostly. It adds `.strip()`, a return value and a time-format assumption that nobody asked for. |
| Adds assumptions? | Few: the time is free text and the practitioner is just a name. | More: assumes `YYYY-MM-DD HH:MM` format, assumes names are always strings, assumes the caller owns the list. |
| Handles errors? | Yes, after Part G: blank, whitespace-only and `None` values raise `ValueError`. Duplicate bookings are not detected. | No validation at all; blank names are stored and `None` causes a crash. |
| Could I explain it? | Yes, every line. | Yes after reading it carefully, but I would have to justify the assumptions it makes. |

## Five limitations of the human prototype (Part B)

1. Data is lost when the program ends (no persistence).
2. No patient or practitioner identifiers, so two people with the same name cannot be told apart.
3. No date/time validation; the time is free text.
4. Duplicate / conflicting bookings for the same practitioner and time are accepted.
5. No cancellation, search or appointment history.

(Also: no authentication or role control, and `appointments` is a global variable.)

## Conclusion

The AI version looks tidier but is *less* safe: its "helpful" `.strip()` creates a crash on `None`, and its format assumption is not backed by the client brief. Neither version is complete; the human version, with one controlled improvement, is the better base for Stage 2.
