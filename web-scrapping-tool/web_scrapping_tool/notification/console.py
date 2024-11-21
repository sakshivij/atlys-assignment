from .abstract import INotificationOperation


class ConsoleNotification(INotificationOperation):
    def notify():
        print("Scrapped")