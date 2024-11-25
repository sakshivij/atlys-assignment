from hashlib import sha256
from typing import List

from bson import ObjectId
from pymongo import UpdateOne

from ....persistance.abstract import IScrapsDbPersistance
from ....persistance.database.mongo import get_db
from ....router.model.scrap import Scrap


class ScrapDbPersistance(IScrapsDbPersistance):
    def __init__(self):
        self.db = get_db()
    
    def generate_data_hash(self, scrap_data: dict) -> str:
        stable_fields = {
            "name": scrap_data.get("name"),
        }
        return sha256(str(stable_fields).encode('utf-8')).hexdigest()

    async def save(self, request_id:str, scrap_data_list: list):
        scrap_data_dicts = [scrap_data.dict() for scrap_data in scrap_data_list]

        for scrap_data_dict in scrap_data_dicts:
            scrap_data_dict['data_hash'] = self.generate_data_hash(scrap_data_dict)

        insert_ops = []
        update_ops = []

        for scrap_data_dict in scrap_data_dicts:
            existing_scrap = await self.db.scraps.find_one({"data_hash": scrap_data_dict['data_hash']})

            if existing_scrap:
                existing_data = existing_scrap['data']

                if existing_data['amount'] != scrap_data_dict.get('amount'):
                    update_ops.append(UpdateOne(
                        {"_id": existing_scrap["_id"]},
                        {"$set": {"data.amount": scrap_data_dict['amount']}}
                    ))
            else:
                insert_ops.append(scrap_data_dict)

        if insert_ops or update_ops:
            if update_ops:
                await self.db.scraps.bulk_write(update_ops)

            if insert_ops:
                result = await self.db.scraps.insert_many(insert_ops)

                inserted_scraps = [
                    Scrap(
                        id=str(inserted_id),
                        request_id=request_id,
                        data=scrap_data_dict
                    )
                    for inserted_id, scrap_data_dict in zip(result.inserted_ids, insert_ops)
                ]
                scraps = inserted_scraps
            else:
                scraps = []

        else:
            scraps = []
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