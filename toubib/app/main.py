import uvicorn
from datetime import date
from importlib.metadata import version

import fastapi_sqla
from fastapi import Depends, FastAPI, HTTPException
from fastapi_sqla import Item, Session
from pydantic import BaseModel
from structlog import get_logger
from toubib.app import settings

from toubib.sqla import Doctor
from toubib.app.core.models import HealthCheck

log = get_logger()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)

fastapi_sqla.setup(app)


@app.get("/health", response_model=HealthCheck, tags=["status"])
def health():
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description
    }


class DoctorIn(BaseModel):
    first_name: str
    last_name: str
    hiring_date: date
    specialization: str


class DoctorModel(DoctorIn):
    id: int

    class Config:
        orm_mode = True


@app.post("/v1/doctors", response_model=Item[DoctorModel], status_code=201)
def create_doctor(*, body: DoctorIn, session: Session = Depends()):
    doctor = Doctor(**body.dict())
    session.add(doctor)
    session.flush()
    return {"data": doctor}


@app.get("/v1/doctors/{doctor_id}", response_model=Item[DoctorModel])
def get_doctor(*, doctor_id: int, session: Session = Depends()):
    doctor = session.get(Doctor, doctor_id)
    if doctor is None:
        raise HTTPException(404)
    return {"data": doctor}


@app.get("/v1/patients")
def list_patients():
    pass


@app.post("/v1/patients")
def create_patient():
    pass


@app.get("/v1/patients/{patient_id}")
def get_patient():
    pass

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
