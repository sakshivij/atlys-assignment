from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from ..services.service_provider import get_user_service
from ..services.user import UserService
from .model.user import User, UserCreate

router = APIRouter(prefix="/users")

@router.post("", response_model=User)
async def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    db_user = await service.create_user(name=user.name)
    return db_user

@router.get("/{ user_id}", response_model=User)
async def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    db_user = await service.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("", response_model=List[User])
async def get_all_users(service: UserService = Depends(get_user_service)):
    return await service.get_all_users()

@router.put("/{ user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate, service: UserService = Depends(get_user_service)):
    db_user = await service.update_user(user_id=user_id, name=user.name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{ user_id}")
async def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    await service.delete_user(user_id=user_id)
    return {"detail": "User deleted"}
