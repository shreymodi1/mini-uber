from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RideStatus(PyEnum):
    """
    Enum for indicating the ride status.
    """
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Ride(Base):
    """
    SQLAlchemy model for ride data, storing information about ride locations,
    status, and timestamps.
    """
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    start_location = Column(String, nullable=False)
    end_location = Column(String, nullable=False)
    status = Column(Enum(RideStatus), nullable=False, default=RideStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # TODO: Consider adding foreign keys for user references or additional constraints.
    #       Implement triggers or callbacks to automatically update 'updated_at' on changes.
    #       Add indexes or unique constraints where necessary for performance and data consistency.


class RideBaseModel(BaseModel):
    """
    Base Pydantic model for shared ride fields and validation.
    """
    start_location: str = Field(..., description="Starting point of the ride.")
    end_location: str = Field(..., description="Destination point of the ride.")
    status: RideStatus = Field(RideStatus.PENDING, description="Current status of the ride.")

    class Config:
        use_enum_values = True
        extra = "forbid"
        error_msg_templates = {
            "value_error.enum": "Invalid status value provided."
        }


class RideCreateModel(RideBaseModel):
    """
    Pydantic model used when creating a new ride.
    """
    # TODO: Add additional fields or validations needed specifically for ride creation.


class RideUpdateModel(BaseModel):
    """
    Pydantic model used for updating ride data, with optional fields.
    """
    start_location: Optional[str]
    end_location: Optional[str]
    status: Optional[RideStatus]

    class Config:
        use_enum_values = True
        extra = "forbid"


class RideReadModel(RideBaseModel):
    """
    Pydantic model for reading ride data from the database.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


def handle_model_error(data: dict) -> Optional[RideBaseModel]:
    """
    Demonstrates error handling while parsing data into a ride model.

    :param data: A dictionary containing ride fields.
    :return: A valid RideBaseModel instance or None if validation fails.
    """
    try:
        return RideBaseModel(**data)
    except ValidationError as e:
        # TODO: Log or handle validation errors appropriately.
        return None

    # NOTE: In production, consider raising custom exceptions or returning error messages
    #       to the application layer as needed.