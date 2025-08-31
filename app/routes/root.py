from fastapi import APIRouter, Depends
from app.models.user import get_current_user

router = APIRouter()

@router.get("/")
async def root(current_user = Depends(get_current_user)):
    """
    Root endpoint that returns service status
    Requires basic authentication
    """
    return {
        "status": "ok", 
        "user": current_user.username,
        "role": current_user.role
    }