from sqlmodel import Field, SQLModel
from sqlalchemy import Column, event
from sqlalchemy.databases import postgres
from datetime import date
from typing import List
from pydantic import BaseModel

from toubib.app.core.models import TimestampModel, IDModel, PaginationModel

gender_types = postgres.ENUM(
    "FEMALE",
    "MALE",
    name=f"gender_types"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):
    gender_types.create(conn, checkfirst=True)


class PatientBase(SQLModel):
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
        default=None,
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
    data: List[PatientBase]
    meta: PaginationModel
