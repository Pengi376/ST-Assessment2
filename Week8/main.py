"""Composition root: the one place that chooses concrete classes and wires the layers together.

Usage:  python main.py            (stores data in smartcare.db)
        python main.py :memory:   (temporary, nothing saved)
"""
import sys

from smartcare.persistence import (SqliteAppointmentRepository, SqlitePatientRepository,
                                   SqlitePractitionerRepository, connect)
from smartcare.presentation.cli import run
from smartcare.services import AppointmentService, DirectoryService


def build(db_path: str = "smartcare.db"):
    conn = connect(db_path)
    patients = SqlitePatientRepository(conn)
    practitioners = SqlitePractitionerRepository(conn)
    appointments = SqliteAppointmentRepository(conn, patients, practitioners)
    return DirectoryService(patients, practitioners), AppointmentService(appointments, patients, practitioners)


if __name__ == "__main__":
    directory, appointment_service = build(sys.argv[1] if len(sys.argv) > 1 else "smartcare.db")
    run(directory, appointment_service)
