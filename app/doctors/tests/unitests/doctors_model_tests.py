from datetime import date
from app.doctors.models import DoctorBase
import pytest


def test_create_doctor_success():
    doctor_data = {
        "first_name": "John",
        "last_name": "Doe",
        "hiring_date": date(1990, 1, 1),
        "specialization": "GENERAL_INTERNAL_MEDICINE"
    }
    doctor = DoctorBase(**doctor_data)
    assert doctor.first_name == "John"
    assert doctor.last_name == "Doe"
    assert doctor.hiring_date == date(1990, 1, 1)
    assert doctor.specialization == "GENERAL_INTERNAL_MEDICINE"


def test_create_doctor_first_name_length_fail():
    doctor_data = {
        "first_name": "a" * 256,
        "last_name": "Doe",
        "hiring_date": date(1990, 1, 1),
        "specialization": "GENERAL_INTERNAL_MEDICINE"
    }
    with pytest.raises(ValueError):
        doctor = DoctorBase(**doctor_data)

