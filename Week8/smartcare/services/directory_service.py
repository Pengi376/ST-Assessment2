"""Registering and finding patients and practitioners (FR-01, FR-02, FR-03)."""
from __future__ import annotations

from ..domain import Patient, Practitioner
from ..repositories import PatientRepository, PractitionerRepository


class DirectoryService:
    def __init__(self, patients: PatientRepository, practitioners: PractitionerRepository) -> None:
        self._patients = patients
        self._practitioners = practitioners

    def register_patient(self, patient_id: str, name: str) -> Patient:
        patient = Patient(patient_id, name)                          # domain validates
        if self._patients.find_by_id(patient.patient_id) is not None:
            raise ValueError(f"Patient id {patient.patient_id!r} already exists")
        self._patients.save(patient)
        return patient

    def find_patient(self, patient_id: str) -> Patient | None:
        return self._patients.find_by_id(patient_id)

    def register_practitioner(self, practitioner_id: str, name: str, specialty: str) -> Practitioner:
        practitioner = Practitioner(practitioner_id, name, specialty)
        if self._practitioners.find_by_id(practitioner.practitioner_id) is not None:
            raise ValueError(f"Practitioner id {practitioner.practitioner_id!r} already exists")
        self._practitioners.save(practitioner)
        return practitioner
