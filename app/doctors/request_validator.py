from app.doctors.models import DoctorCreate, specializations
from fastapi import HTTPException, status
from datetime import date
import json


def create_doctor_validator(request: DoctorCreate):
    """
    Responsible to validate create doctor body request before it reaches the service, to make sure data are as expected.
    In this way it will avoid reaching the DB unwanted data
    Args:
        request: DoctorCreate (request body of create doctor)
    Raises:
        HTTP Exception with 422 unprocessable entity in case any element in the body request contains faulty data
    Returns:

    """
    if request.specialization not in specializations:
        specializations_as_string = json.dumps(specializations)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        "specialization"
                    ],
                    "msg": f"invalid specialization value, it should be one of: {specializations_as_string}",
                    "type": "value_error.specialization"
                }
            ]
        )
    today = date.today()
    if request.hiring_date > today:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        "hiring_date"
                    ],
                    "msg": "invalid date_of_birth value, it should not be in the future",
                    "type": "value_error.hiring_date"
                }
            ]
        )
