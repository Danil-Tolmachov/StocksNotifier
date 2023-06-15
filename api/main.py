from fastapi import APIRouter
import uvicorn

from database.db import engine
from database.models import Base


Base.metadata.create_all(engine)
app = APIRouter()


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
