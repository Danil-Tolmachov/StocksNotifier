import pytest
from aiohttp import ClientSession

from services.tickers import Ticker


@pytest.mark.asyncio
@pytest.mark.skip
async def test_get_ticker_price():
    ticker = Ticker('AAPL')
    
    async with ClientSession() as session:
        price = await ticker.get_price(session)
        assert isinstance(await ticker.get_price(session), float)
