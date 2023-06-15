from dotenv import load_dotenv
import os

from services.checkers import PolygonIoClient

load_dotenv('.env')

POLYGONIO_API_KEY = 'AVodlDZT9tcJBX3dOgc1VEhPhepXEKKu'
DATA_API_CLIENT = PolygonIoClient

DATABASE_URL = os.environ('DATABASE_URL')
DATABASE_HOST = os.environ('DATABASE_HOST')
DATABASE_PORT = os.environ('DATABASE_PORT')
DATABASE_NAME = os.environ('DATABASE_NAME')
DATABASE_USER = os.environ('DATABASE_USER')
DATABASE_PASSWORD = os.environ('DATABASE_PASSWORD')
