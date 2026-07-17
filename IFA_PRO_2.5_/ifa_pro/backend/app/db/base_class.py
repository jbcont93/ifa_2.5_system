from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa. Toda tabela ganha ID, criado_em e atualizado_em
    automaticamente, preservando o padrao de auditoria do sistema anterior
    (cada insercao/alteracao era logada em tbl_LogAuditoria)."""

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
