from typing import List

from bson import ObjectId

from ..persistance.abstract import IRequestDbPersistance
from ..router.model.request import Request, RequestCreate


class RequestService:
    def __init__(self, persistance: IRequestDbPersistance):
        self.persistance = persistance

    async def create_request(self, request_data: RequestCreate) -> Request:
        return await self.persistance.save(request_data)

    async def get_request(self, request_id: str) -> Request:
        return await self.persistance.get_by_id(request_id)
 
    async def get_all_requests(self) -> List[Request]:
        return await self.persistance.get_all()


    async def update_request(self, request_id: str, request_data: Request) -> Request:
        return await self.persistance.update(request_id, request_data)


    async def delete_request(self, request_id: str) -> bool:
        return await self.persistance.delete(request_id)
    
    async def get_all_unprocessed(self) -> List[Request]:
        return await self.persistance.get_all_unprocessed()