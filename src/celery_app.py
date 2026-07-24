from celery import Celery

from src.config.settings import settings

celery_app = Celery(
    "twitter_clone",
    broker=settings.broker.url,
    backend=settings.broker.result_backend,
)

celery_app.conf.update(
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    task_time_limit=30 * 60,
)
