"""Equivalente a modAuditoria.bas: toda insercao/alteracao relevante
grava uma linha em log_auditoria."""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.log_auditoria import LogAuditoria


def registrar_auditoria(
    db: Session,
    usuario: str,
    tabela_afetada: str,
    id_registro: str,
    acao: str,
    valor_anterior: str | None = None,
    valor_novo: str | None = None,
) -> None:
    entrada = LogAuditoria(
        data_hora=datetime.now(timezone.utc),
        usuario=usuario,
        tabela_afetada=tabela_afetada,
        id_registro=str(id_registro),
        acao=acao,
        valor_anterior=valor_anterior,
        valor_novo=valor_novo,
    )
    db.add(entrada)
    db.commit()
