from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class EstatisticaPartida(Base):
    """Equivalente a tbl_EstatisticasPartida."""
    __tablename__ = "estatisticas_partida"

    id_partida: Mapped[int] = mapped_column(ForeignKey("partidas.id"), index=True)
    id_clube: Mapped[int] = mapped_column(ForeignKey("clubes.id"), index=True)

    posse_bola_pct: Mapped[float] = mapped_column(Float, default=0)
    finalizacoes: Mapped[int] = mapped_column(Integer, default=0)
    finalizacoes_no_alvo: Mapped[int] = mapped_column(Integer, default=0)
    escanteios: Mapped[int] = mapped_column(Integer, default=0)
    faltas: Mapped[int] = mapped_column(Integer, default=0)
    cartoes_amarelos: Mapped[int] = mapped_column(Integer, default=0)
    cartoes_vermelhos: Mapped[int] = mapped_column(Integer, default=0)
    passes_certos: Mapped[int] = mapped_column(Integer, default=0)
    passes_errados: Mapped[int] = mapped_column(Integer, default=0)
    xg: Mapped[float] = mapped_column(Float, default=0)
