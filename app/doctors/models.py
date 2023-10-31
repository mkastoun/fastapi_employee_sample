from sqlmodel import Field, SQLModel
from datetime import date
from typing import List
from pydantic import BaseModel

from app.core.models import TimestampModel, IDModel, PaginationModel

specializations = ["GENERAL_INTERNAL_MEDICINE",
                   "NEUROLOGY",
                   "FAMILY_MEDICINE",
                   "PSYCHIATRY",
                   "GASTROENTEROLOGY",
                   "ONCOLOGY",
                   "RADIOLOGY",
                   "GERIATRIC MEDICINE",
                   "PEDIATRICS",
                   "ORTHOPEDICS",
                   "OTOLARYNGOLOGY",
                   "OPHTHALMOLOGY",
                   "ANESTHESIOLOGY",
                   "NEUROSURGERY",
                   "GENERAL SURGERY",
                   "GNEPHROLOGY",
                   "UROLOGY",
                   "PATHOLOGY",
                   "DERMATOLOGY",
                   "EMERGENCY_MEDICINE",
                   "OBSTETRICS AND GYNAECOLOGY",
                   "CARDIOLOGY",
                   "PLASTIC_SURGERY",
                   "GENERAL_PRACTITIONER"
                   ]


class DoctorBase(SQLModel):
    """
    Doctor Model struct
    """
    first_name: str = Field(
        max_length=255,
        nullable=False
    )
    last_name: str = Field(
        max_length=255,
        nullable=False
    )
    hiring_date: date = Field(
        nullable=False
    )
    specialization: str = Field(
        max_length=255,
        nullable=False
    )


class Doctor(
    IDModel,
    TimestampModel,
    DoctorBase,
    table=True
):
    __tablename__ = "doctors"


class DoctorDetails(DoctorBase, IDModel):
    ...


class DoctorCreate(DoctorBase):
    ...


class DoctorsList(BaseModel):
    data: List[DoctorDetails]
    meta: PaginationModel
