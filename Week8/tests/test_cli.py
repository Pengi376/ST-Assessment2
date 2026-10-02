"""Presentation layer: scripted console session (no real keyboard needed)."""
from smartcare.persistence import (InMemoryAppointmentRepository, InMemoryPatientRepository,
                                   InMemoryPractitionerRepository)
from smartcare.presentation.cli import run
from smartcare.services import AppointmentService, DirectoryService


def session(lines):
    pats, pracs, appts = InMemoryPatientRepository(), InMemoryPractitionerRepository(), InMemoryAppointmentRepository()
    out, feed = [], iter(lines)
    run(DirectoryService(pats, pracs), AppointmentService(appts, pats, pracs),
        read=lambda prompt: next(feed), write=out.append)
    return "\n".join(out)


def test_full_booking_conflict_and_cancel_flow():
    text = session([
        "1", "P1", "Alice Smith",                    # register patient
        "3", "D1", "Dr John Doe", "GP",              # register practitioner
        "4", "2026-10-08 10:00", "A1", "P1", "D1",   # book
        "4", "2026-10-08 10:00", "A2", "P1", "D1",   # conflicting booking
        "5", "A1",                                   # cancel
        "5", "A1",                                   # cancel again -> error
        "7", "P1",                                   # history
        "0"])
    assert "Booked: A1" in text
    assert "Error: Practitioner already has an appointment at that time" in text
    assert "Cancelled: A1" in text and "Error: Only scheduled appointments can be cancelled" in text
    assert "A1 | 2026-10-08 10:00 | Alice Smith with Dr John Doe | CANCELLED" in text
    assert text.rstrip().endswith("Goodbye.")


def test_bad_date_and_bad_menu_choice_do_not_crash():
    text = session(["4", "not-a-date", "9", "0"])
    assert "Error:" in text and "Please choose a number" in text
