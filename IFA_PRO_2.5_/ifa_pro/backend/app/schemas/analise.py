from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnaliseIFAOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_clube: int
    indice_forca_ofensiva: float
    indice_forca_defensiva: float
    ifa_geral: float
    classificacao: str


class AnaliseIAOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    qualidade_dados: float
    convergencia_indicadores: float
    grau_incerteza: float
    estabilidade_equipes: float
    ia_geral: float


class ProbabilidadeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    prob_vitoria_mandante: float
    prob_empate: float
    prob_vitoria_visitante: float
    cenario_principal: str


class RelatorioAnaliticoOut(BaseModel):
    """Corresponde exatamente a estrutura da secao 9 do prompt mestre:
    Identificacao + Indicadores + Resultado Provavel + Analise Tecnica."""
    id_partida: int
    data: datetime
    campeonato: str
    mandante: str
    visitante: str

    ifa_mandante: float
    ifa_visitante: float
    ia_geral: float
    consenso: float
    classificacao: str
    grau_risco: str | None

    cenario_principal: str
    probabilidades: ProbabilidadeOut

    pontos_favoraveis: list[str]
    pontos_atencao: list[str]
    fatores_risco: list[str]
