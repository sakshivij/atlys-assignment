from typing import List

from bson import ObjectId

from ....persistance.abstract import IScrapsDbPersistance
from ....persistance.database.mongo import get_db
from ....router.model.scrap import Scrap


class ScrapDbPersistance(IScrapsDbPersistance):
    def __init__(self):
        self.db = get_db()

    async def save(self, request_id:str, scrap_data_list: list):
        scrap_data_dicts = [scrap_data.dict() for scrap_data in scrap_data_list]
        result = await self.db.scraps.insert_many(scrap_data_dicts)
        scraps = [
            Scrap(
                id=str(inserted_id),
                request_id=request_id,
                data=scrap_data_dict  # Pass the dictionary here, not the object
            )
            for inserted_id, scrap_data_dict in zip(result.inserted_ids, scrap_data_dicts)
        ]
    
        return scraps

    async def get_by_id(self, scrap_id: str) -> Scrap:
        scrap = await self.db.scraps.find_one({"_id": ObjectId(scrap_id)})
        if scrap:
            return Scrap(** {**scrap, "id": str(scrap['_id']) })
        return None
 
    async def get_all(self) -> List[Scrap]:
        scraps_cursor = self.db.scraps.find()
        scraps = await scraps_cursor.to_list(length=None)
        return [Scrap (**{**scrap,"id": str(scrap['_id'])}) for scrap in scraps]


    async def update(self, scrap_id: str, scrap_data: Scrap) -> Scrap:
        update_fields = scrap_data.dict(exclude_unset=True)        
        if update_fields:
            result = await self.db.scraps.update_one({"_id": ObjectId(scrap_id)}, {"$set": update_fields})
            if result.modified_count > 0:
                return await self.get_scrap(scrap_id)        
        return None


    async def delete(self, scrap_id: str) -> bool:
        result = await self.db.scraps.delete_one({"_id": ObjectId(scrap_id)})
        return result.deleted_count > 0

    async def get_data_by_request_id(self, request_id: str) -> List[Scrap]:
        scraps = await self.db.scraps.find({"request_id": request_id}).to_list(None)
        if scraps:
            return [Scrap(**{**scrap, "id": str(scrap['_id'])}) for scrap in scraps]
        return []