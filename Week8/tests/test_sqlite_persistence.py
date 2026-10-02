"""Data really survives in a database file (PER) - and a new connection can read it back."""
from datetime import datetime
from smartcare.persistence import (SqliteAppointmentRepository, SqlitePatientRepository,
                                   SqlitePractitionerRepository, connect)
from smartcare.services import AppointmentService, DirectoryService


def wire(path):
    conn = connect(str(path))
    pat, prac = SqlitePatientRepository(conn), SqlitePractitionerRepository(conn)
    return conn, DirectoryService(pat, prac), AppointmentService(SqliteAppointmentRepository(conn, pat, prac), pat, prac)


def test_data_survives_restart(tmp_path):
    db = tmp_path / "clinic.db"
    conn, d, s = wire(db)
    d.register_patient("P1", "Alice Smith"); d.register_practitioner("D1", "Dr Doe", "GP")
    s.book("A1", "P1", "D1", datetime(2026, 10, 8, 10)); s.book("A2", "P1", "D1", datetime(2026, 10, 8, 11))
    s.cancel("A1"); conn.close()

    conn2, d2, s2 = wire(db)                       # "restart the program"
    assert d2.find_patient("P1").name == "Alice Smith"
    assert [(a.appointment_id, a.status.value) for a in s2.history_for_patient("P1")] == \
           [("A1", "CANCELLED"), ("A2", "SCHEDULED")]
    conn2.close()
