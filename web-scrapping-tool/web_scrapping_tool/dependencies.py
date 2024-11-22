import os

from fastapi import Depends

from .config import EnvironmentVariables
from .persistance.abstract import IPersistanceOperation
from .persistance.database.implementations.requests import RequestDbPersistance
from .persistance.database.implementations.scraps import ScrapDbPersistance
from .persistance.database.implementations.settings import SettingDbPersistance
from .persistance.file.requests import RequestFilePersistance
from .persistance.file.scraps import ScrapFilePersistance
from .persistance.file.settings import SettingFilePersistance
from .services.requests import RequestService
from .services.scraps import ScrapService
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
        persistance = RequestFilePersistance()
    
    return RequestService(persistance=persistance)

def get_scrap_service() -> ScrapService:
    if use_db:
        persistance = ScrapDbPersistance()
    else:
        persistance = ScrapFilePersistance()
    
    return ScrapService(persistance=persistance)

