from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import Session
from sqlalchemy import select
from sqlalchemy import desc
from app.doctors.models import Doctor, DoctorCreate, DoctorsList
from app.core.service import calculate_pagination


class DoctorsService:
    """
    This contains all the business logic for Doctors entities.
    """
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: DoctorCreate) -> Doctor:
        """
        Responsible to insert new record to Doctor
        Args:
            data: DoctorCreate
        Returns:
            Doctor
        """
        values = data.dict()

        doctor = Doctor(**values)

        self.session.add(doctor)
        self.session.commit()
        self.session.refresh(doctor)

        return doctor

    def get(self, doctor_id: int) -> Doctor:
        """
        Responsible to return specific doctor details by doctor id
        Args:
            doctor_id: int
        Raises:
            Raises 404 http exception in case doctor id not found
        Returns:
            Doctor
        """
        statement = select(
            Doctor
        ).where(
            Doctor.id == doctor_id
        )

        results = self.session.execute(statement=statement)
        doctor = results.scalar_one_or_none()

        if doctor is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "loc": [
                            "route",
                            "doctor_id"
                        ],
                        "msg": "doctor_id not found",
                        "type": "value_error.doctor_id"
                    }
                ]
            )

        return doctor

    def list(self, offset: int, limit: int) -> DoctorsList:
        """
        Responsible to list all doctors based on the offset and limit, with pagination order by desc last name
        Args:
            offset: int
            limit: int

        Returns:
            DoctorsList
        """
        statement = select(
            Doctor
        ).order_by(
            desc(Doctor.last_name)
        ).offset(offset).limit(limit)

        doctors_result = self.session.scalars(statement=statement).all()

        doctors_count = self.session.query(Doctor)

        metadata = calculate_pagination(offset, limit, doctors_count.count())

        response_data = {
            "data": doctors_result,
            "meta": metadata
        }

        return DoctorsList(**response_data)
