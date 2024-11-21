from fastapi import Depends

from ..db.mongo import get_db
from .settings import SettingService
from .user import UserService


def get_user_service(db = Depends(get_db)) -> UserService:
    return UserService(db)

def get_setting_service(db = Depends(get_db)) -> SettingService:
    return SettingService(db)
