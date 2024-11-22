from typing import List

from bson import ObjectId

from ....persistance.abstract import IPersistanceOperation
from ....persistance.database.mongo import get_db
from ....router.model.request import Request, RequestCreate, Status


class RequestDbPersistance(IPersistanceOperation):
    def __init__(self):
        self.db = get_db()

    async def save(self, request_data: RequestCreate) -> Request:
        result = await self.db.requests.insert_one(request_data.dict())
        request = Request(
            id=str(result.inserted_id), 
            name=request_data.name, 
            override_page_limit=request_data.override_page_limit,
            setting_id=request_data.setting_id,
            status=request_data.status,
            meta=request_data.meta)
        return request

    async def get_by_id(self, request_id: str) -> Request:
        request = await self.db.requests.find_one({"_id": ObjectId(request_id)})
        if request:
            return Request(** {**request, "id": str(request['_id']) })
        return None
 
    async def get_all(self) -> List[Request]:
        requests_cursor = self.db.requests.find()
        requests = await requests_cursor.to_list(length=None)
        return [Request (**{**request,"id": str(request['_id'])}) for request in requests]


    async def update(self, request_id: str, request_data: Request) -> Request:
        update_fields = request_data.dict(exclude_unset=True)        
        if update_fields:
            result = await self.db.requests.update_one({"_id": ObjectId(request_id)}, {"$set": update_fields})
            if result.modified_count > 0:
                return await self.get_by_id(request_id)        
        return None


    async def delete(self, request_id: str) -> bool:
        result = await self.db.requests.delete_one({"_id": ObjectId(request_id)})
        return result.deleted_count > 0
    
    async def get_all_unprocessed(self):
        requests_cursor = self.db.requests.find({"status": Status.UNPROCESSED.value})  # Adjust if your status enum is different
        requests = await requests_cursor.to_list(length=None)
    
        return [Request(**{**request, "id": str(request["_id"])}) for request in requests]
