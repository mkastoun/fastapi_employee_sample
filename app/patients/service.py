from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import Session
from sqlalchemy import select
from sqlalchemy import desc
from app.patients.models import Patient, PatientCreate, PatientsList
from app.core.service import calculate_pagination
from sqlalchemy.sql import exists


class PatientsService:
    """
    This contains all the business logic for Patient entities.
    """

    def __init__(self, session: Session):
        """
        Init to initialize the session
        Args:
            session:
        """
        self.session = session

    def create(self, data: PatientCreate) -> Patient:
        """
        Responsible to check if the email already exists, and insert new record to patient
        Args:
            data: PatientCreate

        Exceptions:
            raises an HTTP exception in case the email already exists
        Returns:
            Patient
        """
        email_exists = self.session.query(exists().where(Patient.email == data.email)).scalar()

        if email_exists:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "loc": [
                            "body",
                            "email"
                        ],
                        "msg": "Email already taken",
                        "type": "value_error.email"
                    }
                ]
            )

        values = data.dict()

        patient = Patient(**values)
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)

        return patient

    def get(self, patient_id: int) -> Patient:
        """
        Responsible to return specific patient details by patient id
        Args:
            patient_id:
        Exception:
            Raises 404 http exception in case patient id not found
        Returns:
            Patient
        """
        statement = select(
            Patient
        ).where(
            Patient.id == patient_id
        )

        results = self.session.execute(statement=statement)
        patient = results.scalar_one_or_none()

        if patient is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "loc": [
                            "route",
                            "patient_id"
                        ],
                        "msg": "patient_id not found",
                        "type": "value_error.patient_id"
                    }
                ]
            )

        return patient

    def list(self, offset: int, limit: int) -> PatientsList:
        """
        Responsible to list all patients based on the offset and limit, with pagination check order by desc last name
        Args:
            offset: int
            limit: int

        Returns:
            PatientList
        """
        statement = select(
            Patient
        ).order_by(
            desc(Patient.last_name)
        ).offset(offset).limit(limit)

        patients_result = self.session.scalars(statement=statement).all()

        patients_count = self.session.query(Patient)

        metadata = calculate_pagination(offset, limit, patients_count.count())

        response_data = {
            "data": patients_result,
            "meta": metadata
        }

        return PatientsList(**response_data)
