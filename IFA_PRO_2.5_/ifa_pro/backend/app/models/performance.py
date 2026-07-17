from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class PerformanceClube(Base):
    """Equivalente a tbl_PerformanceClubes: agregado por clube/temporada."""
    __tablename__ = "performance_clubes"

    id_clube: Mapped[int] = mapped_column(ForeignKey("clubes.id"), index=True)
    temporada: Mapped[str] = mapped_column(String(4), index=True)

    jogos: Mapped[int] = mapped_column(Integer, default=0)
    vitorias: Mapped[int] = mapped_column(Integer, default=0)
    empates: Mapped[int] = mapped_column(Integer, default=0)
    derrotas: Mapped[int] = mapped_column(Integer, default=0)
    gols_pro: Mapped[int] = mapped_column(Integer, default=0)
    gols_contra: Mapped[int] = mapped_column(Integer, default=0)
    saldo_gols: Mapped[int] = mapped_column(Integer, default=0)
    pontos: Mapped[int] = mapped_column(Integer, default=0)
    aproveitamento_pct: Mapped[float] = mapped_column(Float, default=0)
