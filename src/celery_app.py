import os
from celery import Celery


BROKER = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@rabbitmq:5672//")
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "rpc://")

celery_app = Celery(
    "twitter_clone",
    broker=BROKER,
    backend=BACKEND,
)

celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=30 * 60,
)

from src.tasks import notifications
