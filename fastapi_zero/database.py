from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from fastapi_zero.settings import settings


engine = create_async_engine(settings.DATABASE_URL)


async def get_session():
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
