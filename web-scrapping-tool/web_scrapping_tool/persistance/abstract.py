from __future__ import annotations

from abc import ABC, abstractmethod


class IPersistanceOperation(ABC):

    @abstractmethod
    def save(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, **kwargs):
        pass

    @abstractmethod
    def get_all(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass

class IScrapsDbPersistance(IPersistanceOperation):
    @abstractmethod
    async def get_data_by_request_id(self, request_id: str):
        pass

class IRequestDbPersistance(IPersistanceOperation):
    @abstractmethod
    async def get_all_unprocessed(self, request_id: str):
        pass