from dotenv import load_dotenv
import os

from services.api_client import PolygonIoClient


# Environment setup
def env(var: str):
    try:
        return os.environ[var]
    except KeyError:
        return None


load_dotenv('.env')


# Variables
DATA_API_CLIENT = PolygonIoClient # AbstractAPIClient

DEFAULT_EMAIL_TEMPLATE = None

DATABASE_URL = env('DATABASE_URL')
DATABASE_HOST = env('DATABASE_HOST')
DATABASE_PORT = env('DATABASE_PORT')
DATABASE_NAME = env('DATABASE_NAME')
DATABASE_USER = env('DATABASE_USER')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')


# Mongo Structure / Active classes
#
# WARNING: Sensitive settings
# Users might loose their checkers if you delete/move or change it. 
#
checker_types = [
    {
        'id': 1,
        'class': 'EverydayChecker',
    },
    {
        'id': 2,
        'class': 'GrowthChecker',
    },
    {
        'id': 3,
        'class': 'DropChecker',
    },
]

delivery_types = [
    {
        'id': 1,
        'class': 'EmailDelivery',
    },
]

subscription_types = [
    {
        'id': 1,
        'class': 'IndividualSubscription',
    },
    {
        'id': 2,
        'class': 'GroupSubscription',
    },
]
