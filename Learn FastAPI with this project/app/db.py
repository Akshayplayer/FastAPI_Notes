from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime

DATABASE_URL="sqlite+aiosqlite:///./test.db" # database url for sqlite database connection (aiosqlite it is an asynchronus version of sqlite)

# Defining data models and create the databases which will automatically create the datamodels for us.

class Base(DeclarativeBase):
    pass
class Post(Base):
    __tablename__ = "posts"

    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption=Column(Text)
    url=Column(String, nullable=False)
    file_type=Column(String, nullable=False)
    file_name=Column(String, nullable=False)
    created_at=Column(DateTime, default=datetime.utcnow)   


# create the database.
engine=create_async_engine(DATABASE_URL, echo=True)
async_session_maker=async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_tables(): # will create database and tables 
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) # it will find all the classes and create the tables defined with declarativebase


# This code defines an asynchronous function called get_async_session that returns an asynchronous generator. The generator yields an instance of AsyncSession, which is a session object for interacting with an asynchronous database. The function uses an async with statement to create a session using async_session_maker, and then yields that session. This allows the caller of the function to iterate over the generator and retrieve multiple sessions as needed.
async def get_async_session() -> AsyncGenerator[AsyncSession, None]: # will return the session
    async with async_session_maker() as session:
        yield session