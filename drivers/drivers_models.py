from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Driver(Base):
    """
    SQLAlchemy model representing a driver in the system.
    TODO: Add additional columns or constraints as needed.
    """
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    license_number = Column(String, unique=True, index=True)

    vehicles = relationship("Vehicle", back_populates="driver")


class Vehicle(Base):
    """
    SQLAlchemy model representing a vehicle associated with a driver.
    TODO: Add additional columns or constraints as needed.
    """
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    driver = relationship("Driver", back_populates="vehicles")


class DriverBase(BaseModel):
    """
    Pydantic model for driver data validation.
    """
    name: str = Field(..., description="The name of the driver")
    license_number: str = Field(..., description="The license number of the driver")


class DriverCreate(DriverBase):
    """
    Pydantic model for creating a new driver entry.
    """
    pass


class DriverUpdate(DriverBase):
    """
    Pydantic model for updating an existing driver entry.
    TODO: Extend with any optional fields if necessary.
    """
    pass


class DriverInDB(DriverBase):
    """
    Pydantic model for representing a driver entry in the database.
    """
    id: int = Field(..., description="The unique identifier of the driver")

    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    """
    Pydantic model for vehicle data validation.
    """
    make: str = Field(..., description="The make of the vehicle")
    model: str = Field(..., description="The model of the vehicle")
    year: int = Field(..., description="The year of the vehicle")


class VehicleCreate(VehicleBase):
    """
    Pydantic model for creating a new vehicle entry.
    """
    pass


class VehicleUpdate(VehicleBase):
    """
    Pydantic model for updating an existing vehicle entry.
    TODO: Extend with any optional fields if necessary.
    """
    pass


class VehicleInDB(VehicleBase):
    """
    Pydantic model for representing a vehicle entry in the database.
    """
    id: int = Field(..., description="The unique identifier of the vehicle")
    driver_id: int = Field(..., description="The unique identifier of the driver owning the vehicle")

    class Config:
        orm_mode = True