from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError
from src.exceptions.exceptions import AlreadyExistsError, ValidationError


def handle_db_error(exc: Exception):
    if isinstance(exc, UniqueViolationError):
        raise AlreadyExistsError("Unique constraint violated")

    if isinstance(exc, IntegrityError):
        raise ValidationError("Integrity error")

    raise exc
