from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    nome: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    papel: Mapped[str] = mapped_column(String(20), default="analista")  # admin | analista | leitor
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
