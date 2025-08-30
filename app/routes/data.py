from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import desc
from app.models.room import RoomData, RoomDataCreate, RoomDataResponse
from app.models.user import User, get_current_user
from app.database import get_db
from app.auth.permissions import Permission, has_permission

router = APIRouter(prefix="/api/v1")

@router.post("/data", response_model=RoomDataResponse)
async def create_room_data(
    data: RoomDataCreate,
    current_user: User = Depends(has_permission([Permission.CREATE_ROOM_DATA])),
    db: AsyncSession = Depends(get_db)
):
    """
    Store room data in PostgreSQL database
    Requires create_room_data permission (admin role)
    """
    db_data = RoomData(**data.dict())
    db.add(db_data)
    await db.commit()
    await db.refresh(db_data)
    return db_data

@router.get("/room/{room_id}/latest", response_model=RoomDataResponse)
async def get_latest_room_data(
    room_id: str,
    current_user: User = Depends(has_permission([Permission.READ_ROOM_DATA])),
    db: AsyncSession = Depends(get_db)
):
    """
    Get the most recent data for a specific room
    Requires read_room_data permission (admin or viewer role)
    """
    query = select(RoomData).filter(RoomData.room_id == room_id).order_by(desc(RoomData.timestamp)).limit(1)
    result = await db.execute(query)
    data = result.scalar_one_or_none()
    
    if not data:
        raise HTTPException(status_code=404, detail=f"No data found for room {room_id}")
    
    return data
