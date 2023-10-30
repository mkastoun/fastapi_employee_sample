from fastapi import APIRouter, Depends
from fastapi import status, Query
from fastapi_sqla import Item

from app.patients.service import PatientsService
from app.patients.dependencies import get_patients_service
from app.patients.models import PatientCreate, PatientDetails, PatientsList
from app.patients.request_validator import create_patient_validator

router = APIRouter()

"""
This is where the routes of patients entity are located
"""


@router.post(
    "",
    response_model=Item[PatientDetails],
    status_code=status.HTTP_201_CREATED
)
def create_patient(
        data: PatientCreate,
        patients: PatientsService = Depends(get_patients_service)
):
    """
    Endpoint responsible to create endpoint
    Args:
        data: Request body PatientCreate
        patients: Dependency injected patientsService
    Raises:
        HTTP Exception 409 in case Email not found
        HTTP Exception 422 in case request body element is invalid
    Returns:
        JSON response Patient created with the inserted id wrapped in data key
    """
    # Validate the create patient request
    create_patient_validator(request=data)
    # create Patient
    patient = patients.create(data=data)

    return {"data": patient}


@router.get(
    "/{patient_id}",
    response_model=PatientDetails,
    status_code=status.HTTP_200_OK
)
def get_patient_by_id(
        patient_id: int,
        patients: PatientsService = Depends(get_patients_service)
):
    """
    Endpoint responsible to retrieve patient details
    Args:
        patient_id: int Patient id
        patients: Dependency injected patientsService
    Raises:
        HTTP Exception 404 in case not found
    Returns:
        Json Response of PatientDetails model
    """
    # Get patient details
    patient = patients.get(patient_id=patient_id)

    return patient


@router.get(
    "",
    response_model=PatientsList,
    status_code=status.HTTP_200_OK
)
def get_patients_list(
        offset: int = 0, limit: int = Query(default=10, le=100, gt=0),
        patients: PatientsService = Depends(get_patients_service)
):
    """
    Endpoint Responsible to return all patients with pagination
    Args:
        offset: int skip param
        limit: int limit of result per page
        patients: Dependency injected patientsService

    Returns:
        JSON response of PatientsList model
    """
    patients_list = patients.list(offset, limit)

    return patients_list
