from typing import List

from bson import ObjectId

from ..persistance.abstract import IPersistanceOperation
from ..router.model.setting import Setting, SettingCreate


class SettingService:
    def __init__(self, persistance: IPersistanceOperation):
        self.persistance = persistance

    async def create_setting(self, setting_data: SettingCreate) -> Setting:
        return await self.persistance.save(setting_data)

    async def get_setting(self, setting_id: str) -> Setting:
        return await self.persistance.get_by_id(setting_id)
 
    async def get_all_settings(self) -> List[Setting]:
        return await self.persistance.get_all()


    async def update_setting(self, setting_id: str, setting_data: Setting) -> Setting:
        return await self.persistance.update(setting_id, setting_data)


    async def delete_setting(self, setting_id: str) -> bool:
        return await self.persistance.delete(setting_id)