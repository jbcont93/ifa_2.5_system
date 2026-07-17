"""
Motor de Consenso (secao 7 do prompt mestre).

Combina IFA (dos dois clubes) + IA (confiabilidade da partida) em um
Consenso Final e aplica a classificacao oficial:

    Consenso >= 90            -> ELITE      (selecao prioritaria)
    85 <= Consenso < 90        -> FORTE      (selecao condicional)
    Consenso < 85              -> DESCARTADO (nao entra no relatorio)

A forma de combinar IFA + IA e um parametro de modelo (nao especificado
literalmente no prompt mestre alem de "Gerar CONSENSO FINAL"): aqui a
media dos dois IFAs representa a forca esperada do confronto, e o
Consenso Final pondera essa forca pela confiabilidade (IA) da analise —
uma partida "forte" tecnicamente mas com dados pouco confiaveis nao deve
alcancar Elite. Os pesos ficam em Configuracao (PESO_FORCA_CONSENSO /
PESO_CONFIABILIDADE_CONSENSO), 70/30 por padrao.
"""
from dataclasses import dataclass

from app.core.config import get_settings

settings = get_settings()


@dataclass
class ResultadoConsenso:
    consenso_final: float
    classificacao: str  # Elite | Forte | Descartado
    grau_risco: str  # Baixo | Medio | Alto


def classificar_consenso(consenso_final: float) -> str:
    if consenso_final >= settings.CONSENSO_LIMIAR_ELITE:
        return "Elite"
    if consenso_final >= settings.CONSENSO_LIMIAR_FORTE:
        return "Forte"
    return "Descartado"


def calcular_grau_risco(ia_geral: float) -> str:
    if ia_geral >= 80:
        return "Baixo"
    if ia_geral >= 60:
        return "Medio"
    return "Alto"


def calcular_consenso(
    ifa_mandante: float,
    ifa_visitante: float,
    ia_geral: float,
    peso_forca: float = 0.7,
    peso_confiabilidade: float = 0.3,
) -> ResultadoConsenso:
    forca_confronto = (ifa_mandante + ifa_visitante) / 2
    consenso_final = round(forca_confronto * peso_forca + ia_geral * peso_confiabilidade, 1)

    return ResultadoConsenso(
        consenso_final=consenso_final,
        classificacao=classificar_consenso(consenso_final),
        grau_risco=calcular_grau_risco(ia_geral),
    )
