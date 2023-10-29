import sys

from fastapi import APIRouter, Depends
from fastapi import status, Query
from fastapi_sqla import Item

from toubib.app.patients.service import PatientsService
from toubib.app.patients.dependencies import get_patients_service
from toubib.app.patients.models import PatientCreate, PatientDetails, PatientsList
from toubib.app.patients.request_validator import create_patient_validator

router = APIRouter()


@router.post(
    "",
    response_model=Item[PatientDetails],
    status_code=status.HTTP_201_CREATED
)
def create_patient(
        data: PatientCreate,
        patients: PatientsService = Depends(get_patients_service)
):
    create_patient_validator(request=data)
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
    patient = patients.get(patient_id=patient_id)

    return patient


@router.get(
    "",
    response_model=PatientsList,
    status_code=status.HTTP_200_OK
)
def get_patients_list(
        offset: int = 0, limit: int = Query(default=10, le=100),
        patients: PatientsService = Depends(get_patients_service)
):
    patients_list = patients.list(offset, limit)

    return patients_list
