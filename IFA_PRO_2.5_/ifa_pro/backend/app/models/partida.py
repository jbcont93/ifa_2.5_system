from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Partida(Base):
    """Equivalente a tbl_Partidas. Status: Agendada | Elegivel | Descartada |
    Encerrada -- o campo 'status' tambem reflete o resultado do Filtro de
    Elegibilidade (secao 4) antes de a partida entrar no Motor IFA."""
    __tablename__ = "partidas"

    data_partida: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    rodada: Mapped[int] = mapped_column(Integer, nullable=True)
    competicao: Mapped[str] = mapped_column(String(120), index=True)
    pais_competicao: Mapped[str] = mapped_column(String(80), nullable=True)

    id_clube_mandante: Mapped[int] = mapped_column(ForeignKey("clubes.id"))
    id_clube_visitante: Mapped[int] = mapped_column(ForeignKey("clubes.id"))

    gols_mandante: Mapped[int] = mapped_column(Integer, nullable=True)
    gols_visitante: Mapped[int] = mapped_column(Integer, nullable=True)
    publico: Mapped[int] = mapped_column(Integer, nullable=True)
    local: Mapped[str] = mapped_column(String(120), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="Agendada")
    motivo_descarte: Mapped[str] = mapped_column(String(255), nullable=True)

    mandante = relationship("Clube", foreign_keys=[id_clube_mandante], back_populates="partidas_mandante")
    visitante = relationship("Clube", foreign_keys=[id_clube_visitante], back_populates="partidas_visitante")
