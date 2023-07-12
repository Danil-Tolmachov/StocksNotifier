from fastapi import FastAPI
import uvicorn


import settings
api = FastAPI()


if __name__ == '__main__':
    uvicorn.run('main:router', reload=True)
