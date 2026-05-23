from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import User, Transacao, TipoTransacao
from app.schemas import TransacaoCreate, TransacaoResponse, ExtratoResponse
from app.security import obter_usuario_atual

router = APIRouter(prefix="/v1/conta", tags=["Operações Bancárias"])

@router.post("/transacao", response_model=TransacaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_transacao(
    transacao_in: TransacaoCreate, 
    db: AsyncSession = Depends(get_db), 
    usuario_atual: User = Depends(obter_usuario_atual)
):
    
    if transacao_in.tipo == TipoTransacao.deposito:
        usuario_atual.saldo += transacao_in.valor

    elif transacao_in.tipo == TipoTransacao.saque:
        if usuario_atual.saldo < transacao_in.valor:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Saldo insuficiente para realizar o saque. Saldo atual: R$ {usuario_atual.saldo:.2f}"
            )
        usuario_atual.saldo -= transacao_in.valor

    nova_transacao = Transacao(
        tipo=transacao_in.tipo,
        valor=transacao_in.valor,
        user_id=usuario_atual.id
    )

    db.add(nova_transacao)
    db.add(usuario_atual)
    
    await db.commit()
    await db.refresh(nova_transacao)
    
    return nova_transacao


@router.get("/extrato", response_model=ExtratoResponse)
async def obter_extrato(
    db: AsyncSession = Depends(get_db), 
    usuario_atual: User = Depends(obter_usuario_atual)
):
    query = (
        select(User)
        .where(User.id == usuario_atual.id)
        .options(selectinload(User.transacoes))
    )
    resultado = await db.execute(query)
    usuario_carregado = resultado.scalars().first()

    transacoes_ordenadas = sorted(
        usuario_carregado.transacoes, 
        key=lambda t: t.data_hora, 
        reverse=True
    )

    return {
        "saldo_atual": usuario_carregado.saldo,
        "transacoes": transacoes_ordenadas
    }