from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.partida import Partida
from app.schemas.partida import PartidaCreate, PartidaOut, PartidaResultado
from app.services.auditoria import registrar_auditoria

router = APIRouter()


@router.get("", response_model=list[PartidaOut])
def listar_partidas(
    status_filtro: str | None = None,
    competicao: str | None = None,
    db: Session = Depends(get_db),
    _=Depends(get_current_user),
):
    query = db.query(Partida)
    if status_filtro:
        query = query.filter(Partida.status == status_filtro)
    if competicao:
        query = query.filter(Partida.competicao == competicao)
    return query.order_by(Partida.data_partida.desc()).all()


@router.post("", response_model=PartidaOut, status_code=201)
def cadastrar_partida(payload: PartidaCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    if payload.id_clube_mandante == payload.id_clube_visitante:
        raise HTTPException(400, "Clube mandante e visitante nao podem ser iguais")
    partida = Partida(**payload.model_dump())
    db.add(partida)
    db.commit()
    db.refresh(partida)
    registrar_auditoria(db, usuario.email, "partidas", str(partida.id), "Insercao")
    return partida


@router.patch("/{id_partida}/resultado", response_model=PartidaOut)
def registrar_resultado(
    id_partida: int, payload: PartidaResultado, db: Session = Depends(get_db), usuario=Depends(get_current_user)
):
    partida = db.get(Partida, id_partida)
    if not partida:
        raise HTTPException(404, "Partida nao encontrada")
    partida.gols_mandante = payload.gols_mandante
    partida.gols_visitante = payload.gols_visitante
    partida.status = "Encerrada"
    db.commit()
    db.refresh(partida)
    registrar_auditoria(db, usuario.email, "partidas", str(partida.id), "Alteracao", valor_novo="Encerrada")
    return partida
