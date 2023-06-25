import pytest
from freezegun import freeze_time

from services.checkers import DropChecker, GrowthChecker, EverydayChecker
from services.subscriptions import IndividualSubscription
from services.delivery import EmailDelivery
from services.abstractions import AbstractChecker
from services.tickers import Ticker


@pytest.mark.asyncio
@freeze_time('2023-06-24 7:30:53')
async def test_everyday_checker():
    # Create checker
    sub = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), id=4)
    checker = await EverydayChecker.create(sub)

    assert isinstance(checker, AbstractChecker)
    assert await checker.check() == False

    with freeze_time('2023-06-25 12:30:53'):
        assert await checker.check() == True
        checker.update()
        assert await checker.check() == False


@pytest.mark.asyncio
@freeze_time('2023-06-24 12:30:53')
async def test_drop_checker(mocker):
    # Create checker
    sub = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), id=4)
    checker = await DropChecker.create(sub)

    assert isinstance(checker, AbstractChecker)
    assert await checker.check() == False
    
    mocker.patch('services.tickers.Ticker.get_price', return_value=110.5)
    await checker.update()
    
    # Growth/Delay check
    assert await checker.check() == False
    mocker.patch('services.tickers.Ticker.get_price', return_value=150.5)
    await checker.update()
    assert await checker.check() == False

    # Delay check
    with freeze_time('2023-06-24 22:31:00'):
        mocker.patch('services.tickers.Ticker.get_price', return_value=50.5)
        assert await checker.check() == True
        await checker.update()
        assert await checker.check() == False


@pytest.mark.asyncio
@freeze_time('2023-06-24 12:30:53')
async def test_growth_checker(mocker):
    sub = IndividualSubscription(Ticker('AAPL'), EmailDelivery(), 4)

    checker = await GrowthChecker.create(sub)
    assert isinstance(checker, AbstractChecker)
    assert await checker.check() == False
    
    mocker.patch('services.tickers.Ticker.get_price', return_value=110.5)
    await checker.update()
    
    # Growth/Delay check
    assert await checker.check() == False
    mocker.patch('services.tickers.Ticker.get_price', return_value=150.5)
    await checker.update()
    assert await checker.check() == False

    # Delay check
    with freeze_time('2023-06-24 22:31:00'):
        mocker.patch('services.tickers.Ticker.get_price', return_value=200.5)
        assert await checker.check() == True
        await checker.update()
        assert await checker.check() == False
