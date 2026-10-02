"""SmartCare v0.4 - domain layer (Stage 4, Week 7).

Implements the approved v0.3 UML. Contains business rules only:
no database, no UI, no notifications, no services.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"


class InvalidStatusTransition(ValueError):
    """Raised when an appointment is asked to make an illegal status change."""


def _required(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} is required")
    return value.strip()


@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str

    def __post_init__(self) -> None:
        # frozen dataclass: use object.__setattr__ to store the cleaned values once
        object.__setattr__(self, "patient_id", _required(self.patient_id, "patient_id"))
        object.__setattr__(self, "name", _required(self.name, "name"))


@dataclass(frozen=True)
class Practitioner:
    practitioner_id: str
    name: str
    specialty: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "practitioner_id", _required(self.practitioner_id, "practitioner_id"))
        object.__setattr__(self, "name", _required(self.name, "name"))
        object.__setattr__(self, "specialty", _required(self.specialty, "specialty"))


class Appointment:
    """Links one Patient and one Practitioner at a time. Owns its status rule."""

    def __init__(self, appointment_id: str, patient: Patient,
                 practitioner: Practitioner, scheduled_at: datetime) -> None:
        self._appointment_id = _required(appointment_id, "appointment_id")
        if not isinstance(patient, Patient):
            raise TypeError("patient must be a Patient")
        if not isinstance(practitioner, Practitioner):
            raise TypeError("practitioner must be a Practitioner")
        if not isinstance(scheduled_at, datetime):
            raise TypeError("scheduled_at must be a datetime")
        self._patient = patient
        self._practitioner = practitioner
        self._scheduled_at = scheduled_at
        self._status = AppointmentStatus.SCHEDULED

    @property
    def appointment_id(self) -> str:
        return self._appointment_id

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        return self._practitioner

    @property
    def scheduled_at(self) -> datetime:
        return self._scheduled_at

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def cancel(self) -> None:
        """SCHEDULED -> CANCELLED only. The object is kept as history."""
        if self._status is not AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransition("Only scheduled appointments can be cancelled")
        self._status = AppointmentStatus.CANCELLED
