from aiohttp import ClientSession

from services.abstractions import AbstractTicker
from settings import DATA_API_CLIENT


class Ticker(AbstractTicker):
    async def get_price(self, session: ClientSession, type: str = 'c'):
        client = DATA_API_CLIENT()
        price = await client.ticker_price(self, session, type)
        return price
        
