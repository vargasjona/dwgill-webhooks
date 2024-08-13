from fastapi import FastAPI
from sqlmodel import select
from app.db.models import Client
from app.dependable import DatabaseSession

app = FastAPI()


@app.get("/")
async def read_root(session: DatabaseSession):
    result = await session.exec(select(Client))
    return result.all()
