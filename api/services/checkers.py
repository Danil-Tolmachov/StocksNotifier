from abc import ABC, abstractmethod
from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPNotFound
import settings
import ujson



class AbstractTiker(ABC):
    def __init__(self, tiker) -> None:
        super().__init__()
        self.tiker = tiker

    def __str__(self) -> str:
        return self.tiker

class Tiker(AbstractTiker):
    pass


class AbstractChecker(ABC):
    _instances = []

    def __new__(cls, tiker: AbstractTiker):

        for obj in cls._instances:
            if obj.target.tiker == tiker: # Change to obj
                return obj

        new_obj = super().__new__(cls)
        cls._instances.append(new_obj)
        return new_obj

    def __init__(self, target: AbstractTiker) -> None:
        super().__init__()
        self.target = target


class BaseChecker(AbstractChecker):
    pass



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
    async def tiker_list(self) -> dict:
        pass

    @abstractmethod
    async def tiker_details(self, tiker: str) -> dict:
        pass


class PolygonIoClient(AbstractAPIClient):
    URL = 'https://api.polygon.io/v3/'
    
    def get_api_token(self) -> str:
        return settings.POLYGONIO_API_KEY
    

    async def tiker_list(self, tiker: AbstractTiker, session: ClientSession):
        query = f'?apiKey={self.get_api_token()}'
        request = self.URL + 'reference/tickers/' + query

        async with session.get(request) as response:

            if response.status == 404:
                raise HTTPNotFound()
            
            return ujson.loads(await response.text())
        

    async def tiker_details(self, tiker: AbstractTiker, session: ClientSession):
        query = f'?apiKey={self.get_api_token()}'
        request = self.URL + 'reference/tickers/' + tiker.tiker + query

        async with session.get(request) as response:
            
            if response.status == 404:
                raise HTTPNotFound()
            
            return ujson.loads(await response.text())


# async def main():
#     cl1 = PolygonIoClient()
# 
#     async with ClientSession() as session:
#         print(await cl1.tiker_details(Tiker('AAPL'), session))
# 
# asyncio.run(main())
