from dotenv import load_dotenv
import os
from datetime import datetime
import uuid
from collections.abc import AsyncGenerator

from sqlalchemy import Column, Integer, String, Boolean, PickleType, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     caption = Column(Text)
#     url = Column(String, nullable=False)
#     file_type = Column(String, nullable=False)
#     file_name = Column(String, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

class Question(Base):
    __tablename__ = "question"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    complexity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    options = Column(String)
    correct_answers = Column(ARRAY(String))
    max_score = Column(Integer, default=1)

class Examination(Base):
    __tablename__ = "examination"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    duration = Column(Integer, default=1)
    ques_list = Column(ARRAY(String))

class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    disabled = Column(Boolean, nullable=True)
    
    
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # False in production
    future=True
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def create_db_and_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
