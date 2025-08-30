from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from pydantic import BaseModel
from app.database import Base

class RoomData(Base):
    __tablename__ = "room_data"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, index=True)
    temp = Column(Float)
    humidity = Column(Float)
    occupied = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)

class RoomDataCreate(BaseModel):
    room_id: str
    temp: float
    humidity: float
    occupied: bool

class RoomDataResponse(RoomDataCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
