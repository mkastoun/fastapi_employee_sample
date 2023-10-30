from fastapi import Depends
from sqlmodel import Session

from app.core.db import get_session
from app.patients.service import PatientsService


def get_patients_service(
        session: Session = Depends(get_session)
) -> PatientsService:
    """
    Responsible to return patient service
    Args:
        session: Session

    Returns:
        Patient Service
    """
    return PatientsService(session=session)
