"""One test per Given-When-Then acceptance criterion in SmartCare v0.2 (AC-01 .. AC-06)."""
import pytest
import smartcare_v02 as sc


@pytest.fixture(autouse=True)
def clean():
    sc.patients.clear(); sc.appointments.clear()
    sc.register_patient("P1", "Alice Smith")


def test_AC01_valid_booking_is_scheduled():
    a = sc.book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    assert a["status"] == "SCHEDULED"


def test_AC02_conflicting_booking_rejected_and_existing_unchanged():       # negative
    first = sc.book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    with pytest.raises(ValueError):
        sc.book("A2", "P1", "Dr. John Doe", "2026-10-08 10:00")
    assert sc.appointments == [first] and first["status"] == "SCHEDULED"


def test_AC03_cancel_keeps_appointment_in_history():
    sc.book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    sc.cancel("A1")
    assert [a["status"] for a in sc.history_for_patient("P1")] == ["CANCELLED"]


def test_AC04_cancelling_twice_is_rejected():                               # negative
    sc.book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    sc.cancel("A1")
    with pytest.raises(ValueError):
        sc.cancel("A1")


def test_AC05_patient_search_found_and_not_found():                         # includes negative
    assert sc.find_patient("P1") == "Alice Smith"
    assert sc.find_patient("NOPE") is None


def test_AC06_cancelled_slot_can_be_rebooked():
    sc.book("A1", "P1", "Dr. John Doe", "2026-10-08 10:00")
    sc.cancel("A1")
    assert sc.book("A2", "P1", "Dr. John Doe", "2026-10-08 10:00")["status"] == "SCHEDULED"
