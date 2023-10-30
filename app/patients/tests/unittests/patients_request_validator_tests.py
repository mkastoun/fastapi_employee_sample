from app.patients.service import PatientCreate
from app.patients.request_validator import create_patient_validator
from fastapi import HTTPException
from datetime import date, timedelta
import pytest


def test_valid_email_sex_birth_date():
    request = PatientCreate(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        date_of_birth=date(1990, 1, 1),
        sex_at_birth="MALE"
    )
    try:
        create_patient_validator(request)
    except HTTPException:
        assert False, "Expected no exception to be raised"


def test_invalid_date_of_birth_future():
    request = PatientCreate(
        email="test@example.com",
        first_name="John",
        last_name="Doe",
        date_of_birth=date.today() + timedelta(days=1),
        sex_at_birth="MALE"
    )
    with pytest.raises(HTTPException):
        create_patient_validator(request)
