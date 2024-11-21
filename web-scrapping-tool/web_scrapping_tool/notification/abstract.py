from __future__ import annotations

from abc import ABC, abstractmethod


class INotificationOperation(ABC):

    @abstractmethod
    def notify(self, **kwargs):
        pass