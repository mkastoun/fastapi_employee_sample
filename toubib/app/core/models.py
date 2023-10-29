from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import text
from sqlmodel import Field, SQLModel


class HealthCheck(BaseModel):
    name: str
    version: str
    description: str


class IDModel(SQLModel):
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False
    )


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)")
        }
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)")
        }
    )


class PaginationModel(BaseModel):
    offset: int
    total_items: int
    total_pages: int
    page_number: int

