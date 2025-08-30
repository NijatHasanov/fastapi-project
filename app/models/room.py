from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoomData(BaseModel):
    room_id: str
    temperature: float
    occupancy: int
    humidity: Optional[float] = None
    last_updated: datetime = datetime.utcnow()

    class Config:
        from_attributes = True
