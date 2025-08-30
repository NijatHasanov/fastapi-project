from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.room import RoomData
from app.models.user import get_current_user, User

router = APIRouter()

# Temporary in-memory storage
room_data_storage = []

@router.post("/data", response_model=RoomData)
async def create_room_data(
    data: RoomData,
    current_user: User = Depends(get_current_user)
):
    """
    Create new room data
    Requires authentication and admin role
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required")
    room_data_storage.append(data)
    return data

@router.get("/data/all", response_model=List[RoomData])
async def get_all_room_data(
    current_user: User = Depends(get_current_user)
):
    """
    Get all room data
    Requires authentication (both admin and viewer roles allowed)
    """
    return room_data_storage
