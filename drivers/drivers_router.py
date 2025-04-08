from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional


class CreateDriverRequest(BaseModel):
    """
    Request model for creating a new driver.
    """
    name: str
    email: str
    password: str
    phone_number: Optional[str] = None


class UpdateVehicleDetailsRequest(BaseModel):
    """
    Request model for updating vehicle details.
    """
    make: str
    model: str
    year: int


router = APIRouter(prefix="/drivers", tags=["drivers"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_driver_endpoint(request_data: CreateDriverRequest) -> dict:
    """
    Registers a new driver.

    Args:
        request_data (CreateDriverRequest): The information needed to create a new driver.

    Returns:
        dict: A response indicating success or failure of the operation.
    """
    try:
        # TODO: Implement driver creation logic with the database
        return {"message": "Driver created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{driver_id}/vehicle", status_code=status.HTTP_200_OK)
async def update_vehicle_details_endpoint(driver_id: int, request_data: UpdateVehicleDetailsRequest) -> dict:
    """
    Updates the vehicle details for a given driver.

    Args:
        driver_id (int): The ID of the driver whose vehicle details are to be updated.
        request_data (UpdateVehicleDetailsRequest): The vehicle details to be updated.

    Returns:
        dict: A response indicating success or failure of the operation.
    """
    try:
        # TODO: Implement vehicle detail update logic with the database
        return {"message": f"Vehicle details updated for driver {driver_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )