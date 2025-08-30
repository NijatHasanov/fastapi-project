from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_async_engine(settings.DB_URL)
async_session = sessionmaker(engine, class_=AsyncSession)
Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
