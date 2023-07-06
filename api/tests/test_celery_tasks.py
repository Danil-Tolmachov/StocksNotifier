from datetime import datetime
import pytest
from fixtures import fake_mongo, initiated_db, subscriptions_list
from freezegun import freeze_time

from task_manager.tasks import init_checkers, save_new_checker, load_checker
from task_manager.utils import super_len
from services.delivery import EmailDelivery
from services.tickers import Ticker
from services.checkers import EverydayChecker, GrowthChecker
from services.subscriptions import IndividualSubscription, GroupSubscription


@pytest.mark.asyncio
async def test_init_checkers(fake_mongo, subscriptions_list, initiated_db):
    collection = fake_mongo['db']['checkers']

    docs = [
        {   
           'id': 1, 
           'checker_type': 2, 
           'checker_dict': {'last_price': 110.5}, 
           'delivery_type': 1, 
           'subscription_type': 1, 
           'subscription_dict': {'_AbstractSubscription__subscriber': 2}, 
           'ticker': 'AAPL', 
           'subscriber': 2, 
           'active': True
        },
        {
           'id': 2, 
           'checker_type': 1, 
           'checker_dict': {'delivery_date': datetime(2023, 6, 29, 20, 20, 55)}, 
           'delivery_type': 1, 
           'subscription_type': 2, 
           'subscription_dict': {'_AbstractSubscription__subscriber': [2,3]}, 
           'ticker': 'AAPL', 
           'subscriber': [2,3], 
           'active': True
        }]
    
    collection.insert_many(docs)
    cursor = collection.find({})[1]

    assert super_len(collection.find({})) == 2

    checkers = init_checkers(collection)

    assert isinstance(checkers[0], GrowthChecker)
    assert isinstance(checkers[1], EverydayChecker)

    assert isinstance(checkers[0].subscription, IndividualSubscription)
    assert isinstance(checkers[1].subscription, GroupSubscription)

    assert isinstance(checkers[0].ticker, Ticker)
    assert isinstance(checkers[1].subscription.ticker, Ticker)
    assert checkers[0].ticker.__str__() == 'AAPL'
    assert checkers[1].ticker.__str__() == 'AAPL'

    assert isinstance(checkers[0].subscription.subscriber, int)
    assert isinstance(checkers[1].subscription.subscriber, list)


@pytest.mark.asyncio
async def test_load_checker(fake_mongo, initiated_db):
    db = fake_mongo['db']
    collection = db['checkers']

    assert super_len(collection.find({})) == 0

    sub = IndividualSubscription(Ticker('AAPL'), EmailDelivery, 2)
    sub.delivery = EmailDelivery()
    checker = EverydayChecker(sub)

    save_new_checker(collection, checker)
    assert super_len(collection.find({})) == 1

    raw_checker = collection.find({})[0]
    result = load_checker(raw_checker)

    assert isinstance(result, EverydayChecker)
    assert isinstance(result.subscription, IndividualSubscription)
    assert isinstance(result.subscription.delivery, EmailDelivery)
    assert isinstance(result.ticker, Ticker)


@pytest.mark.asyncio
@freeze_time('2023-06-28 20:20:55')
async def test_save_new_checker(fake_mongo, initiated_db):
    db = fake_mongo['db']
    collection = db['checkers']

    assert super_len(collection.find({})) == 0

    sub = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 2)
    sub.delivery = EmailDelivery()
    checker = EverydayChecker(sub)
    checker.update()

    save_new_checker(collection, checker)
    assert super_len(collection.find({})) == 1

    db_obj: dict = collection.find({})[0]

    expected = {
        'id': 1,
        'checker_type': 1,
        'checker_dict': {'delivery_date': datetime(2023, 6, 28, 20, 22, 55)},
        'delivery_type': 1,
        'subscription_type': 1,
        'subscription_dict': {'_AbstractSubscription__subscriber': 2},
        'ticker': 'AAPL',
        'subscriber': 2,
        'active': True,
    }
