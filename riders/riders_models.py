from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Rider(Base):
    """
    SQLAlchemy model for the riders table.
    """
    __tablename__ = "riders"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone_number = Column(String(20), unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)


class RiderBase(BaseModel):
    """
    Shared base model for rider data.
    """
    name: str = Field(..., max_length=100)
    email: EmailStr
    phone_number: Optional[str] = None
    is_active: bool = True


class RiderCreate(RiderBase):
    """
    Model for creating a new rider.
    """
    # TODO: Add additional fields or validations specific to rider creation if needed


class RiderUpdate(RiderBase):
    """
    Model for updating rider data.
    """
    # TODO: Add fields or validations for partially updating rider data if needed


class RiderInDB(RiderBase):
    """
    Model representing rider data stored in the database.
    """
    id: int

    class Config:
        orm_mode = True