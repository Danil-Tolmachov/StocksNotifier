from celery import Celery
from dotenv import load_dotenv
import os


load_dotenv('.env')

checkers = []
checkers_to_append = []


broker = os.environ['CELERY_BROKER']
result_backend = 'redis://localhost:6379/0'


# Initiate celery app
app = Celery('tasks', 
             broker=broker,
             backend=result_backend,
             broker_connection_retry=False,
             broker_connection_retry_on_startup=True,
             broker_connection_max_retries=10,
        )

app.conf.event_serializer = 'pickle'
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']
app.autodiscover_tasks()
