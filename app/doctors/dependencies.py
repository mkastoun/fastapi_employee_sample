from fastapi import Depends
from sqlmodel import Session

from app.core.db import get_session
from app.doctors.service import DoctorsService


def get_doctors_service(
        session: Session = Depends(get_session)
) -> DoctorsService:
    """
    Responsible to return doctors service
    Args:
        session: Session

    Returns:
        Doctor Service
    """
    return DoctorsService(session=session)
