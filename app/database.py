from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

"""Database initialization module.

Uses async SQLAlchemy engine pointing at the configured DATABASE_URL. Previous
code referenced settings.DB_URL which no longer exists after the refactor to
granular DB_* env vars; this updates to use settings.DATABASE_URL property.
"""

engine = create_async_engine(settings.DATABASE_URL, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    """FastAPI dependency providing an async DB session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
