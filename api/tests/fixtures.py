import sys
import os.path
sys.path.append(os.path.curdir.split('api')[0])

import pytest

from services.tickers import Ticker
from services.subscriptions import IndividualSubscription, GroupSubscription
from services.delivery import EmailDelivery
from services.abstractions import AbstractChecker


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
    subs = []
    
    sub1 = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 1)
    sub2 = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 2)
    sub3 = GroupSubscription(Ticker('AAPL'), EmailDelivery(), [3,])
    sub4 = GroupSubscription(Ticker('AAPL'), EmailDelivery(), [1, 3])

    subs.extend([sub1, sub2, sub3, sub4])
    return subs

@pytest.fixture
def checkers_list(moker, subscriptions_list):
    checkers = {}

    moker.patch('Ticker.get_price', 120)

    for key, sub in enumerate(subscriptions_list):
        checkers.update(key, sub)

    return checkers
