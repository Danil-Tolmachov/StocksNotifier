from abc import ABC, abstractmethod
from datetime import datetime

from services.checkers import AbstractTiker


class AbstractCondition(ABC):
    @abstractmethod
    def _check_condition(self, tiker: AbstractTiker) -> bool:
        pass
    
    def check(self) -> bool:
        return self._check_condition()


class EverydayCondition(AbstractCondition):
    delivery_date: datetime = None
    pass

class DropCondition(AbstractCondition):
    pass

class GrowthCondition(AbstractCondition):
    pass
