"""SmartCare v0.1 - human-written prototype (Stage 1, Week 4).

Task 1 used plain variables; the "enhanced" version below uses a list,
dictionaries and functions. Part G adds exactly ONE controlled improvement:
every field must be a non-empty string (this also rejects None).
"""

appointments = []


def _is_blank(value):
    """True for None, non-strings and empty/whitespace-only strings."""
    return not isinstance(value, str) or not value.strip()


def book_appointment(patient_name, practitioner_name, appointment_time):
    # Part G improvement: validate all three required fields.
    if _is_blank(patient_name):
        raise ValueError("Patient name cannot be empty")
    if _is_blank(practitioner_name):
        raise ValueError("Practitioner name cannot be empty")
    if _is_blank(appointment_time):
        raise ValueError("Appointment time cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time,
    }
    appointments.append(appointment)


def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return
    for appointment in appointments:
        print(f"Patient: {appointment['patient']} | "
              f"Practitioner: {appointment['practitioner']} | "
              f"Time: {appointment['time']}")


if __name__ == "__main__":
    print("Welcome to SmartCare: Community Clinic Appointment Booking System!")
    book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
    book_appointment("Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")
    display_appointments()
