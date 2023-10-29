from fastapi import Depends
from sqlmodel import Session

from toubib.app.core.db import get_session
from toubib.app.patients.service import PatientsService


def get_patients_service(
        session: Session = Depends(get_session)
) -> PatientsService:
    return PatientsService(session=session)
