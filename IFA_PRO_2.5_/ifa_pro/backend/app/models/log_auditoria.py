from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class LogAuditoria(Base):
    """Equivalente a tbl_LogAuditoria (secao 15 - Seguranca: auditoria)."""
    __tablename__ = "log_auditoria"

    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    usuario: Mapped[str] = mapped_column(String(120))
    tabela_afetada: Mapped[str] = mapped_column(String(80))
    id_registro: Mapped[str] = mapped_column(String(40))
    acao: Mapped[str] = mapped_column(String(40))
    valor_anterior: Mapped[str] = mapped_column(String(500), nullable=True)
    valor_novo: Mapped[str] = mapped_column(String(500), nullable=True)
