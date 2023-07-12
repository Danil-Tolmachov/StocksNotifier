from typing import Optional
from pydantic import BaseSettings

from services.api_client import PolygonIoClient



class Settings(BaseSettings):

    # Cryptography
    SECRET_KEY: str

    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int

    # Third-party api
    DATA_API_CLIENT = PolygonIoClient

    # Email template
    DEFAULT_EMAIL_TEMPLATE: Optional[str]

    # MongoDB
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_URL: str

    # RabbitMQ - message broker
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_URL: str


    class Config:
        env_file = '.env'


settings = Settings()


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
