import sys
import os.path
sys.path.append(os.path.curdir.split('api')[0])

import pytest
from mongomock import MongoClient

from services.tickers import Ticker
from services.subscriptions import IndividualSubscription, GroupSubscription
from services.delivery import EmailDelivery
from services.checkers import EverydayChecker, GrowthChecker, DropChecker


#
# Run pytest from 'api' directory
#
# Example:
# PS C:\Users\user\Desktop\InfoStocksAPI\api> pytest
#

@pytest.fixture
def get_subscription():
    return IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 1)

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

@pytest.fixture
def fake_mongo():
    return MongoClient()

