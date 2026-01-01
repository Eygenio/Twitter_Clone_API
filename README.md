# 🐦 Twitter Clone API v1.0.0 — FastAPI + Celery + RabbitMQ + PostgreSQL + Nginx

Высокопроизводительное backend-приложение, реализующее ключевой функционал Twitter: пользователи, посты, лайки, подписки, фоновые задачи.

> ⚠️ Проект реализован **только в части backend**.  
> Frontend предоставлен готовым и использовался для интеграции и тестирования API.

---

## ✨ Возможности

* 📝 Создание постов и ленты новостей
* ❤️ Лайки и статистика постов
* 🔔 Подписки (followers / following)
* ⚙️ Фоновые задачи Celery (уведомления, обработка задач)
* 🐇 RabbitMQ в качестве брокера
*  🗄 PostgreSQL
* 🌐 Nginx для раздачи статики и проксирования
* 🐳 Полная поддержка Docker + docker-compose
* 📡 Swagger UI

---

## 🏗️ Архитектура проекта

Архитектура построена по принципу:
Routing → Service → Repository

```
app/
 ├── alembic/
 │    ├── env.py
 │    └── script.py.mako
 ├── dist/
 ├── media/
 ├── nginx/
 │    └── nginx.conf
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
* Nginx
* Docker + docker-compose
* API-key authentication (FastAPI dependencies)
* Pytest
* SQLAlchemy 2.0 (async)
* Repository Pattern

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
git clone https://github.com/Eygenio/Twitter_Clone_API
```

## 2. Создать `.env` или скопируйте содержимое `.env.template` в `.env`

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

## 3. 🐳 Сборка через Docker

```bash
docker-compose build
```

## 4. 🐳 Запуск через Docker

```bash
docker-compose up -d
```

## 🔗 Доступ к сервису

```bash
http://0.0.0.0:8080/ 
```

## 🔗 Доступ к документации

```bash
http://0.0.0.0:8080/docs/
```

---

# 📦 Структура PostgreSQL

### `users`

* id
* name
* api_key

### `tweets`

* id
* user_id
* content
* created_at

### `followers`

* follower_id
* following_id

---

# 🔐 Безопасность

* Аутентификация через API-key (HTTP Header)
* PostgreSQL изолирован Docker'ом
* Минимум привилегий

---
