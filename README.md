# 🐦 Twitter Clone API — FastAPI + Celery + RabbitMQ + PostgreSQL

Высокопроизводительное backend-приложение, реализующее ключевой функционал Twitter: пользователи, посты, лайки, подписки, фоновые задачи.

---

## ✨ Возможности

* 📝 Создание постов и ленты новостей
* ❤️ Лайки и статистика постов
* 🔔 Подписки (followers / following)
* ⚙️ Фоновые задачи Celery (уведомления, обработка задач)
* 🐇 RabbitMQ в качестве брокера
*  🗄 PostgreSQL
* 🐳 Полная поддержка Docker + docker-compose
* 📡 Swagger UI

---

## 🏗️ Архитектура проекта

```
app/
 ├── alembic/
 │    ├── env.py
 │    └── script.py.mako
 ├── dist/
 ├── media/
 ├── scripts/
 │    ├── __init__.py
 │    ├── seed_ddb.py
 │    ├── send_test_task.py
 │    └── wait-for-db.sh
 ├── src/
 │    ├── config/
 │    │    ├── base.py
 │    │    └── logging_config.py
 │    ├── db
 │    │    └── db.py
 │    ├── exceptions/
 │    │    ├── db.py
 │    │    └── exceptions.py
 │    ├── middleware/
 │    │    ├── error_handler.py
 │    │    └── request_id.py
 │    ├── models/
 │    │    ├── __init__.py
 │    │    ├── base.py
 │    │    ├── followers.py
 │    │    ├── likes.py
 │    │    ├── medias.py
 │    │    ├── tweets.py
 │    │    └── users.py
 │    ├── repositories/
 │    │    ├── base.py
 │    │    ├── followers.py
 │    │    ├── likes.py
 │    │    ├── medias.py
 │    │    ├── tweets.py
 │    │    └── users.py
 │    ├── routing/
 │    │    ├── followers.py
 │    │    ├── likes.py
 │    │    ├── medias.py
 │    │    ├── tweets.py
 │    │    └── users.py
 │    ├── schemas/
 │    │    ├── followers.py
 │    │    ├── likes.py
 │    │    ├── medias.py
 │    │    ├── tweets.py
 │    │    └── users.py
 │    ├── services/
 │    │    ├── followers.py
 │    │    ├── likes.py
 │    │    ├── medias.py
 │    │    ├── tweets.py
 │    │    └── users.py
 │    ├── tasks/
 │    │    └── notifications.py
 │    ├── app.py
 │    ├── celery_app.py
 │    └── dependencies.py
 ├── tests/
 │    ├── conftest.py
 │    ├── test_followers_service.py
 │    ├── test_likes_service.py
 │    ├── test_media_service.py
 │    └── test_tweets_service.py
 ├── .env
 ├── alembic.ini
 ├── docker-compose.yml
 ├── Dockerfile
 ├── pytest.ini
 ├── README.md
 └── requirements.txt
```

Технологии:

* FastAPI
* Celery 5
* RabbitMQ
* PostgreSQL
* Docker + docker-compose
* JWT Auth
* Pytest

---

## 💡 Функциональность

### 👤 Пользователи

* профиль
* подписки / отписки

### 📝 Посты

* создание
* получение
* лента
* лайки

### ⚙️ Celery-задачи

* отправка уведомлений
* тестовые задачи (send_test_task.py)

---

# 🚀 Запуск проекта (локально)

## 1. Клонировать репозиторий

```bash
git clone https://gitlab.skillbox.ru/evgenii_nemchenko_1/python_advanced_diploma.git
```

## 2. Установить зависимости

```bash
pip install -r requirements.txt
```

## 3. Создать `.env`

```
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=database
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND=rpc://
RABBIT_USER=guest
RABBIT_PASSWORD=guest
```

## 4. Запуск FastAPI

```bash
uvicorn src.main:app --reload
```

## 5. Запуск Celery

```bash
celery -A src.celery_app.celery_app worker --loglevel=info
```

---

# 🐳 Запуск через Docker

## 1. Сборка

```bash
docker-compose build
```

## 2. Запуск

```bash
docker-compose up -d
```


# 🎯 Тест Celery

```bash
python src/celery_app/send_test_task.py
```

---

# 📦 Структура PostgreSQL

### `users`

* id
* username
* email
* password
* created_at

### `posts`

* id
* user_id
* content
* created_at

### `followers`

* follower_id
* following_id

---

# 🔐 Безопасность

* JWT в заголовках
* PostgreSQL изолирован Docker'ом
* Минимум привилегий

---

# 📊 Отчет (coverage)

```
Name                              Stmts   Miss  Cover
-----------------------------------------------------
src/config/base.py                   13      0   100%
src/exceptions/db.py                  9      5    44%
src/exceptions/exceptions.py         19      0   100%
src/models/__init__.py                7      0   100%
src/models/base.py                    3      0   100%
src/models/followers.py               9      0   100%
src/models/likes.py                  12      0   100%
src/models/medias.py                  7      0   100%
src/models/tweets.py                 11      0   100%
src/models/users.py                  11      0   100%
src/repositories/base.py             76     59    22%
src/repositories/followers.py         4      0   100%
src/repositories/likes.py             4      0   100%
src/repositories/medias.py            4      0   100%
src/repositories/tweets.py            4      0   100%
src/repositories/users.py             4      0   100%
src/schemas/followers.py              3      0   100%
src/schemas/likes.py                  8      0   100%
src/schemas/medias.py                 8      0   100%
src/schemas/tweets.py                22      0   100%
src/schemas/users.py                 17      0   100%
src/services/followers.py            27      7    74%
src/services/likes.py                32      2    94%
src/services/medias.py               30      1    97%
src/services/tweets.py               68     20    71%
tests/conftest.py                     7      3    57%
tests/test_followers_service.py      23      0   100%
tests/test_likes_service.py          48      0   100%
tests/test_media_service.py          35      0   100%
tests/test_tweets_service.py         48      0   100%
-----------------------------------------------------
TOTAL                               573     97    83%
```