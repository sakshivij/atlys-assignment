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