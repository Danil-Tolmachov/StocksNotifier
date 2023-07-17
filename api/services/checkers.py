from datetime import datetime, timedelta

from services.abstractions import AbstractChecker, AbstractSubscription


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

    async def update(self, session):
        super().update()
        await self.update_last_price(session)

    async def update_last_price(self, session):
        self.last_price = await self.subscription.ticker.get_price(session)



class EverydayChecker(AbstractChecker):
    delivery_time: datetime = timedelta(hours=12)

    def __init__(self, sub: AbstractSubscription) -> None:
        super().__init__(sub)
        self.delivery_date = None
        self.update()

    def update(self):
        self.delivery_date = datetime.now() + timedelta(days=1)
        hours, minutes, seconds = [int(i) for i in self.delivery_time.__str__().split(':')]
        
        self.delivery_date.replace(hour=hours or 0, 
                                   minute=minutes or 0,
                                   second=seconds or 0)

    def _condition(self, *args, **kwargs) -> bool:

        if datetime.now() > self.delivery_date:
            return True

        return False
    
    async def send(self, session, *args, **kwargs) -> bool:
        if not self._condition(session):
            return False
        
        self.subscription.send(self,
                               *args,
                               ticker = str(self.ticker), 
                               subject = f'Your everyday ticker check: {str(self.ticker)}', 
                               **kwargs)
        return True


class DropChecker(PriceRelatedMixin, AbstractChecker):

    async def _condition(self, session) -> bool:
        if super()._condition() == False:
            return False
        
        current_price = await self.ticker.get_price(session)

        if current_price < self.last_price:
            return True

        return False

    async def send(self, session, *args, **kwargs) -> bool:
        if not await self._condition(session):
            return False
        
        self.subscription.send(self,
                               *args,
                               ticker = str(self.ticker), 
                               subject = f'Ticker has droped: {str(self.ticker)}', 
                               **kwargs)
        return True
    

class GrowthChecker(PriceRelatedMixin, AbstractChecker):

    async def _condition(self, session) -> bool:
        if super()._condition() == False:
            return False
        
        current_price = await self.ticker.get_price(session)

        if current_price > self.last_price:
            return True

        return False
    
    async def send(self, session, *args, **kwargs) -> bool:
        if not await self._condition(session):
            return False
        
        self.subscription.send(self,
                               *args,
                               ticker = str(self.ticker), 
                               subject = f'Ticker has increased: {str(self.ticker)}', 
                               **kwargs)
        return True
