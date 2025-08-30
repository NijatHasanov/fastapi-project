from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models.user import User, UserCreate, UserUpdate, UserResponse
from app.auth.permissions import Permission, has_permission
from app.database import get_db

router = APIRouter(prefix="/api/v1")

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(has_permission([Permission.CREATE_USERS])),
    db: AsyncSession = Depends(get_db)
):
    """Create a new user (requires create_users permission)"""
    # Check if username exists
    result = await db.execute(select(User).filter(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        role=user_data.role
    )
    new_user.set_password(user_data.password)
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[UserResponse])
async def list_users(
    current_user: User = Depends(has_permission([Permission.READ_USERS])),
    db: AsyncSession = Depends(get_db)
):
    """List all users (requires read_users permission)"""
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(has_permission([Permission.READ_USERS])),
    db: AsyncSession = Depends(get_db)
):
    """Get user details (requires read_users permission)"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user: User = Depends(has_permission([Permission.UPDATE_USERS])),
    db: AsyncSession = Depends(get_db)
):
    """Update user details (requires update_users permission)"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_data.email:
        user.email = user_data.email
    if user_data.role:
        # Prevent removing the last admin
        if user.role == "admin" and user_data.role != "admin":
            admin_count = await db.execute(select(User).filter(User.role == "admin"))
            if len(admin_count.scalars().all()) <= 1:
                raise HTTPException(
                    status_code=400,
                    detail="Cannot remove the last admin"
                )
        user.role = user_data.role
    if user_data.password:
        user.set_password(user_data.password)
    
    await db.commit()
    await db.refresh(user)
    return user

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(has_permission([Permission.DELETE_USERS])),
    db: AsyncSession = Depends(get_db)
):
    """Delete a user (requires delete_users permission)"""
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent deleting the last admin
    if user.role == "admin":
        admin_count = await db.execute(select(User).filter(User.role == "admin"))
        if len(admin_count.scalars().all()) <= 1:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete the last admin"
            )
    
    await db.delete(user)
    await db.commit()
