"""SmartCare v0.2 - requirements prototype (Stage 2, Week 5).

A deliberately small, procedural prototype used to make the acceptance
criteria in the v0.2 Requirements Specification executable.
It is NOT the final design (that comes in Stages 3-5).
"""

patients = {}          # patient_id -> name              (FR-01, FR-02)
appointments = []      # list of dicts, never deleted     (FR-08, FR-10)


def register_patient(patient_id, name):                  # FR-01, FR-11
    if not (isinstance(patient_id, str) and patient_id.strip() and isinstance(name, str) and name.strip()):
        raise ValueError("patient_id and name are required")
    if patient_id in patients:
        raise ValueError("patient_id already exists")
    patients[patient_id] = name


def find_patient(patient_id):                            # FR-02
    return patients.get(patient_id)                      # None when not found


def book(appointment_id, patient_id, practitioner, time):   # FR-05, FR-06, FR-11
    if patient_id not in patients:
        raise ValueError("Unknown patient")
    if not (isinstance(practitioner, str) and practitioner.strip() and isinstance(time, str) and time.strip()):
        raise ValueError("practitioner and time are required")
    for a in appointments:
        if a["practitioner"] == practitioner and a["time"] == time and a["status"] == "SCHEDULED":
            raise ValueError("Practitioner already booked at that time")
    appt = {"id": appointment_id, "patient_id": patient_id, "practitioner": practitioner,
            "time": time, "status": "SCHEDULED"}
    appointments.append(appt)
    return appt


def cancel(appointment_id):                              # FR-07, FR-08
    for a in appointments:
        if a["id"] == appointment_id:
            if a["status"] != "SCHEDULED":
                raise ValueError("Only SCHEDULED appointments can be cancelled")
            a["status"] = "CANCELLED"                    # retained, not deleted
            return a
    raise ValueError("Appointment not found")


def history_for_patient(patient_id):                     # FR-10, FR-12
    return [a for a in appointments if a["patient_id"] == patient_id]


if __name__ == "__main__":
    register_patient("P1", "Alice Smith")
    book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    try:
        book("A2", "P1", "Dr. John Doe", "2026-10-08 10:00")
    except ValueError as err:
        print("Rejected:", err)
    cancel("A1")
    print(history_for_patient("P1"))
