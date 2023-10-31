from sqlmodel import Field, SQLModel
from sqlalchemy import Column, event
from sqlalchemy.databases import postgres
from datetime import date
from typing import List
from pydantic import BaseModel

from app.core.models import TimestampModel, IDModel, PaginationModel

# The gender types that a patient can have
gender_types = postgres.ENUM(
    "FEMALE",
    "MALE",
    name=f"gender_types"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    """
    Responsible to create the enum as a datatype in the db before creating the patient table
    Args:
        metadata:
        conn:
        **kw:

    Returns:

    """
    gender_types.create(conn, checkfirst=True)


class PatientBase(SQLModel):
    """
    Patient Model structure
    """
    email: str = Field(
        max_length=320,
        nullable=False,
        unique=True
    )
    first_name: str = Field(
        max_length=255,
        nullable=False
    )
    last_name: str = Field(
        max_length=255,
        nullable=False
    )
    date_of_birth: date = Field(
        nullable=False
    )
    sex_at_birth: str = Field(
        sa_column=Column(
            "sex_at_birth",
            gender_types,
            nullable=False
        )
    )


class Patient(
    IDModel,
    TimestampModel,
    PatientBase,
    table=True
):
    __tablename__ = "patients"


class PatientDetails(PatientBase, IDModel):
    ...


class PatientCreate(PatientBase):
    ...


class PatientsList(BaseModel):
    """
    Response model for list of patients.
    """
    data: List[PatientDetails]
    meta: PaginationModel
