"""Service-layer behaviour. Every test runs against BOTH repository implementations
(in-memory and SQLite) - evidence that the abstraction is substitutable (LSP/DIP)."""
from datetime import datetime
import pytest

from smartcare.domain import AppointmentStatus, InvalidStatusTransition
from smartcare.persistence import (InMemoryAppointmentRepository, InMemoryPatientRepository,
                                   InMemoryPractitionerRepository, SqliteAppointmentRepository,
                                   SqlitePatientRepository, SqlitePractitionerRepository, connect)
from smartcare.services import AppointmentService, BookingConflictError, DirectoryService, NotFoundError

T10 = datetime(2026, 10, 8, 10, 0)
T11 = datetime(2026, 10, 8, 11, 0)


def _memory():
    return (InMemoryAppointmentRepository(), InMemoryPatientRepository(), InMemoryPractitionerRepository())


def _sqlite():
    conn = connect(":memory:")
    pat, prac = SqlitePatientRepository(conn), SqlitePractitionerRepository(conn)
    return SqliteAppointmentRepository(conn, pat, prac), pat, prac


@pytest.fixture(params=[_memory, _sqlite], ids=["in-memory", "sqlite"])
def env(request):
    appts, pats, pracs = request.param()
    directory = DirectoryService(pats, pracs)
    service = AppointmentService(appts, pats, pracs)
    directory.register_patient("P1", "Alice Smith")
    directory.register_patient("P2", "Bob Johnson")
    directory.register_practitioner("D1", "Dr John Doe", "GP")
    return directory, service


def test_book_creates_scheduled_appointment(env):                              # FR-05
    _, s = env
    a = s.book("A1", "P1", "D1", T10)
    assert a.status is AppointmentStatus.SCHEDULED


def test_conflicting_booking_rejected(env):                                    # FR-06
    _, s = env
    s.book("A1", "P1", "D1", T10)
    with pytest.raises(BookingConflictError):
        s.book("A2", "P2", "D1", T10)
    assert [a.appointment_id for a in s.schedule_for_practitioner("D1")] == ["A1"]


def test_cancel_retains_history_and_frees_slot(env):                           # FR-07, FR-08
    _, s = env
    s.book("A1", "P1", "D1", T10)
    s.cancel("A1")
    assert [a.status for a in s.history_for_patient("P1")] == [AppointmentStatus.CANCELLED]
    assert s.is_available("D1", T10)
    assert s.book("A2", "P2", "D1", T10).status is AppointmentStatus.SCHEDULED


def test_repeated_cancel_rejected_by_domain(env):
    _, s = env
    s.book("A1", "P1", "D1", T10); s.cancel("A1")
    with pytest.raises(InvalidStatusTransition):
        s.cancel("A1")


def test_unknown_ids_are_not_found(env):
    _, s = env
    with pytest.raises(NotFoundError):
        s.book("A1", "NOPE", "D1", T10)
    with pytest.raises(NotFoundError):
        s.book("A1", "P1", "NOPE", T10)
    with pytest.raises(NotFoundError):
        s.cancel("NOPE")


def test_duplicate_appointment_id_rejected(env):
    _, s = env
    s.book("A1", "P1", "D1", T10)
    with pytest.raises(ValueError):
        s.book("A1", "P2", "D1", T11)


def test_schedule_shows_only_scheduled_sorted_by_time(env):                    # FR-09
    _, s = env
    s.book("A2", "P2", "D1", T11); s.book("A1", "P1", "D1", T10); s.cancel("A2")
    assert [a.appointment_id for a in s.schedule_for_practitioner("D1")] == ["A1"]


def test_patient_history_includes_cancelled(env):                              # FR-10
    _, s = env
    s.book("A1", "P1", "D1", T10); s.book("A2", "P1", "D1", T11); s.cancel("A1")
    assert [(a.appointment_id, a.status.value) for a in s.history_for_patient("P1")] == \
           [("A1", "CANCELLED"), ("A2", "SCHEDULED")]


def test_directory_find_and_duplicates(env):                                   # FR-01, FR-02, FR-03
    d, _ = env
    assert d.find_patient("P1").name == "Alice Smith"
    assert d.find_patient("NOPE") is None
    with pytest.raises(ValueError):
        d.register_patient("P1", "Someone Else")
    with pytest.raises(ValueError):
        d.register_patient("", "No Id")                                        # FR-11
