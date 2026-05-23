from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, bank

app = FastAPI(
    title="API Bancária Assíncrona",
    description="Desafio de API RESTful para depósitos, saques e extratos utilizando FastAPI e JWT.",
    version="1.0.0"
)

# Evento executado ao iniciar a aplicação para criar o banco de dados e as tabelas
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", tags=["Root"])
async def root():
    """
    Rota de verificação (healthcheck) para garantir que a API está online.
    """
    return {
        "status": "online",
        "message": "API Bancária rodando de forma assíncrona com sucesso!"
    }

app.include_router(auth.router)
app.include_router(bank.router)
