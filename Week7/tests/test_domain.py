"""Part F - manual behaviour checks, automated (run from stage04/: python -m pytest -q)."""
from datetime import datetime
import dataclasses
import pytest
from smartcare.domain import (Appointment, AppointmentStatus, InvalidStatusTransition,
                              Patient, Practitioner)

WHEN = datetime(2026, 10, 8, 10, 0)


def make():
    return Appointment("A1", Patient("P1", "Alice Smith"), Practitioner("D1", "Dr John Doe", "GP"), WHEN)


# --- valid objects -----------------------------------------------------------
def test_valid_objects_are_created():
    a = make()
    assert a.status is AppointmentStatus.SCHEDULED
    assert a.patient.name == "Alice Smith" and a.practitioner.specialty == "GP"


def test_text_is_trimmed():
    assert Patient("  P1 ", " Alice ").name == "Alice"


# --- invalid input -----------------------------------------------------------
@pytest.mark.parametrize("pid,name", [("", "Alice"), ("P1", ""), ("  ", "Alice"), (None, "Alice"), ("P1", None)])
def test_invalid_patient_rejected(pid, name):
    with pytest.raises(ValueError):
        Patient(pid, name)


@pytest.mark.parametrize("args", [("", "Dr", "GP"), ("D1", "", "GP"), ("D1", "Dr", ""), ("D1", "Dr", None)])
def test_invalid_practitioner_rejected(args):
    with pytest.raises(ValueError):
        Practitioner(*args)


def test_appointment_requires_domain_objects_and_datetime():
    p, pr = Patient("P1", "A"), Practitioner("D1", "B", "GP")
    with pytest.raises(TypeError):
        Appointment("A1", "P1", pr, WHEN)
    with pytest.raises(TypeError):
        Appointment("A1", p, "D1", WHEN)
    with pytest.raises(TypeError):
        Appointment("A1", p, pr, "2026-10-08 10:00")
    with pytest.raises(ValueError):
        Appointment("", p, pr, WHEN)


# --- state transitions -------------------------------------------------------
def test_cancel_scheduled_appointment():
    a = make(); a.cancel()
    assert a.status is AppointmentStatus.CANCELLED


def test_repeated_cancel_is_illegal_transition():
    a = make(); a.cancel()
    with pytest.raises(InvalidStatusTransition):
        a.cancel()
    assert a.status is AppointmentStatus.CANCELLED          # unchanged, still retained


# --- encapsulation -----------------------------------------------------------
def test_status_cannot_be_assigned_from_outside():
    a = make()
    with pytest.raises(AttributeError):
        a.status = AppointmentStatus.CANCELLED


def test_patient_is_immutable():
    with pytest.raises(dataclasses.FrozenInstanceError):
        Patient("P1", "Alice").name = "Mallory"
