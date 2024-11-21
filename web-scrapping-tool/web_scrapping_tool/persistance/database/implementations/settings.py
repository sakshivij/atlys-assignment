from typing import List

from bson import ObjectId

from ....persistance.abstract import IPersistanceOperation
from ....persistance.database.mongo import get_db
from ....router.model.setting import Setting, SettingCreate


class SettingDbPersistance(IPersistanceOperation):
    def __init__(self):
        self.db = get_db()

    async def save(self, setting_data: SettingCreate) -> Setting:
        result = await self.db.settings.insert_one(setting_data.dict())
        setting = Setting(
            id=result.inserted_id, 
            name=setting_data.name, 
            is_page_query_parameter=setting_data.is_page_query_parameter,
            is_scrapping_paginated=setting_data.is_scrapping_paginated,
            max_pages_limit=setting_data.max_pages_limit,
            proxy=setting_data.proxy,
            base_url=setting_data.base_url)
        return setting

    async def get_by_id(self, setting_id: str) -> Setting:
        setting = await self.db.settings.find_one({"_id": ObjectId(setting_id)})
        if setting:
            return Setting(** {**setting, "id": str(setting['_id']) })
        return None
 
    async def get_all(self) -> List[Setting]:
        settings_cursor = self.db.settings.find()
        settings = await settings_cursor.to_list(length=None)
        return [Setting (**{**setting,"id": str(setting['_id'])}) for setting in settings]


    async def update(self, setting_id: str, setting_data: Setting) -> Setting:
        update_fields = setting_data.dict(exclude_unset=True)        
        if update_fields:
            result = await self.db.settings.update_one({"_id": ObjectId(setting_id)}, {"$set": update_fields})
            if result.modified_count > 0:
                return await self.get_setting(setting_id)        
        return None


    async def delete(self, setting_id: str) -> bool:
        result = await self.db.settings.delete_one({"_id": ObjectId(setting_id)})
        return result.deleted_count > 0
    
    async def get_all_unprocessed(self, **kwargs):
        pass
