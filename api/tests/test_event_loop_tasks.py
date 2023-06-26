import pytest
from fixtures import fake_mongo

from event_loop.tasks import load_checkers
from event_loop.utils import super_len
from services.delivery import EmailDelivery
from services.tickers import Ticker
from services.checkers import EverydayChecker, GrowthChecker
from services.subscriptions import IndividualSubscription, GroupSubscription


@pytest.mark.skip
def test_load_checkers(fake_mongo):
    collection = fake_mongo['db']['checkers']

    documents = [{
            '_id': 1,
            'checker_type': 2,
            'delivery_type': 1,
            'subscription_type': 1,
            'ticker': 'AAPL',
            'subscriber': 1,
        },
        {
            '_id': 2,
            'checker_type': 1,
            'delivery_type': 1,
            'subscription_type': 2,
            'ticker': 'AAPL',
            'subscriber': [1, 2],
    }]

    collection.insert_many(documents)

    assert super_len(collection.find({})) == 2

    checkers = load_checkers(collection)

    assert isinstance(checkers[0], GrowthChecker)
    assert isinstance(checkers[1], EverydayChecker)

    assert isinstance(checkers[0].subscription, IndividualSubscription)
    assert isinstance(checkers[1].subscription, GroupSubscription)

    assert isinstance(checkers[0].ticker, Ticker)
    assert isinstance(checkers[1].subscription.ticker, Ticker)
    assert checkers[0].ticker.__str__ == 'AAPL' and checkers[1].ticker.__str__ == 'AAPL'

    assert isinstance(checkers[0].subscription.subscriber, int)
    assert isinstance(checkers[1].subscription.subscriber, list)
