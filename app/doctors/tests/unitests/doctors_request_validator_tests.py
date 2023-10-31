from app.doctors.service import DoctorCreate
from app.doctors.request_validator import create_doctor_validator
from fastapi import HTTPException
from datetime import date, timedelta
import pytest


def test_valid_request():
    request = DoctorCreate(
        first_name="John",
        last_name="Doe",
        hiring_date=date(1990, 1, 1),
        specialization="GENERAL_INTERNAL_MEDICINE"
    )
    try:
        create_doctor_validator(request)
    except HTTPException:
        assert False, "Expected no exception to be raised"


def test_invalid_with_future_hiring_date():
    request = DoctorCreate(
        first_name="John",
        last_name="Doe",
        hiring_date=date.today() + timedelta(days=1),
        specialization="GENERAL_INTERNAL_MEDICINE"
    )
    with pytest.raises(HTTPException):
        create_doctor_validator(request)
