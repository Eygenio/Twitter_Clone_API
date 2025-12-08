from typing import Any, Generic, Type, TypeVar, List, Optional, NoReturn
from sqlalchemy import insert, delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.exceptions.db import handle_db_error

ModelType = TypeVar("ModelType")


class SQLAlchemyRepository(Generic[ModelType]):
    """Базовый класс с CRUD операциями для SQLAlchemy."""
    model: Type[ModelType] = None

    def __init__(self, session: AsyncSession):
        # инициализация класса с сессиями базы данных
        self.session = session

    async def add_one(self, data: dict) -> int:
        """Добавление одной записи с возвратом id."""
        statement = insert(self.model).values(**data).returning(self.model.id)

        try:
            result = await self.session.execute(statement)
            await self.session.commit()
            return result.scalar_one()
        except Exception as exc:
            raise handle_db_error(exc)

    async def add_one_no_return(self, data: dict):
        """Добавление одной записи без возврата результата."""
        statement = insert(self.model).values(**data)

        try:
            await self.session.execute(statement)
            await self.session.commit()
        except Exception as exc:
            handle_db_error(exc)

    async def delete_one_by_id(self, data_id: int):
        """Удаление одной записи по id без возврата результата."""
        statement = delete(self.model).where(self.model.id == data_id)

        try:
            await self.session.execute(statement)
            await self.session.commit()
        except Exception as exc:
            handle_db_error(exc)

    async def delete_one_no_return(self, data: dict):
        """Удаление одной записи по фильтру без возврата результата."""
        statement = delete(self.model).filter_by(**data)

        try:
            await self.session.execute(statement)
            await self.session.commit()
        except Exception as exc:
            handle_db_error(exc)

    async def find_all(
        self,
        relations: Optional[List[Any]] = None,
            offset: int = 0,
            limit: int = 100
    ) -> Optional[ModelType]:
        """Получение всех записей с загрузкой связанных данных с поддержкой пагинации."""
        statement = (
            select(self.model)
            .offset(offset)
            .limit(limit)
        )

        if relations:
            for relation in relations:
                statement = statement.options(selectinload(relation))

        try:
            result = await self.session.execute(statement)
            return result.scalars().all()
        except Exception as exc:
            raise handle_db_error(exc)

    async def find_one(
        self,
        data_id: int,
        relations: Optional[list[Any]] = None
    ) -> Optional[ModelType]:
        """Получение одной записи с загрузкой связанных данных по id."""
        statement = select(self.model).where(self.model.id == data_id)

        if relations:
            for relation in relations:
                statement = statement.options(selectinload(relation))

        try:
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as exc:
            raise handle_db_error(exc)

    async def find_one_api_key(
        self,
        api_key: str,
        relations: Optional[list[Any]] = None
    ) -> Optional[ModelType]:
        """Получение одной записи с загрузкой связанных данных по api_key."""
        statement = select(self.model).where(self.model.api_key == api_key)

        if relations:
            for relation in relations:
                statement = statement.options(selectinload(relation))

        try:
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()
        except Exception as exc:
            raise handle_db_error(exc)

    async def get_user_by_list(self, user_id_list: list[int]):
        """Получение списка записей по списку id."""
        statement = (
            select(self.model)
            .where(self.model.id.in_(user_id_list))
        )

        try:
            result = await self.session.execute(statement)
            return result.scalars().all()
        except Exception as exc:
            raise handle_db_error(exc)
