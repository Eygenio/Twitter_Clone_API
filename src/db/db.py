import logging

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config.settings import settings
from src.infrastructure.models import ModelBase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

engine = create_async_engine(settings.db.database_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(ModelBase.metadata.create_all)
