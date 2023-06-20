from abc import ABC, abstractmethod


class AbstractTiker(ABC):
    def __init__(self, tiker) -> None:
        super().__init__()
        self.tiker = tiker

    def __str__(self) -> str:
        return self.tiker
    
    @abstractmethod
    async def get_price(self) -> float:
        pass

class Tiker(AbstractTiker):
    pass