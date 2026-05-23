import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from app.schemas import TokenData

# Configurações do JWT
SECRET_KEY = os.getenv("SECRET_KEY", "b3m_v1nd0_a0_s1st3m4_b4nc4r10_4ss1ncr0n0_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hashing de senhas com o algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define de onde o FastAPI vai extrair o token automaticamente nas rotas protegidas
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# --- FUNÇÕES DE HASH ---
def verificar_senha(senha_pura: str, senha_hashed: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hashed)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


# --- FUNÇÕES DE TOKEN JWT ---
def criar_token_acesso(data: dict, expires_delta: timedelta | None = None) -> str:
    dados_criptografar = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    dados_criptografar.update({"exp": expire})
    encoded_jwt = jwt.encode(dados_criptografar, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função assíncrona que valida o token e retorna o usuário logado para as rotas protegidas
async def obter_usuario_atual(
    token: str = Depends(oauth2_scheme), 
    db: AsyncSession = Depends(get_db)
) -> User:
    
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais de acesso.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodifica o token recebido
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise excecao_credenciais
        token_data = TokenData(username=username)
    except JWTError:
        raise excecao_credenciais

    # Busca assíncrona do usuário no banco de dados através do SQLAlchemy
    query = select(User).where(User.username == token_data.username)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if usuario is None:
        raise excecao_credenciais
        
    return usuario