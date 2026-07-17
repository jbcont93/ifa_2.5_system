from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Lesao(Base):
    """Equivalente a tbl_Lesoes, consumida pelo Filtro de Elegibilidade
    (secao 4) e pelo Motor IFA (secao 5, criterio 'Lesoes')."""
    __tablename__ = "lesoes"

    id_clube: Mapped[int] = mapped_column(ForeignKey("clubes.id"), index=True)
    jogador: Mapped[str] = mapped_column(String(120))
    tipo_lesao: Mapped[str] = mapped_column(String(120))
    regiao_corpo: Mapped[str] = mapped_column(String(80), nullable=True)
    data_ocorrencia: Mapped[date] = mapped_column(Date)
    data_prevista_retorno: Mapped[date] = mapped_column(Date)
    data_retorno_real: Mapped[date] = mapped_column(Date, nullable=True)
    dias_afastado: Mapped[int] = mapped_column(Integer, default=0)
    gravidade: Mapped[str] = mapped_column(String(20))  # Leve | Moderada | Grave
    status: Mapped[str] = mapped_column(String(20), default="Em Tratamento")
