import random
from datetime import datetime
from app.models.room import RoomData

def generate_demo_rooms(count: int = 5) -> list[RoomData]:
    """Generate demo room data with random temperature and occupancy"""
    rooms = []
    for i in range(count):
        room = RoomData(
            room_id=f"room_{i+1}",
            temperature=round(random.uniform(18.0, 28.0), 1),
            occupancy=random.randint(0, 20),
            humidity=round(random.uniform(30.0, 70.0), 1),
            last_updated=datetime.utcnow()
        )
        rooms.append(room)
    return rooms

if __name__ == "__main__":
    # Generate and print demo rooms
    demo_rooms = generate_demo_rooms()
    for room in demo_rooms:
        print(room.json(indent=2))
