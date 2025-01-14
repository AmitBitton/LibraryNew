class Subject:

    def __init__(self):
        self._observers = []

    def register_observer(self, observer):
        self._observers.append(observer)

    def unregister_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, notification):
        for observer in self._observers:
            observer.update(notification)


class Observer:
    def update(self, notification):
        pass
