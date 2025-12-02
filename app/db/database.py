"""
Database connection and session management.
Uses SQLAlchemy with SQLite for simplicity.
"""

import os
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import event

from app.config import settings


# Ensure data directory exists
db_path = Path(settings.database_path)
db_path.parent.mkdir(parents=True, exist_ok=True)

# Create async engine for SQLite (using aiosqlite)
DATABASE_URL = f"sqlite+aiosqlite:///{settings.database_path}"

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,  # Log SQL queries in debug mode
    connect_args={"check_same_thread": False}  # Required for SQLite
)

# Session factory for creating database sessions
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session.
    Automatically closes the session after the request.
    
    Usage in FastAPI:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    Initialize database: create tables.
    Call this on application startup.
    """
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """
    Close database connections.
    Call this on application shutdown.
    """
    await engine.dispose()
