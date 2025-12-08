"""
Скрипт заполнения базы данных данными для тестирования.
Запуск: python scripts/seed_db.py
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import insert, select
from src.config.base import Config
from src.models.base import ModelBase
from src.models.users import UserOrm
from src.models.tweets import TweetOrm
from src.models.medias import MediaOrm

DATABASE_URL = Config.DATABASE_URL


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    try:
        # Проверяем подключение к БД
        async with engine.connect() as conn:
            await conn.execute(select(1))

        async with async_session() as session:
            # Проверяем, есть ли уже пользователи
            existing_users = await session.execute(select(UserOrm).limit(1))
            if existing_users.scalar_one_or_none():
                print("Database already has data, skipping seed")
                return

            print("Starting database seeding")

            # Добавим пользователей (добавляем без ID - база данных сама сгенерирует)
            users_data = [
                {"name": "user", "api_key": "test"},
                {"name": "user_2", "api_key": "test_2"},
                {"name": "user_3", "api_key": "test_3"},
            ]

            result = await session.execute(
                insert(UserOrm).returning(UserOrm.id),
                users_data
            )
            user_ids = result.scalars().all()
            print(f"Added users with ID: {user_ids}")

            # Добавим медиа
            medias_data = [
                {"path": "/media/cat_1.png"},
                {"path": "/media/cat_2.png"},
                {"path": "/media/cat_3.png"},
                {"path": "/media/cat_4.png"},
                {"path": "/media/cat_5.png"},
            ]

            result = await session.execute(
                insert(MediaOrm).returning(MediaOrm.id),
                medias_data
            )
            media_ids = result.scalars().all()
            print(f"Added media with IDs: {media_ids}")

            # Добавим твиты
            tweets_data = [
                {"content": "Hello world!", "author_id": user_ids[0], "medias_id": []},
                {"content": "Another tweet", "author_id": user_ids[1], "medias_id": [media_ids[0]]},
                {"content": "Tweet with media!", "author_id": user_ids[2], "medias_id": [media_ids[1]]},
                {"content": "Media tweet!", "author_id": user_ids[0], "medias_id": [media_ids[2]]},
                {"content": "Text tweet", "author_id": user_ids[1], "medias_id": []},
                {"content": "Cat tweet", "author_id": user_ids[1], "medias_id": [media_ids[3]]},
                {"content": "Cat media tweet", "author_id": user_ids[2], "medias_id": [media_ids[4]]},
                {"content": "The end!", "author_id": user_ids[2], "medias_id": []},
            ]

            result = await session.execute(
                insert(TweetOrm).returning(TweetOrm.id),
                tweets_data
            )
            tweet_ids = result.scalars().all()
            print(f"Added tweets with ID: {tweet_ids}")

            await session.commit()
            print("✅ Database seeded successfully!")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed())
