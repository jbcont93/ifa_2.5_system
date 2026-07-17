from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.clube import Clube
from app.schemas.clube import ClubeCreate, ClubeOut
from app.services.auditoria import registrar_auditoria

router = APIRouter()


@router.get("", response_model=list[ClubeOut])
def listar_clubes(ativo: bool | None = None, db: Session = Depends(get_db), _=Depends(get_current_user)):
    query = db.query(Clube)
    if ativo is not None:
        query = query.filter(Clube.ativo == ativo)
    return query.order_by(Clube.nome).all()


@router.post("", response_model=ClubeOut, status_code=201)
def cadastrar_clube(payload: ClubeCreate, db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    clube = Clube(**payload.model_dump())
    db.add(clube)
    db.commit()
    db.refresh(clube)
    registrar_auditoria(db, usuario.email, "clubes", str(clube.id), "Insercao", valor_novo=clube.nome)
    return clube
