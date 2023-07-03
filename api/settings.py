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

MONGO_USER = env('MONGO_USER')
MONGO_PASSWORD = env('MONGO_PASSWORD')

# RabbitMQ - message broker
RABBITMQ_USER = env('RABBITMQ_USER')
RABBITMQ_PASS = env('RABBITMQ_PASS')
RABBIT_MQ_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@localhost/'


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
