import pytest
from fastapi import status, HTTPException

from app.doctors.service import DoctorsService


def test_returns_doctor_with_given_id(mocker):
    # Arrange
    session_mock = mocker.Mock()
    doctor_id = 1
    doctor_data = {"id": doctor_id, "name": "John Doe"}
    session_mock.execute.return_value.scalar_one_or_none.return_value = doctor_data
    service = DoctorsService(session=session_mock)

    # Act
    result = service.get(doctor_id=doctor_id)

    # Assert
    assert result == doctor_data


def test_raises_http_exception_when_doctor_not_found(mocker):
    # Arrange
    session_mock = mocker.Mock()
    doctor_id = 1
    session_mock.execute.return_value.scalar_one_or_none.return_value = None
    service = DoctorsService(session=session_mock)

    # Act and Assert
    with pytest.raises(HTTPException) as exc:
        service.get(doctor_id=doctor_id)

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
