from aiohttp import ClientSession

from services.abstractions import AbstractTicker
from settings import settings


class Ticker(AbstractTicker):
    async def get_price(self, session: ClientSession, type: str = 'c'):
        client = settings.get_api_client()()
        price = await client.ticker_price(self, session, type)
        return price
        
