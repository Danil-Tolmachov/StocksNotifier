from abc import ABC, abstractmethod

from services.delivery import AbstractDelivery
from services.checkers import AbstractChecker
from services.tickers import AbstractTiker
from database.models import User


class AbstractSubscription(ABC):
    def __init__(self, tiker: AbstractTiker) -> None:
        self.tiker = tiker
        super().__init__()
    
    @property
    @abstractmethod
    def delivery(self):
        pass

    @property
    @abstractmethod
    def subscribers(self):
        pass


    @abstractmethod
    def create_checker(self) -> AbstractChecker:
        pass

    @abstractmethod
    def create_delivery(self) -> AbstractDelivery:
        pass


    @abstractmethod
    def subscribe(self):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass

    @abstractmethod
    def send(self):
        pass


class IndividualSubscription(AbstractSubscription):
    def __init__(self, id: int = None) -> None:
        super().__init__()

        if id is not None:
            self.subscriber: int = id

    def subscribe(self, id: int):
        self.subscriber = id

    def unsubscribe(self):
        del self

    def send(self):
        self.create_delivery().send()


class GroupSubscription(AbstractSubscription):
    def __init__(self, ids: list = None) -> None:
        super().__init__()

        if ids is not None:
            self.subscribers: list[int] = ids

    def subscribe(self, id: int):
        self.subscribers.append(id)

    def subscribe_many(self, ids: list[int]):
        self.subscribers.extend(ids)

    def unsubscribe(self, id: int):
        self.subscribers.remove(id)

    def send(self):
        self.create_delivery().send()
