"""Part F - verify behaviour with normal and unusual inputs (run: python -m pytest -q)."""
import pytest
import smartcare_v01 as sc


@pytest.fixture(autouse=True)
def clean():
    sc.appointments.clear()


def test_normal_appointment_is_stored():
    sc.book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
    assert sc.appointments == [{"patient": "Alice Smith", "practitioner": "Dr. John Doe",
                                "time": "2024-07-20 10:00 AM"}]


@pytest.mark.parametrize("name", ["", "   ", None])
def test_blank_or_none_patient_rejected(name):
    with pytest.raises(ValueError):
        sc.book_appointment(name, "Dr. John Doe", "2024-07-20 10:00 AM")
    assert sc.appointments == []


def test_none_appointment_time_rejected():
    with pytest.raises(ValueError):
        sc.book_appointment("Alice Smith", "Dr. John Doe", None)


def test_none_practitioner_rejected():
    with pytest.raises(ValueError):
        sc.book_appointment("Alice Smith", None, "2024-07-20 10:00 AM")


def test_same_practitioner_and_time_is_STILL_accepted_known_limitation():
    """Documented limitation: v0.1 has no conflict rule (addressed in Stage 2 FR-06 / Stage 4+)."""
    sc.book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
    sc.book_appointment("Bob Johnson", "Dr. John Doe", "2024-07-20 10:00 AM")
    assert len(sc.appointments) == 2
