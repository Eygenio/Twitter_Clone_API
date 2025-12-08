from src.celery_app import celery_app
import logging

logger = logging.getLogger("src.tasks.notifications")


@celery_app.task(name="tasks.send_follow_notification", bind=True, acks_late=True)
def send_follow_notification(self, follower_id: int, followed_id: int, request_id: str | None = None ):
    """
    Пример реальной 'Таски': уведомление о подписке.
    Здесь пока только логируем - в реальном приложении можно отправлять push/email.
    """
    logger.info(f"[{request_id}] Task send_follow_notification: {follower_id} -> {followed_id}")
    #  Место для реальной логики (email/push)
    return {"follower_id": follower_id, "followed_id": followed_id, "status": "notified"}


@celery_app.task(name="tasks.add_number", bind=True, acks_late=True)
def add_number(self, a:int, b: int):
    """
    Простейшая тестовая 'Таска' - складывает два числа.
    Используется для проверки, что worker обрабатывает задачи.
    """
    result = a + b
    logger.info(f"add_number: {a} + {b} = {result}")
    return result
