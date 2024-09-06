from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
import os

# Replace with your actual database URL
DATABASE_URL = os.getenv("DATABASE_URL")
# Create the asynchronous engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)


# Initialize the database schema
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# Get an asynchronous session
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, future=True
    )
    async with async_session() as session:
        yield session


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
