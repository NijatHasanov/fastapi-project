from typing import Optional, Dict, Any

async def authenticate_user(username: str, password: str, db) -> Optional[Dict[str, Any]]:
    """
    Simple authentication service with hardcoded users.
    Replace with real database lookup later.
    """
    # Hardcoded users for demo
    users = {
        "admin": {"password": "adminpass", "role": "admin", "id": 1},
        "viewer": {"password": "viewerpass", "role": "viewer", "id": 2}
    }
    
    user = users.get(username)
    if user and user["password"] == password:
        return {
            "id": user["id"],
            "username": username,
            "role": user["role"]
        }
    return None

async def get_user_by_username(username: str, db) -> Optional[Dict[str, Any]]:
    """
    Get user by username. Replace with database lookup later.
    """
    users = {
        "admin": {"id": 1, "role": "admin"},
        "viewer": {"id": 2, "role": "viewer"}
    }
    
    user = users.get(username)
    if user:
        return {
            "id": user["id"],
            "username": username,
            "role": user["role"]
        }
    return None