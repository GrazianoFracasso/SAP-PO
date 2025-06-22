from typing import Optional, Dict
from datetime import datetime
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text
from sqlalchemy.sql import select
from pydantic import BaseModel, Field
import json

# --- Configurazione DB ---
STATUS_DATABASE_URL = "sqlite+aiosqlite:///./status_store.db"
status_engine = create_async_engine(STATUS_DATABASE_URL, echo=False)
SessionLocal = async_sessionmaker(status_engine, expire_on_commit=False)


# --- Modello ORM ---
class Base(DeclarativeBase): pass

class StatusRecord(Base):
    __tablename__ = "extract_status"
    procedure_name: Mapped[str] = mapped_column(String, primary_key=True)
    status_json: Mapped[str] = mapped_column(Text)

# --- Modello Pydantic ---
class StatusModel(BaseModel):
    running: bool
    completed_at: Optional[datetime] = None
    processed: int = 0
    total: int = 0
    result: Optional[dict] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

async def init_models():
    async with status_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

# --- Inizializzazione DB ---
async def init_db():
    async with status_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Accesso asincrono ---
async def get_status(procedure_name_: str) -> Optional[StatusModel]:
    async with SessionLocal() as session:
        stmt = select(StatusRecord).where(StatusRecord.procedure_name == procedure_name_)
        result = await session.execute(stmt)
        record = result.scalar_one_or_none()
        if record:
            return StatusModel(**json.loads(record.status_json))
        return None

async def set_status(procedure_name_: str, status: StatusModel) -> None:
    async with SessionLocal() as session:

        #status = StatusModel(**status)
        status_json = status.model_dump_json()
        existing = await session.get(StatusRecord, procedure_name_)
        if existing:
            existing.status_json = status_json
        else:
            existing = StatusRecord(procedure_name=procedure_name_, status_json=status_json)
            session.add(existing)
        await session.commit()

async def get_all_procedures() -> list:
    async with SessionLocal() as session:
        stmt = select(StatusRecord.procedure_name)
        result = await session.execute(stmt)
        return [row[0] for row in result.all()]
