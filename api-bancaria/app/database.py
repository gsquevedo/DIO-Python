from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

# URL de conexão utilizando o driver assíncrona 'aiosqlite'
DATABASE_URL = "sqlite+aiosqlite:///./banco_digital.db"

# Cria a engine de conexão assíncrona
engine = create_async_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

# Configura a fábrica de sessões assíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Classe base que nossos modelos de tabelas
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session