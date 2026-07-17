from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class ModeloIA(Base):
    """Equivalente a tbl_ModelosIA: ficha de cada modelo de IA/ML usado
    para apoiar o Motor IA (secao 6)."""
    __tablename__ = "modelos_ia"

    nome_modelo: Mapped[str] = mapped_column(String(120))
    versao: Mapped[str] = mapped_column(String(20))
    tipo_algoritmo: Mapped[str] = mapped_column(String(80))
    data_treinamento: Mapped[date] = mapped_column(Date)
    acuracia: Mapped[float] = mapped_column(Float, default=0)
    dataset: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(20), default="Ativo")
    responsavel: Mapped[str] = mapped_column(String(120))


class LogML(Base):
    """Equivalente a tbl_LogML."""
    __tablename__ = "log_ml"

    id_modelo: Mapped[int] = mapped_column(ForeignKey("modelos_ia.id"))
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    acao: Mapped[str] = mapped_column(String(40))
    parametros: Mapped[str] = mapped_column(String(255), nullable=True)
    resultado: Mapped[str] = mapped_column(String(255), nullable=True)
    usuario: Mapped[str] = mapped_column(String(120), nullable=True)
