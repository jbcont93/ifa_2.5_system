"""
Motor IFA (secao 5 do prompt mestre) — Indice de Forca Analitica.

Portado com fidelidade da formula original em modAnaliseIFA.bas, agora
recebendo as medias de estatisticas de um clube (calculadas a partir de
tbl_EstatisticasPartida / estatisticas_partida) e retornando uma nota
de 0 a 100.

Formula original (preservada):
    indice_ofensivo  = finalizacoes_alvo*3 + xg*15 + posse*0.4 + escanteios*1.5
    indice_defensivo = 100 - faltas*0.8 - cartoes_amarelos*2 - cartoes_vermelhos*5
                        + (passes_certos / (passes_certos + passes_errados)) * 20
    ifa_geral = indice_ofensivo * peso_ofensivo + indice_defensivo * peso_defensivo
"""
from dataclasses import dataclass


@dataclass
class MediasClube:
    posse_bola_pct: float
    finalizacoes: float
    finalizacoes_no_alvo: float
    escanteios: float
    faltas: float
    cartoes_amarelos: float
    cartoes_vermelhos: float
    passes_certos: float
    passes_errados: float
    xg: float


@dataclass
class ResultadoIFA:
    indice_forca_ofensiva: float
    indice_forca_defensiva: float
    ifa_geral: float
    classificacao: str


def _limitar_0_100(valor: float) -> float:
    return max(0.0, min(100.0, valor))


def classificar_ifa(ifa_geral: float) -> str:
    if ifa_geral >= 80:
        return "Elite"
    if ifa_geral >= 65:
        return "Forte"
    if ifa_geral >= 50:
        return "Regular"
    if ifa_geral >= 35:
        return "Fraco"
    return "Critico"


def calcular_ifa(
    medias: MediasClube,
    peso_ofensivo: float = 0.5,
    peso_defensivo: float = 0.5,
) -> ResultadoIFA:
    indice_ofensivo = (
        medias.finalizacoes_no_alvo * 3
        + medias.xg * 15
        + medias.posse_bola_pct * 0.4
        + medias.escanteios * 1.5
    )
    indice_ofensivo = _limitar_0_100(indice_ofensivo)

    indice_defensivo = (
        100
        - medias.faltas * 0.8
        - medias.cartoes_amarelos * 2
        - medias.cartoes_vermelhos * 5
    )
    total_passes = medias.passes_certos + medias.passes_errados
    if total_passes > 0:
        indice_defensivo += (medias.passes_certos / total_passes) * 20
    indice_defensivo = _limitar_0_100(indice_defensivo)

    ifa_geral = round(
        indice_ofensivo * peso_ofensivo + indice_defensivo * peso_defensivo, 1
    )

    return ResultadoIFA(
        indice_forca_ofensiva=round(indice_ofensivo, 1),
        indice_forca_defensiva=round(indice_defensivo, 1),
        ifa_geral=ifa_geral,
        classificacao=classificar_ifa(ifa_geral),
    )
