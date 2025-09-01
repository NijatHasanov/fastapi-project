from enum import Enum
from fastapi import Depends, HTTPException, status
from typing import List, Dict, Optional, Union, Any
from ..models.user import get_current_user, User


class Permission(Enum):
    """User permission levels"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"
    
    # User management permissions
    CREATE_USERS = "create_users"
    READ_USERS = "read_users"
    UPDATE_USERS = "update_users"
    DELETE_USERS = "delete_users"
    
    # Room data permissions
    CREATE_ROOM_DATA = "create_room_data"
    READ_ROOM_DATA = "read_room_data"
    UPDATE_ROOM_DATA = "update_room_data"
    DELETE_ROOM_DATA = "delete_room_data"


def has_permission(required_permissions: list[Permission]):
    """Dependency function to check if user has required permissions"""
    def permission_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return permission_checker


def get_user_permissions(user: User) -> List[Permission]:
    """Get list of permissions for a user based on their role"""
    if user.role == "admin":
        return list(Permission)  # Admin has all permissions
    
    elif user.role == "user":
        return [
            Permission.READ,
            Permission.WRITE,
            Permission.READ_ROOM_DATA,
            Permission.CREATE_ROOM_DATA,
        ]
    
    return []  # Default: no permissions


def has_permission_check(user: User, required_permission: Permission) -> bool:
    """Check if user has required permission based on their role (utility function)"""
    if not user:
        return False
    
    user_permissions = get_user_permissions(user)
    return required_permission in user_permissions


def require_permission(required_permission: Permission):
    """Decorator to require specific permission for endpoint"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # This would be used with dependency injection in FastAPI
            # For now, just return the function
            return func(*args, **kwargs)
        return wrapper
    return decorator