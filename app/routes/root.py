from fastapi import APIRouter, Depends
from app.models.user import get_current_user
from app.auth.permissions import Permission, has_permission

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
        "role": current_user.role,
        "permissions": get_user_permissions(current_user)
    }

def get_user_permissions(user):
    from app.auth.permissions import ROLE_PERMISSIONS
    return ROLE_PERMISSIONS.get(user.role, [])
