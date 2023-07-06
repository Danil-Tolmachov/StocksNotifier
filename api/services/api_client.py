from abc import ABC, abstractmethod
from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPNotFound
import ujson
import os

from services.abstractions import AbstractTicker



class AbstractAPIClient(ABC):
    _instance = None
    URL = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @abstractmethod
    def get_api_token() -> str:
        pass

    @abstractmethod
    async def ticker_list(self) -> dict:
        pass

    @abstractmethod
    async def ticker_details(self, ticker: str) -> dict:
        pass


class PolygonIoClient(AbstractAPIClient):
    URL = 'https://api.polygon.io/'
    
    def get_api_token(self) -> str:
        api_key = os.environ['POLYGONIO_API_KEY']
        return api_key
    

    async def ticker_list(self, ticker: AbstractTicker, session: ClientSession):
        query = f'?apiKey={self.get_api_token()}'
        request = self.URL + 'v3/reference/tickers/' + query

        async with session.get(request) as response:

            if response.status == 404:
                raise HTTPNotFound()
            
            return ujson.loads(await response.text())
        

    async def ticker_details(self, ticker: AbstractTicker, session: ClientSession):
        query = f'?apiKey={self.get_api_token()}'
        request = self.URL + 'v3/reference/tickers/' + ticker.ticker + query

        async with session.get(request) as response:
            
            if response.status == 404:
                raise HTTPNotFound()
            
            if response.status >= 500:
                raise Exception('API client works improperly')
            
            return ujson.loads(await response.text())
        
    async def ticker_price(self, ticker: AbstractTicker, session: ClientSession, type: str = 'c') -> float:
        query = f'?apiKey={self.get_api_token()}' 
        request = self.URL + f'v2/aggs/ticker/{ticker.ticker}/prev/' + query

        async with session.get(request) as response:
            
            if response.status == 404:
                raise HTTPNotFound()
            
            if response.status >= 500:
                raise Exception('API client works improperly')
            
            results = ujson.loads(await response.text())['results']
            return results[0][type]
