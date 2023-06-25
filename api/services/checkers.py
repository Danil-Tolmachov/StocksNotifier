from datetime import datetime, timedelta

from services.abstractions import AbstractChecker


class DelayMixin():
    min_delay: datetime = timedelta(hours=10)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.last_event: datetime = datetime.now()

    def update(self):
        self.last_event: datetime = datetime.now()

    def _condition(self) -> bool:
        if self.last_event + self.min_delay > datetime.now():
            return False


class PriceRelatedMixin(DelayMixin):

    async def update(self):
        super().update()
        await self.update_last_price()

    async def update_last_price(self):
        self.last_price = await self.subscription.ticker.get_price()



class EverydayChecker(AbstractChecker):
    delivery_time: datetime = timedelta(hours=12)

    def __init__(self) -> None:
        super().__init__()
        self.delivery_date = None
        self.update()

    def update(self):
        self.delivery_date = datetime.now() + timedelta(days=1)
        hours, minutes, seconds = [int(i) for i in self.delivery_time.__str__().split(':')]
        
        self.delivery_date.replace(hour=hours or 0, 
                                   minute=minutes or 0,
                                   second=seconds or 0)

    async def _condition(self) -> bool:

        if datetime.now() > self.delivery_date:
            return True

        return False


class DropChecker(PriceRelatedMixin, AbstractChecker):

    async def _condition(self) -> bool:
        if super()._condition() == False:
            return False
        
        current_price = await self.ticker.get_price()

        if current_price < self.last_price:
            return True

        return False
    

class GrowthChecker(PriceRelatedMixin, AbstractChecker):

    async def _condition(self) -> bool:
        if super()._condition() == False:
            return False
        
        current_price = await self.ticker.get_price()

        if current_price > self.last_price:
            return True

        return False
