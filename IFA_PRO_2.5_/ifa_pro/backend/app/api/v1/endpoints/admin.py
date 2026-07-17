"""
Painel Administrativo (Modulo 6, secao 13 do prompt mestre): controle de
usuarios, auditoria e configuracoes. Todos os endpoints exigem papel
'admin' (secao 15 - Seguranca).
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.core.security import hash_password
from app.db.session import get_db
from app.models.configuracao import Configuracao
from app.models.log_auditoria import LogAuditoria
from app.models.usuario import Usuario
from app.schemas.admin import (
    ConfiguracaoOut,
    ConfiguracaoUpdate,
    LogAuditoriaOut,
    UsuarioCreate,
    UsuarioOut,
)
from app.services.auditoria import registrar_auditoria

router = APIRouter()


# ---------- Usuarios ----------

@router.get("/usuarios", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(Usuario).order_by(Usuario.nome).all()


@router.post("/usuarios", response_model=UsuarioOut, status_code=201)
def criar_usuario(payload: UsuarioCreate, db: Session = Depends(get_db), admin=Depends(require_admin)):
    if db.query(Usuario).filter(Usuario.email == payload.email).first():
        raise HTTPException(409, "Ja existe um usuario com esse email")
    usuario = Usuario(
        nome=payload.nome, email=payload.email,
        senha_hash=hash_password(payload.senha), papel=payload.papel,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    registrar_auditoria(db, admin.email, "usuarios", str(usuario.id), "Insercao", valor_novo=usuario.email)
    return usuario


@router.patch("/usuarios/{id_usuario}/desativar", response_model=UsuarioOut)
def desativar_usuario(id_usuario: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    usuario = db.get(Usuario, id_usuario)
    if not usuario:
        raise HTTPException(404, "Usuario nao encontrado")
    usuario.ativo = False
    db.commit()
    db.refresh(usuario)
    registrar_auditoria(db, admin.email, "usuarios", str(usuario.id), "Alteracao", valor_novo="Inativo")
    return usuario


# ---------- Auditoria ----------

@router.get("/auditoria", response_model=list[LogAuditoriaOut])
def listar_auditoria(
    limite: int = 100, tabela: str | None = None, db: Session = Depends(get_db), _=Depends(require_admin)
):
    query = db.query(LogAuditoria)
    if tabela:
        query = query.filter(LogAuditoria.tabela_afetada == tabela)
    return query.order_by(LogAuditoria.data_hora.desc()).limit(limite).all()


# ---------- Configuracoes ----------

@router.get("/configuracoes", response_model=list[ConfiguracaoOut])
def listar_configuracoes(db: Session = Depends(get_db), _=Depends(require_admin)):
    return db.query(Configuracao).order_by(Configuracao.categoria, Configuracao.chave).all()


@router.put("/configuracoes/{chave}", response_model=ConfiguracaoOut)
def atualizar_configuracao(
    chave: str, payload: ConfiguracaoUpdate, db: Session = Depends(get_db), admin=Depends(require_admin)
):
    """Altera um parametro (ex.: PESO_OFENSIVO_IFA). Nenhuma alteracao
    automatica pode ocorrer sem validacao humana (secao 11) — por isso
    esse endpoint exige papel admin e fica registrado na auditoria."""
    config = db.query(Configuracao).filter(Configuracao.chave == chave).first()
    valor_anterior = config.valor if config else None
    if not config:
        config = Configuracao(chave=chave, valor=payload.valor, categoria="Geral")
        db.add(config)
    else:
        config.valor = payload.valor
    db.commit()
    db.refresh(config)
    registrar_auditoria(db, admin.email, "configuracoes", chave, "Alteracao", valor_anterior, payload.valor)
    return config
