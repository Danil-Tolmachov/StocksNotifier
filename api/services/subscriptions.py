from abc import ABC, abstractmethod
from services.conditions import AbstractCondition
from conditions import AbstractCondition


class AbstractSubscriptionManager(ABC):  
    @abstractmethod
    def subscribe(self):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass


class EmailSubscriptionManager(AbstractSubscriptionManager):
    def subscribe(self, email: str):
        pass

    def unsubscribe(self, email: str):
        pass
        

class AbstractSubscription(ABC):
    _instances = []

    def __new__(cls, condition: AbstractCondition):

        for obj in cls._instances:
            if obj.condition.__class__ == condition:
                return obj

        new_obj = super().__new__(cls)
        cls._instances.append(new_obj)
        return new_obj

    def __init__(self, condition: AbstractCondition, manager: AbstractSubscriptionManager) -> None:
        super().__init__()
        self.condition = condition
        self.manager = manager
        self.subscribers = []

    @property
    @abstractmethod
    def manager(self) -> AbstractSubscriptionManager:
        pass

    @property
    @abstractmethod
    def condition(self) -> AbstractCondition:
        pass


    @abstractmethod
    def _send_notification(self) -> bool:
        """Sends a message about the event"""
        pass


    def notify(self) -> bool:
        if self.condition.check() == True:
            self._send_notification()


class EmailSubscription(AbstractSubscription):

    def _send_notification(self):
        pass

    
