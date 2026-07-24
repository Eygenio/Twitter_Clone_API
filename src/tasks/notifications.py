import logging
from typing import Any

from src.celery_app import celery_app

logger = logging.getLogger("src.tasks.notifications")


@celery_app.task(name="tasks.send_follow_notification", bind=True, acks_late=True)
def send_follow_notification(
    self,
    follower_id: int,
    followed_id: int,
    request_id: str | None = None,
) -> dict[str, Any]:
    logger.info(
        "[%s] Task send_follow_notification: %s -> %s", request_id, follower_id, followed_id
    )
    return {"follower_id": follower_id, "followed_id": followed_id, "status": "notified"}


@celery_app.task(name="tasks.add_number", bind=True, acks_late=True)
def add_number(self, a: int, b: int) -> int:
    result = a + b
    logger.info("add_number: %s + %s = %s", a, b, result)
    return result
