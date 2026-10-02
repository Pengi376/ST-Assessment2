"""SQLite implementations of the repository contracts (standard library only).

This is the ONLY place in the system that knows about sqlite3 and SQL.
Domain objects are rebuilt through their public API (an appointment that was
CANCELLED is re-created and then cancel()ed), so the domain needed no change.
"""
from __future__ import annotations
import sqlite3
from datetime import datetime

from ..domain import Appointment, AppointmentStatus, Patient, Practitioner

SCHEMA = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS practitioners (
    practitioner_id TEXT PRIMARY KEY, name TEXT NOT NULL, specialty TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL REFERENCES patients(patient_id),
    practitioner_id TEXT NOT NULL REFERENCES practitioners(practitioner_id),
    scheduled_at TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('SCHEDULED','CANCELLED')));
"""


def connect(path: str = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


class SqlitePatientRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._c = conn

    def save(self, patient: Patient) -> None:
        self._c.execute("INSERT OR REPLACE INTO patients VALUES (?, ?)", (patient.patient_id, patient.name))
        self._c.commit()

    def find_by_id(self, patient_id: str) -> Patient | None:
        row = self._c.execute("SELECT patient_id, name FROM patients WHERE patient_id = ?", (patient_id,)).fetchone()
        return Patient(*row) if row else None


class SqlitePractitionerRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self._c = conn

    def save(self, practitioner: Practitioner) -> None:
        self._c.execute("INSERT OR REPLACE INTO practitioners VALUES (?, ?, ?)",
                        (practitioner.practitioner_id, practitioner.name, practitioner.specialty))
        self._c.commit()

    def find_by_id(self, practitioner_id: str) -> Practitioner | None:
        row = self._c.execute("SELECT practitioner_id, name, specialty FROM practitioners "
                              "WHERE practitioner_id = ?", (practitioner_id,)).fetchone()
        return Practitioner(*row) if row else None


class SqliteAppointmentRepository:
    _COLS = "appointment_id, patient_id, practitioner_id, scheduled_at, status"

    def __init__(self, conn: sqlite3.Connection, patients: SqlitePatientRepository,
                 practitioners: SqlitePractitionerRepository) -> None:
        self._c, self._patients, self._practitioners = conn, patients, practitioners

    def _rebuild(self, row) -> Appointment:
        appt_id, patient_id, practitioner_id, when, status = row
        appt = Appointment(appt_id, self._patients.find_by_id(patient_id),
                           self._practitioners.find_by_id(practitioner_id), datetime.fromisoformat(when))
        if status == AppointmentStatus.CANCELLED.value:
            appt.cancel()
        return appt

    def save(self, appointment: Appointment) -> None:
        self._c.execute(
            f"INSERT OR REPLACE INTO appointments ({self._COLS}) VALUES (?, ?, ?, ?, ?)",
            (appointment.appointment_id, appointment.patient.patient_id,
             appointment.practitioner.practitioner_id,
             appointment.scheduled_at.isoformat(), appointment.status.value))
        self._c.commit()

    def find_by_id(self, appointment_id: str) -> Appointment | None:
        row = self._c.execute(f"SELECT {self._COLS} FROM appointments WHERE appointment_id = ?",
                              (appointment_id,)).fetchone()
        return self._rebuild(row) if row else None

    def find_scheduled_by_practitioner_and_time(self, practitioner_id: str,
                                                scheduled_at: datetime) -> Appointment | None:
        row = self._c.execute(
            f"SELECT {self._COLS} FROM appointments WHERE practitioner_id = ? AND scheduled_at = ? "
            "AND status = 'SCHEDULED'", (practitioner_id, scheduled_at.isoformat())).fetchone()
        return self._rebuild(row) if row else None

    def list_by_practitioner(self, practitioner_id: str) -> list[Appointment]:
        rows = self._c.execute(f"SELECT {self._COLS} FROM appointments WHERE practitioner_id = ? "
                               "ORDER BY scheduled_at", (practitioner_id,)).fetchall()
        return [self._rebuild(r) for r in rows]

    def list_by_patient(self, patient_id: str) -> list[Appointment]:
        rows = self._c.execute(f"SELECT {self._COLS} FROM appointments WHERE patient_id = ? "
                               "ORDER BY scheduled_at", (patient_id,)).fetchall()
        return [self._rebuild(r) for r in rows]
