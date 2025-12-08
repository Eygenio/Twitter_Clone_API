from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session
from src.repositories.users import UserRepository
from src.models.users import UserOrm


async def get_current_user(
        api_key: str = Header(...),
        session: AsyncSession = Depends(get_async_session)
) -> UserOrm:
    """
    Проверка соответствия api_key пользователю.
    """
    repositories = UserRepository(session)
    user = await repositories.find_one_api_key(api_key)

    if not user: raise HTTPException(
        status_code=401,
        detail="Invalid or missing API key"
    )
    return user
