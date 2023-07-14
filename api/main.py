from fastapi import FastAPI
import uvicorn

from routes.v1 import auth
import settings


api = FastAPI()

api.include_router(auth.router)



if __name__ == '__main__':
    uvicorn.run('main:api', reload=True)
