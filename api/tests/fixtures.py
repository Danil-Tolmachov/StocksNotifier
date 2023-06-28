import sys
import os.path
sys.path.append(os.path.curdir.split('api')[0])

import pytest
from mongomock import MongoClient

from event_loop.tasks import initiate_settings
from services.tickers import Ticker
from services.subscriptions import IndividualSubscription, GroupSubscription
from services.delivery import EmailDelivery, TestDelivery
from services.checkers import EverydayChecker, GrowthChecker, DropChecker


#
# Run pytest from 'api' directory
#
# Example:
# PS C:\Users\user\Desktop\InfoStocksAPI\api> pytest
#

@pytest.fixture
def get_subscription():
    return IndividualSubscription(Ticker('AAPL'))

@pytest.fixture
def get_checker(get_subscription):
    sub =get_subscription
    sub.subscribe(1)
    sub.delivery = TestDelivery()
    checker = EverydayChecker.create(sub)
    return checker


@pytest.fixture
def subscriptions_list():
    subs = [
            IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 1),
            IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 2),
            GroupSubscription(Ticker('AAPL'), EmailDelivery(), [3,]),
            GroupSubscription(Ticker('AAPL'), EmailDelivery(), [1, 3])
        ]
    return subs

@pytest.fixture
def checkers_list(mocker, subscriptions_list):
    mocker.patch('services.tickers.Ticker.get_price', return_value=110.5)
    checkers = [
                EverydayChecker(subscriptions_list[0]),
                GrowthChecker(subscriptions_list[1]),
                DropChecker(subscriptions_list[2]),
            ]
    return checkers

@pytest.fixture(scope='function')
def fake_mongo():
    return MongoClient()


@pytest.fixture(scope='function')
def initiated_db(fake_mongo):
    db = fake_mongo['db']

    checker_types = [
    {
        'id': 1,
        'class': 'EverydayChecker',
    },
    {
        'id': 2,
        'class': 'GrowthChecker',
    },
    {
        'id': 3,
        'class': 'DropChecker',
    },
    ]

    delivery_types = [
        {
            'id': 1,
            'class': 'EmailDelivery',
        },
    ]

    subscription_types = [
        {
            'id': 1,
            'class': 'IndividualSubscription',
        },
        {
            'id': 2,
            'class': 'GroupSubscription',
        },
    ]

    checker_collection = db['checker_types']
    delivery_collection = db['delivery_types']
    subscription_collection = db['subsctiption_types']
    checker_instances = db['checkers']

    checker_collection.insert_many(checker_types)
    subscription_collection.insert_many(subscription_types)
    delivery_collection.insert_many(delivery_types)

