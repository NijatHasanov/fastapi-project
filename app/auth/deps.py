from typing import Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose.exceptions import JWTError
from pydantic import BaseModel

from app.auth.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

class CurrentUser(BaseModel):
    username: str
    role: str

async def get_current_user(token: str = Depends(oauth2_scheme)) -> CurrentUser:
    """
    Decode JWT token and return current user info.
    """
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        role = payload.get("role")
        
        if username is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        return CurrentUser(username=username, role=role)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def require_role(role: str) -> Callable:
    """
    Dependency to require specific role. 
    - 'viewer' accepts both viewer and admin
    - other roles require exact match
    """
    async def role_checker(user: CurrentUser = Depends(get_current_user)):
        if role == "viewer":
            # Admin can access viewer endpoints
            if user.role not in ("viewer", "admin"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        else:
            # Exact role match required
            if user.role != role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        return user
    return role_checker