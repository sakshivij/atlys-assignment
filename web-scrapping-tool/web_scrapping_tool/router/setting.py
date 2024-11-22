from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from ..dependencies import get_setting_service
from ..services.settings import SettingService
from ..utils.authentication import verify_token
from .model.setting import Setting, SettingCreate

router = APIRouter(prefix="/settings")

@router.post("", response_model=Setting)
async def create_setting(setting: SettingCreate, service: SettingService = Depends(get_setting_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    db_setting = await service.create_setting(setting_data=setting)
    return db_setting

@router.get("/{setting_id}", response_model=Setting)
async def get_setting(setting_id: str, service: SettingService = Depends(get_setting_service)):
    db_setting = await service.get_setting(setting_id=setting_id)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.get("", response_model=List[Setting])
async def get_all_settings(service: SettingService = Depends(get_setting_service)):
    return await service.get_all_settings()

@router.put("/{setting_id}", response_model=Setting)
async def update_setting(setting_id: str, setting: SettingCreate, service: SettingService = Depends(get_setting_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    db_setting = await service.update_setting(setting_id=setting_id, setting_data=setting)
    if db_setting is None:
        raise HTTPException(status_code=404, detail="Setting not found")
    return db_setting

@router.delete("/{setting_id}")
async def delete_setting(setting_id: str, service: SettingService = Depends(get_setting_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    await service.delete_setting(setting_id=setting_id)
    return {"detail": "Setting deleted"}
