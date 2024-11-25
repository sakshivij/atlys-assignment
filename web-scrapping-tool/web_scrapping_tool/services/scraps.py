from typing import List

from bson import ObjectId

from ..persistance.abstract import IScrapsDbPersistance
from ..router.model.scrap import Scrap, ScrapCreate


class ScrapService:
    def __init__(self, persistance: IScrapsDbPersistance):
        self.persistance = persistance

    async def create_scrap(self, request_id:str, scrap_data_list: List[ScrapCreate]) -> Scrap:
        return await self.persistance.save(request_id, scrap_data_list)

    async def get_scrap(self, scrap_id: str) -> Scrap:
        return await self.persistance.get_by_id(scrap_id)
 
    async def get_all_scraps(self) -> List[Scrap]:
        return await self.persistance.get_all()


    async def update_scrap(self, scrap_id: str, scrap_data: Scrap) -> Scrap:
        return await self.persistance.update(scrap_id, scrap_data)


    async def delete_scrap(self, scrap_id: str) -> bool:
        return await self.persistance.delete(scrap_id)
    
    async def get_scraps_by_request_id(self, request_id) -> List[Scrap]:
        return await self.persistance.get_data_by_request_id(request_id)