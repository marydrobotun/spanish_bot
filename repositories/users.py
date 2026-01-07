from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from db.models import User


class UserRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_language(self, user_id: int) -> str:
        async with self.session_factory() as session:
            result = await session.execute(
                select(User.language).where(User.id == user_id)
            )
            return result.scalar_one_or_none() or "ru"

    async def create_if_not_exists(self, user_id: int):
        async with self.session_factory() as session:
            stmt = insert(User).values(id=user_id)
            stmt = stmt.on_conflict_do_nothing(index_elements=[User.id])
            await session.execute(stmt)
            await session.commit()
