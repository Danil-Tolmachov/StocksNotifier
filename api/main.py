from fastapi import APIRouter
import uvicorn


router = APIRouter()


if __name__ == '__main__':
    uvicorn.run('main:router', reload=True)
