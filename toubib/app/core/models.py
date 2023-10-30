from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import text
from sqlmodel import Field, SQLModel

"""
Core and common models can be placed here
"""


class HealthCheck(BaseModel):
    """
    Health check response model
    """
    name: str
    version: str
    description: str


class IDModel(SQLModel):
    """
    Id structure model
    """
    id: int = Field(
        default=None,
        primary_key=True,
        nullable=False
    )


class TimestampModel(SQLModel):
    """
    TimeStamp Model
    """
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
    """
    Pagination Model
    """
    offset: int
    total_items: int
    total_pages: int
    page_number: int
