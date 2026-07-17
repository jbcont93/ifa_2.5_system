"""
Modelos do nucleo analitico: Motor IFA, Motor IA, Motor de Consenso e
Motor Probabilistico (secoes 5 a 8 do prompt mestre). Juntos formam o
"Relatorio Analitico" (secao 9) e alimentam o "Banco de Aprendizado"
(secao 10) quando o resultado real da partida e conhecido.
"""
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class AnaliseIFA(Base):
    """Motor IFA (secao 5): nota de 0 a 100 por clube, calculada para o
    contexto de uma partida especifica (forma recente, mando de campo,
    eficiencia ofensiva/defensiva, lesoes, escalacao, etc)."""
    __tablename__ = "analises_ifa"

    id_partida: Mapped[int] = mapped_column(ForeignKey("partidas.id"), index=True)
    id_clube: Mapped[int] = mapped_column(ForeignKey("clubes.id"), index=True)

    indice_forca_ofensiva: Mapped[float] = mapped_column(Float)
    indice_forca_defensiva: Mapped[float] = mapped_column(Float)
    ifa_geral: Mapped[float] = mapped_column(Float)
    classificacao: Mapped[str] = mapped_column(String(20))  # Elite/Forte/Regular/Fraco/Critico
    observacao: Mapped[str] = mapped_column(Text, nullable=True)


class AnaliseIA(Base):
    """Motor IA (secao 6): mede a confiabilidade da analise (qualidade
    dos dados, convergencia dos indicadores, incerteza, instabilidade)."""
    __tablename__ = "analises_ia"

    id_partida: Mapped[int] = mapped_column(ForeignKey("partidas.id"), index=True)

    qualidade_dados: Mapped[float] = mapped_column(Float)
    convergencia_indicadores: Mapped[float] = mapped_column(Float)
    grau_incerteza: Mapped[float] = mapped_column(Float)
    estabilidade_equipes: Mapped[float] = mapped_column(Float)
    ia_geral: Mapped[float] = mapped_column(Float)
    observacao: Mapped[str] = mapped_column(Text, nullable=True)


class Consenso(Base):
    """Motor de Consenso (secao 7): combina IFA + IA e classifica a
    partida oficialmente. So partidas Elite/Forte entram no relatorio."""
    __tablename__ = "consensos"

    id_partida: Mapped[int] = mapped_column(ForeignKey("partidas.id"), unique=True, index=True)

    ifa_mandante: Mapped[float] = mapped_column(Float)
    ifa_visitante: Mapped[float] = mapped_column(Float)
    ia_geral: Mapped[float] = mapped_column(Float)
    consenso_final: Mapped[float] = mapped_column(Float)
    classificacao: Mapped[str] = mapped_column(String(20))  # Elite | Forte | Descartado
    grau_risco: Mapped[str] = mapped_column(String(20), nullable=True)  # Baixo | Medio | Alto

    pontos_favoraveis: Mapped[str] = mapped_column(Text, nullable=True)
    pontos_atencao: Mapped[str] = mapped_column(Text, nullable=True)
    fatores_risco: Mapped[str] = mapped_column(Text, nullable=True)

    calculado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    probabilidade = relationship("Probabilidade", back_populates="consenso", uselist=False)


class Probabilidade(Base):
    """Motor Probabilistico (secao 8): probabilidades do resultado mais
    provavel. Registradas para calibracao futura (secao 11)."""
    __tablename__ = "probabilidades"

    id_consenso: Mapped[int] = mapped_column(ForeignKey("consensos.id"), unique=True, index=True)

    prob_vitoria_mandante: Mapped[float] = mapped_column(Float)
    prob_empate: Mapped[float] = mapped_column(Float)
    prob_vitoria_visitante: Mapped[float] = mapped_column(Float)
    cenario_principal: Mapped[str] = mapped_column(String(255))

    # Preenchidos apos a partida terminar, para o Banco de Aprendizado (secao 10)
    resultado_final: Mapped[str] = mapped_column(String(40), nullable=True)
    acertou_cenario: Mapped[bool] = mapped_column(nullable=True)

    consenso = relationship("Consenso", back_populates="probabilidade")
