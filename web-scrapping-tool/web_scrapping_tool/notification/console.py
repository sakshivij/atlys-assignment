import inspect

from .abstract import INotificationOperation


class ConsoleNotification(INotificationOperation):
    def notify(self, total_records: list, request_id: str):
        print(f"{self.__class__.__name__} :::: {inspect.currentframe().f_code.co_name} ::: Scraped {total_records} records for request: {request_id}")