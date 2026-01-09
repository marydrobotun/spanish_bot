from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from redis.asyncio import Redis

from repositories.users import UserRepository


class UserLanguageMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, user_repo: UserRepository):
        self.redis = redis
        self.user_repo = user_repo

    async def __call__(self, handler, event: TelegramObject, data: dict):
        user = data.get('event_from_user')
        if not user:
            return await handler(event, data)
        user_id = user.id
        cache_key = f'user:{user_id}:lang'
        lang = await self.redis.get(cache_key)
        if not lang:
            await self.user_repo.create_if_not_exists(user_id)
            lang = await self.user_repo.get_language(user_id)
            await self.redis.set(cache_key, lang)

        data['lang'] = lang
        return await handler(event, data)
