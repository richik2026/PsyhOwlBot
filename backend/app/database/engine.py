import os

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


DATABASE_URL = os.getenv("DATABASE_URL")


engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
)
