from celery import Celery
from dotenv import load_dotenv

from settings import settings


load_dotenv('.env')

checkers = []
checkers_to_append = []


broker = settings.CELERY_BROKER
result_backend = settings.RESULT_BACKEND


# Initiate celery app
app = Celery('tasks', 
             broker=broker,
             backend=result_backend,
             broker_connection_retry=False,
             broker_connection_retry_on_startup=True,
             broker_connection_max_retries=10,
             settings='celeryapp'
        )
app.autodiscover_tasks()
