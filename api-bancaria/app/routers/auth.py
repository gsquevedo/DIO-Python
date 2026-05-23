from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.security import gerar_hash_senha, verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuario: UserCreate, db: AsyncSession = Depends(get_db)):
    query_username = select(User).where(User.username == usuario.username)
    resultado_username = await db.execute(query_username)
    if resultado_username.scalars().first():
        raise HTTPException(status_code=400, detail="Nome de usuário já cadastrado.")

    query_email = select(User).where(User.email == usuario.email)
    resultado_email = await db.execute(query_email)
    if resultado_email.scalars().first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Cria o novo usuário com a senha criptografada
    senha_criptografada = gerar_hash_senha(usuario.password)
    novo_usuario = User(
        username=usuario.username,
        email=usuario.email,
        hashed_password=senha_criptografada
    )
    
    db.add(novo_usuario)
    await db.commit()
    await db.refresh(novo_usuario)
    return novo_usuario


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.username == form_data.username)
    resultado = await db.execute(query)
    usuario = resultado.scalars().first()

    if not usuario or not verificar_senha(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera e retorna o token de acesso JWT
    token_acesso = criar_token_acesso(data={"sub": usuario.username})
    return {"access_token": token_acesso, "token_type": "bearer"}