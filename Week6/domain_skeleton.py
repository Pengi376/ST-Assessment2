"""SmartCare v0.3 - Python class SKELETONS matching the approved UML (Stage 3, Week 6).

Skeletons only: attributes and operation signatures exist, but behaviour
(validation, status rules) is intentionally NOT implemented yet - that is Stage 4.
"""
from __future__ import annotations
from datetime import datetime
from enum import Enum


class AppointmentStatus(Enum):
    SCHEDULED = "SCHEDULED"
    CANCELLED = "CANCELLED"


class Patient:
    def __init__(self, patient_id: str, name: str) -> None:
        self.patient_id = patient_id
        self.name = name


class Practitioner:
    def __init__(self, practitioner_id: str, name: str, specialty: str) -> None:
        self.practitioner_id = practitioner_id
        self.name = name
        self.specialty = specialty


class Appointment:
    def __init__(self, appointment_id: str, patient: Patient,
                 practitioner: Practitioner, scheduled_at: datetime) -> None:
        self.appointment_id = appointment_id
        self.patient = patient                    # UML: Patient 1 --- 0..* Appointment
        self.practitioner = practitioner          # UML: Practitioner 1 --- 0..* Appointment
        self.scheduled_at = scheduled_at
        self.status = AppointmentStatus.SCHEDULED

    def cancel(self) -> None:
        raise NotImplementedError("Implemented in Stage 4 (Week 7)")
