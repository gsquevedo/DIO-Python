from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from typing import List
from app.models import TipoTransacao

# --- SCHEMAS DE AUTENTICAÇÃO ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None


# --- SCHEMAS DE TRANSAÇÃO ---
class TransacaoBase(BaseModel):
    tipo: TipoTransacao
    valor: float = Field(..., gt=0, description="O valor da operação deve ser maior que zero.")

class TransacaoCreate(TransacaoBase):
    pass

class TransacaoResponse(TransacaoBase):
    id: int
    data_hora: datetime

    class Config:
        from_attributes = True


# --- SCHEMAS DE USUÁRIO ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    saldo: float

    class Config:
        from_attributes = True

# Schema para o Extrato Completo
class ExtratoResponse(BaseModel):
    saldo_atual: float
    transacoes: List[TransacaoResponse]

    class Config:
        from_attributes = True