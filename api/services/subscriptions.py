from services.abstractions import AbstractSubscription, AbstractTicker, AbstractDelivery


class IndividualSubscription(AbstractSubscription):
    def __init__(self, ticker: AbstractTicker, delivery: AbstractDelivery = None, id: int = None) -> None:
        self.ticker = ticker

        if id is not None:
            self.subscribe(id)
        
        if delivery is not None:
            self.delivery = delivery

    def subscribe(self, id: int):
        self.subscriber = id

    def unsubscribe(self, *args):
        self.subscriber = 0


class GroupSubscription(AbstractSubscription):
    def __init__(self, ticker: AbstractTicker, delivery: AbstractDelivery = None,  ids: list = None) -> None:
        self.ticker = ticker
        self.subscriber = []

        if ids is not None:
            self.subscribe_many(ids)
        
        if delivery is not None:
            self.delivery = delivery


    def delivery(self):
        return self.delivery
    
    def subscribe(self, id: int):
        self.subscriber.append(id)

    def subscribe_many(self, ids: list[int]):
        self.subscriber.extend(ids)

    def unsubscribe(self, id: int):
        self.subscriber.remove(id)
