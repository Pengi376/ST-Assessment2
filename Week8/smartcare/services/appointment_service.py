"""Workflow coordination for appointments. Depends ONLY on the domain and repository contracts.

Business rules about a single appointment (status transitions) stay in Appointment.
The service owns the cross-object rule: no double-booking a practitioner (FR-06).
"""
from __future__ import annotations
from datetime import datetime

from ..domain import Appointment, AppointmentStatus
from ..repositories import AppointmentRepository, PatientRepository, PractitionerRepository
from .errors import BookingConflictError, NotFoundError


class AppointmentService:
    def __init__(self, appointments: AppointmentRepository, patients: PatientRepository,
                 practitioners: PractitionerRepository) -> None:
        self._appointments = appointments
        self._patients = patients
        self._practitioners = practitioners

    def is_available(self, practitioner_id: str, scheduled_at: datetime) -> bool:          # FR-04
        return self._appointments.find_scheduled_by_practitioner_and_time(practitioner_id, scheduled_at) is None

    def book(self, appointment_id: str, patient_id: str, practitioner_id: str,
             scheduled_at: datetime) -> Appointment:                                        # FR-05, FR-06
        patient = self._patients.find_by_id(patient_id)
        if patient is None:
            raise NotFoundError(f"Patient {patient_id!r} not found")
        practitioner = self._practitioners.find_by_id(practitioner_id)
        if practitioner is None:
            raise NotFoundError(f"Practitioner {practitioner_id!r} not found")
        if self._appointments.find_by_id(appointment_id) is not None:
            raise ValueError(f"Appointment id {appointment_id!r} already exists")
        if not self.is_available(practitioner_id, scheduled_at):
            raise BookingConflictError("Practitioner already has an appointment at that time")
        appointment = Appointment(appointment_id, patient, practitioner, scheduled_at)      # domain validates
        self._appointments.save(appointment)
        return appointment

    def cancel(self, appointment_id: str) -> Appointment:                                   # FR-07, FR-08
        appointment = self._appointments.find_by_id(appointment_id)
        if appointment is None:
            raise NotFoundError(f"Appointment {appointment_id!r} not found")
        appointment.cancel()                      # the DOMAIN decides whether this is legal
        self._appointments.save(appointment)
        return appointment

    def schedule_for_practitioner(self, practitioner_id: str) -> list[Appointment]:         # FR-09
        items = self._appointments.list_by_practitioner(practitioner_id)
        return sorted((a for a in items if a.status is AppointmentStatus.SCHEDULED),
                      key=lambda a: a.scheduled_at)

    def history_for_patient(self, patient_id: str) -> list[Appointment]:                    # FR-10
        return sorted(self._appointments.list_by_patient(patient_id), key=lambda a: a.scheduled_at)
