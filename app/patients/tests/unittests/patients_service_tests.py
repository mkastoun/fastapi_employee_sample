import pytest
from fastapi import status, HTTPException

from app.patients.models import PatientCreate
from app.patients.service import PatientsService


def test_create_email_already_exists(mocker):
    # Arrange
    data = PatientCreate(
        email="example@example.com",
        first_name="John",
        last_name="Doe",
        date_of_birth="1990-01-01",
        sex_at_birth="male"
    )
    session_mock = mocker.Mock()
    session_mock.query.return_value.exists.return_value.scalar.return_value = True
    service = PatientsService(session=session_mock)

    # Act and Assert
    with pytest.raises(HTTPException) as exc:
        service.create(data)

    assert exc.value.status_code == status.HTTP_409_CONFLICT

