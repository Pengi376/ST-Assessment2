"""Part H - consistency check: does the code match the approved UML (v0.3)?"""
import inspect
from datetime import datetime
import domain_skeleton as d

# The UML, written as data: class -> attributes (constructor parameters) and operations.
UML = {
    "Patient":      {"attrs": ["patient_id", "name"], "ops": []},
    "Practitioner": {"attrs": ["practitioner_id", "name", "specialty"], "ops": []},
    "Appointment":  {"attrs": ["appointment_id", "patient", "practitioner", "scheduled_at"],
                     "ops": ["cancel"]},
}
UML_ENUM = {"SCHEDULED", "CANCELLED"}


def test_every_uml_class_exists_with_the_right_attributes():
    for name, spec in UML.items():
        cls = getattr(d, name)
        params = [p for p in inspect.signature(cls.__init__).parameters if p != "self"]
        assert params == spec["attrs"], name


def test_every_uml_operation_exists():
    for name, spec in UML.items():
        for op in spec["ops"]:
            assert callable(getattr(getattr(d, name), op)), f"{name}.{op}"


def test_status_enum_matches_uml():
    assert {s.name for s in d.AppointmentStatus} == UML_ENUM


def test_associations_hold_domain_objects_not_ids():
    p = d.Patient("P1", "Alice"); pr = d.Practitioner("D1", "Dr Doe", "GP")
    a = d.Appointment("A1", p, pr, datetime(2026, 10, 8, 10))
    assert a.patient is p and a.practitioner is pr
    assert a.status is d.AppointmentStatus.SCHEDULED


def test_no_infrastructure_in_the_domain_skeleton():
    src = inspect.getsource(d)
    for banned in ("sqlite3", "input(", "print(", "Manager", "Controller"):
        assert banned not in src, banned


def test_behaviour_is_deliberately_not_implemented_yet():
    a = d.Appointment("A1", d.Patient("P1", "A"), d.Practitioner("D1", "B", "GP"), datetime(2026, 10, 8, 10))
    try:
        a.cancel()
    except NotImplementedError:
        return
    raise AssertionError("cancel() should still be a skeleton in Stage 3")
