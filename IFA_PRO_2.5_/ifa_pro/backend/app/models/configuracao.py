from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Configuracao(Base):
    """Equivalente a tbl_Configuracoes: parametros ajustaveis sem alterar
    codigo (pesos do Motor IFA, limiares do Consenso, etc)."""
    __tablename__ = "configuracoes"

    chave: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    valor: Mapped[str] = mapped_column(String(255))
    descricao: Mapped[str] = mapped_column(String(255), nullable=True)
    categoria: Mapped[str] = mapped_column(String(60), default="Geral")
