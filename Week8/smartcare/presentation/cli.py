"""Console UI. Reads input, calls services, formats output. Contains NO business rules."""
from __future__ import annotations
from datetime import datetime
from typing import Callable

from ..domain import Appointment
from ..services import AppointmentService, DirectoryService

TIME_FORMAT = "%Y-%m-%d %H:%M"
MENU = """
SmartCare - Community Clinic Appointment Booking
 1) Register patient          5) Cancel appointment
 2) Find patient              6) Practitioner schedule
 3) Register practitioner     7) Patient appointment history
 4) Book appointment          0) Exit"""


def format_appointment(a: Appointment) -> str:
    return (f"{a.appointment_id} | {a.scheduled_at.strftime(TIME_FORMAT)} | {a.patient.name} "
            f"with {a.practitioner.name} | {a.status.value}")


def run(directory: DirectoryService, appointments: AppointmentService,
        read: Callable[[str], str] = input, write: Callable[[str], None] = print) -> None:
    def ask(prompt: str) -> str:
        return read(prompt + ": ").strip()

    while True:
        write(MENU)
        choice = ask("Choose")
        try:
            if choice == "0":
                write("Goodbye.")
                return
            elif choice == "1":
                p = directory.register_patient(ask("Patient ID"), ask("Name"))
                write(f"Registered patient {p.patient_id}: {p.name}")
            elif choice == "2":
                p = directory.find_patient(ask("Patient ID"))
                write(f"Found: {p.patient_id} - {p.name}" if p else "No patient found with that ID.")
            elif choice == "3":
                p = directory.register_practitioner(ask("Practitioner ID"), ask("Name"), ask("Specialty"))
                write(f"Registered practitioner {p.practitioner_id}: {p.name} ({p.specialty})")
            elif choice == "4":
                when = datetime.strptime(ask(f"Date/time ({TIME_FORMAT})"), TIME_FORMAT)
                a = appointments.book(ask("Appointment ID"), ask("Patient ID"), ask("Practitioner ID"), when)
                write("Booked: " + format_appointment(a))
            elif choice == "5":
                write("Cancelled: " + format_appointment(appointments.cancel(ask("Appointment ID"))))
            elif choice == "6":
                items = appointments.schedule_for_practitioner(ask("Practitioner ID"))
                write("\n".join(format_appointment(a) for a in items) or "No scheduled appointments.")
            elif choice == "7":
                items = appointments.history_for_patient(ask("Patient ID"))
                write("\n".join(format_appointment(a) for a in items) or "No appointments on record.")
            else:
                write("Please choose a number from the menu.")
        except (ValueError, LookupError, TypeError) as err:      # domain/service errors -> friendly message
            write(f"Error: {err}")
