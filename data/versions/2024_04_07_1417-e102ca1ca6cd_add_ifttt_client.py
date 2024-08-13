"""Add IFTTT client

Revision ID: e102ca1ca6cd
Revises: 196ac29f1c21
Create Date: 2024-04-07 14:17:13.785060+00:00

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlmodel.sql.sqltypes
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.models import Client, ClientType
from sqlalchemy.ext.asyncio import AsyncConnection
import uuid

# revision identifiers, used by Alembic.
revision: str = "e102ca1ca6cd"
down_revision: Union[str, None] = "196ac29f1c21"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Reference: https://stackoverflow.com/a/24623979/11121928

def upgrade() -> None:
    async def handle_upgrade(async_connection: AsyncConnection):
        async with AsyncSession(async_connection) as session:
            client = Client(
                display_name="IFTTT",
                secret_hash="+iEC9kLgbooCVoHWXtH8sMWbUR1wo9KmCGPH3qvZei8=",
                secret_salt="fXv02YYlYPRK_jBmtAIW5VxcHH0",
                secret_version=1,
                public_id=uuid.UUID("9cc287d1-ac64-4cb6-997a-c54c70d10003"),
                client_type=ClientType.Webhook,
            )
            session.add(client)
            await session.commit()

    op.run_async(handle_upgrade)


def downgrade() -> None:
    async def handle_downgrade(async_connection: AsyncConnection):
        async with AsyncSession(async_connection) as session:
            client = await session.exec(
                sqlmodel.select(Client).where(
                    Client.public_id
                    == uuid.UUID("9cc287d1-ac64-4cb6-997a-c54c70d10003")
                )
            )
            await session.delete(client)
            await session.commit()

    op.run_async(handle_downgrade)
