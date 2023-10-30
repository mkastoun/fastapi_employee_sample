from fastapi import APIRouter, Depends
from fastapi import status, Query
from fastapi_sqla import Item

from app.doctors.service import DoctorsService
from app.doctors.dependencies import get_doctors_service
from app.doctors.models import DoctorCreate, DoctorDetails, DoctorsList
from app.doctors.request_validator import create_doctor_validator

router = APIRouter()

"""
This is where the routes of doctos entity are located
"""


@router.post(
    "",
    response_model=Item[DoctorDetails],
    status_code=status.HTTP_201_CREATED
)
def create_doctor(
        data: DoctorCreate,
        doctors: DoctorsService = Depends(get_doctors_service)
):
    """
    Endpoint responsible to create endpoint
    Args:
        data: Request body DoctorCreate
        doctors: Dependency injected DoctorsService
    Raises:
        HTTP Exception 422 in case request body element is invalid
    Returns:
        JSON response Doctor created with the inserted id wrapped in data key
    """
    # Validate the create doctor request
    create_doctor_validator(request=data)
    # create Doctor
    doctor = doctors.create(data=data)

    return {"data": doctor}


@router.get(
    "/{doctor_id}",
    response_model=DoctorDetails,
    status_code=status.HTTP_200_OK
)
def get_doctor_by_id(
        doctor_id: int,
        doctors: DoctorsService = Depends(get_doctors_service)
):
    """
    Endpoint responsible to retrieve doctor details
    Args:
        doctor_id: int Doctor id
        doctors: Dependency injected
    Raises:
        HTTP Exception 404 in case not found
    Returns:
        Json Response of DoctorDetails model
    """
    doctor = doctors.get(doctor_id=doctor_id)

    return doctor


@router.get(
    "",
    response_model=DoctorsList,
    status_code=status.HTTP_200_OK
)
def get_doctors_list(
        offset: int = 0, limit: int = Query(default=10, le=100, gt=0),
        doctors: DoctorsService = Depends(get_doctors_service)
):
    """
    Endpoint Responsible to return all doctors with pagination
    Args:
        offset: int skip param
        limit: int limit of result per page
        doctors: Dependency injected DoctorsService

    Returns:
        JSON response of DoctorsList model
    """
    doctors_list = doctors.list(offset, limit)

    return doctors_list
