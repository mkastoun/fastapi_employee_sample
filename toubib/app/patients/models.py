from sqlmodel import Field, SQLModel
from sqlalchemy import Column, event
from sqlalchemy.databases import postgres
from datetime import date

from toubib.app.core.models import TimestampModel, IDModel

gender_types = postgres.ENUM(
    "FEMALE",
    "MALE"
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
    ...  # todo add functionality


class PatientCreate(PatientBase):
    ...  # todo add functionality
