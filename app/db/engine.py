from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
import env


def _create_engine() -> AsyncEngine:
    return create_async_engine(
        env.database_connection_string(),
        echo=True,
        future=True,
        pool_size=env.database_pool_size(),
        max_overflow=env.database_max_overflow(),
        pool_timeout=env.database_pool_timeout(),
    )


engine = _create_engine()
