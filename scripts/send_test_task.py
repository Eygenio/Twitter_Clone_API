"""
Скрипт отправки тестовых задач в celery broker.
Запуск: scripts/send_test_task.py
"""
from src.celery_app import celery_app
import time


def send_task():
    res = celery_app.send_task("tasks.add_number", args=(2, 3))
    print("Sent tasks.add_number, task id:", res.id)

    res2 = celery_app.send_task("tasks.send_follow_notification", args=(1, 2, "test-request-id"))
    print("Sent tasks.send_follow_notification, task id:", res2.id)

    time.sleep(1)
    print("Tasks sent.")


if __name__ == "__main__":
    send_task()
