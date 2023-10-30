from datetime import date
from app.patients.models import PatientBase
import pytest


def test_create_patient_success():
    patient_data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1990, 1, 1),
        "sex_at_birth": "MALE"
    }
    patient = PatientBase(**patient_data)
    assert patient.email == "test@example.com"
    assert patient.first_name == "John"
    assert patient.last_name == "Doe"
    assert patient.date_of_birth == date(1990, 1, 1)
    assert patient.sex_at_birth == "MALE"


def test_create_patient_email_length_fail():
    patient_data = {
        "email": "a" * 321,
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": date(1990, 1, 1),
        "sex_at_birth": "MALE"
    }
    with pytest.raises(ValueError):
        patient = PatientBase(**patient_data)


def test_create_patient_first_name_length_fail():
    patient_data = {
        "email": "test@example.com",
        "first_name": "a" * 256,
        "last_name": "Doe",
        "date_of_birth": date(1990, 1, 1),
        "sex_at_birth": "MALE"
    }
    with pytest.raises(ValueError):
        patient = PatientBase(**patient_data)
