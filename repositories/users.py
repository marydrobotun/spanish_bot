from sqlalchemy import select
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
            session.add(User(id=user_id))
            await session.commit()
