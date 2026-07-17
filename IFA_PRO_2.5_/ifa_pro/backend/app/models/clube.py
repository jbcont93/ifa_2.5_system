from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Clube(Base):
    """Equivalente a tbl_Clubes do sistema anterior."""
    __tablename__ = "clubes"

    nome: Mapped[str] = mapped_column(String(120), index=True)
    sigla: Mapped[str] = mapped_column(String(10))
    cidade: Mapped[str] = mapped_column(String(80))
    estado: Mapped[str] = mapped_column(String(80))
    pais: Mapped[str] = mapped_column(String(80), index=True)
    fundacao: Mapped[int] = mapped_column(Integer, nullable=True)
    estadio: Mapped[str] = mapped_column(String(120), nullable=True)
    capacidade_estadio: Mapped[int] = mapped_column(Integer, nullable=True)
    tecnico: Mapped[str] = mapped_column(String(120), nullable=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    partidas_mandante = relationship(
        "Partida", foreign_keys="Partida.id_clube_mandante", back_populates="mandante"
    )
    partidas_visitante = relationship(
        "Partida", foreign_keys="Partida.id_clube_visitante", back_populates="visitante"
    )
