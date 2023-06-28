from abc import ABC, abstractmethod


class AbstractTicker(ABC):
    def __init__(self, ticker: str) -> None:
        super().__init__()
        self.ticker = ticker

    def __str__(self) -> str:
        return self.ticker
    
    @abstractmethod
    async def get_price(self) -> float:
        pass


class AbstractDelivery(ABC):
    @abstractmethod
    def _send(self):
        """Sends a message about the event"""
        pass
    
    def send(self, *args, **kwargs):
        return self._send(*args, **kwargs)


class AbstractSubscription(ABC):

    def __init__(self, ticker: AbstractTicker) -> None:
        self.ticker = ticker
        super().__init__()

    @abstractmethod
    def subscribe(self):
        pass

    @abstractmethod
    def unsubscribe(self):
        pass
    
    @property
    def delivery(self):
        return self.__delivery
    
    @delivery.setter
    def delivery(self, var):
        self.__delivery = var
    
    @property
    def subscriber(self):
        return self.__subscriber
    
    @subscriber.setter
    def subscriber(self, var):
        self.__subscriber = var

    def send(self, *args, **kwargs):
        try:
            return self.delivery.send(*args, **kwargs)
        except AttributeError:
            raise AttributeError('Create a delivery first!')

class AbstractChecker(ABC):

    def __init__(self) -> None:
        self.ticker: AbstractTicker = None
        self.last_price: int = None
        self.subscription: AbstractSubscription = None

    def __str__(self) -> str:
        return f'({self.__class__}, {id(self)}, {self.ticker})'

    @abstractmethod
    def _condition(self, ticker: AbstractTicker) -> bool:
        pass

    @abstractmethod
    def update():
        pass

    @classmethod
    async def create(cls, subscription: AbstractSubscription):
        self = cls()
        self.ticker: AbstractTicker = subscription.ticker
        self.subscription = subscription
        return self

    def check(self) -> bool:
        return self._condition()
    
    def send(self, *args, **kwargs) -> bool:
        if not self._condition():
            return False
        
        self.subscription.send(*args, **kwargs)
        return True
