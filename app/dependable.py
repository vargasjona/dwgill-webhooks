from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.engine import engine


async def database_session():
    async with AsyncSession(engine) as session:
        yield session


DatabaseSession = Annotated[AsyncSession, Depends(database_session)]
UniqueDatabaseSession = Annotated[
    AsyncSession, Depends(database_session, use_cache=False)
]


async def database_transaction(session: UniqueDatabaseSession):
    async with session.begin():
        yield session


DatabaseTransaction = Annotated[AsyncSession, Depends(database_transaction)]
UniqueDatabaseTransaction = Annotated[
    AsyncSession, Depends(database_transaction, use_cache=False)
]
