import os

from fastapi import Depends

from .config import EnvironmentVariables
from .persistance.abstract import IPersistanceOperation
from .persistance.database.implementations.requests import RequestDbPersistance
from .persistance.database.implementations.settings import SettingDbPersistance
from .persistance.file.settings import SettingFilePersistance
from .services.requests import RequestService
from .services.settings import SettingService

env = EnvironmentVariables()
use_db = env.usedatabase.lower() == "true"

def get_setting_service() -> SettingService:
    if use_db:
        persistance = SettingDbPersistance()
    else:
        persistance = SettingFilePersistance()
    
    return SettingService(persistance=persistance)


def get_request_service() -> RequestService:
    if use_db:
        persistance = RequestDbPersistance()
    else:
        persistance = SettingFilePersistance()
    
    return RequestService(persistance=persistance)