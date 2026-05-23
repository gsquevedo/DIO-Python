from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.database import Base

class TipoTransacao(str, enum.Enum):
    deposito = "deposito"
    saque = "saque"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Cada usuário começa com saldo 0.0
    saldo = Column(Float, default=0.0, nullable=False)

    #  Um usuário pode ter múltiplas transações
    transacoes = relationship("Transacao", back_populates="dono", cascade="all, delete-orphan")


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoTransacao), nullable=False)
    valor = Column(Float, nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Chave estrangeira ligando a transação ao usuário
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    dono = relationship("User", back_populates="transacoes")