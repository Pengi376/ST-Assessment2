"""In-memory implementations of the repository contracts (used by tests and as a default)."""
from __future__ import annotations
from datetime import datetime

from ..domain import Appointment, AppointmentStatus, Patient, Practitioner


class InMemoryPatientRepository:
    def __init__(self) -> None:
        self._items: dict[str, Patient] = {}

    def save(self, patient: Patient) -> None:
        self._items[patient.patient_id] = patient

    def find_by_id(self, patient_id: str) -> Patient | None:
        return self._items.get(patient_id)


class InMemoryPractitionerRepository:
    def __init__(self) -> None:
        self._items: dict[str, Practitioner] = {}

    def save(self, practitioner: Practitioner) -> None:
        self._items[practitioner.practitioner_id] = practitioner

    def find_by_id(self, practitioner_id: str) -> Practitioner | None:
        return self._items.get(practitioner_id)


class InMemoryAppointmentRepository:
    def __init__(self) -> None:
        self._items: dict[str, Appointment] = {}

    def save(self, appointment: Appointment) -> None:
        self._items[appointment.appointment_id] = appointment

    def find_by_id(self, appointment_id: str) -> Appointment | None:
        return self._items.get(appointment_id)

    def find_scheduled_by_practitioner_and_time(self, practitioner_id: str,
                                                scheduled_at: datetime) -> Appointment | None:
        return next((a for a in self._items.values()
                     if a.practitioner.practitioner_id == practitioner_id
                     and a.scheduled_at == scheduled_at
                     and a.status is AppointmentStatus.SCHEDULED), None)

    def list_by_practitioner(self, practitioner_id: str) -> list[Appointment]:
        return [a for a in self._items.values() if a.practitioner.practitioner_id == practitioner_id]

    def list_by_patient(self, patient_id: str) -> list[Appointment]:
        return [a for a in self._items.values() if a.patient.patient_id == patient_id]
