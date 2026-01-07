from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT")

DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
print(DB_URL)
engine = create_async_engine(
    DB_URL,
    echo=False
)

SessionFactory = async_sessionmaker(
    engine,
    expire_on_commit=False
)
