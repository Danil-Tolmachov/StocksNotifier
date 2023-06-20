from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from services.tickers import AbstractTiker
from services.subscriptions import AbstractSubscription


class DelayMixin():
    min_delay: datetime = datetime(hour=10)

    def __init__(self) -> None:
        self.last_event: datetime = datetime.now()

    def _condition(self, tiker: AbstractTiker) -> bool:
        if self.last_event + self.min_delay > datetime.now():
            return False

class PriceRelatedMixin():
    async def update_last_price(self):
        self.last_price = await self.ticker.get_price()


class AbstractChecker(ABC):

    @abstractmethod
    def _condition(self, tiker: AbstractTiker) -> bool:
        pass

    @classmethod
    async def create(cls, subscription: AbstractSubscription):
        self = cls()
        self.tiker: AbstractTiker = subscription.tiker
        self.last_price = await self.tiker.get_price()
        self.subscription = None

    def check(self) -> bool:
        return self._condition()



class EverydayChecker(AbstractChecker):
    delivery_time: datetime = datetime(hour=12)

    def __init__(self) -> None:
        super().__init__()

        self.delivery_date = None
        self.update_delivery_date()

    def update_delivery_date(self):
        self.delivery_date = datetime.now() + timedelta(days=1)
        self.delivery_date.replace(hour=self.delivery_time.hour, 
                                   minute=self.delivery_time.minute)

    async def _condition(self) -> bool:

        if datetime.now() > self.delivery_date:
            self.update_delivery_date()
            return True

        return False


class DropChecker(PriceRelatedMixin, DelayMixin, AbstractChecker):

    async def _condition(self) -> bool:
        current_price = await self.ticker.get_price()

        if current_price > self.last_price:
            await self.update_last_price()
            return True

        return False

class GrowthChecker(PriceRelatedMixin, DelayMixin, AbstractChecker):

    async def _condition(self) -> bool:
        current_price = await self.ticker.get_price()

        if current_price < self.last_price:
            await self.update_last_price()
            return True

        return False
