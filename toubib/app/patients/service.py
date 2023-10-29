from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import Session
from sqlalchemy import select
from sqlalchemy import desc
from toubib.app.patients.models import Patient, PatientCreate, PatientsList
from sqlalchemy import func
from toubib.app.core.service import calculate_pagination


class PatientsService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: PatientCreate) -> Patient:
        values = data.dict()

        patient = Patient(**values)
        self.session.add(patient)
        self.session.commit()
        self.session.refresh(patient)

        return patient

    def get(self, patient_id: int) -> Patient:
        """

        Args:
            patient_id:

        Returns:

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
                detail="The patient's has not been found"
            )

        return patient

    def list(self, offset: int, limit: int) -> PatientsList:
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
