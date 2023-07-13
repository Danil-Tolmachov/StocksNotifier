from fastapi import FastAPI
import uvicorn

import settings
from routes.v1 import auth

api = FastAPI()

api.include_router(auth.router)


@api.get('/test')
def test():
    return 'success'


if __name__ == '__main__':
    uvicorn.run('main:api', reload=True)
