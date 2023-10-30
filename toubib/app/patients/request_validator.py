import re
from datetime import date
from toubib.app.patients.models import PatientCreate
from fastapi import HTTPException, status


def create_patient_validator(request: PatientCreate):
    """
    Responsible to validate create patient body request before it reaches the service, to make sure data are as expected.
    In this way it will avoid reaching the DB unwanted data
    Args:
        request: PatientCreate (request body of create patient)
    Raises:
        HTTP Exception with 422 unprocessable entity in case any element in the body request contains faulty data
    Returns:

    """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if not re.search(regex, request.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        "email"
                    ],
                    "msg": "invalid email format",
                    "type": "value_error.email"
                }
            ]
        )

    if request.sex_at_birth not in ["FEMALE", "MALE"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        "sex_at_birth"
                    ],
                    "msg": "invalid sex_at_birth value, it should be one of: FEMALE, MALE ",
                    "type": "value_error.sex_at_birth"
                }
            ]
        )

    today = date.today()
    if request.date_of_birth > today:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": [
                        "body",
                        "date_of_birth"
                    ],
                    "msg": "invalid date_of_birth value, it should not be in the future",
                    "type": "value_error.date_of_birth"
                }
            ]
        )
