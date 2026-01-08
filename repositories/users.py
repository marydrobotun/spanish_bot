from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from db.models import User
from settings import DEFAULT_LANGUAGE

class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_language(self, user_id: int) -> str:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User.language).where(User.id == user_id)
            )
            return result.scalar_one_or_none() or DEFAULT_LANGUAGE

    async def create_if_not_exists(self, user_id: int) -> None:
        async with self.session_factory() as session:
            stmt = insert(User).values(id=user_id)
            stmt = stmt.on_conflict_do_nothing(index_elements=[User.id])
            await session.execute(stmt)
            await session.commit()

    async def set_language(self, user_id: int, language: str) -> None:
        async with self.session_factory() as session:
            stmt = update(User).where(User.id == user_id).values(language=language)
            await session.execute(stmt)
            await session.commit()