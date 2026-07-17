"""
Motor IA (secao 6 do prompt mestre) — avalia a CONFIABILIDADE da analise,
nao o desempenho dos clubes. E o modulo novo do IFA PRO 2.5 (nao existia
no sistema Excel/VBA anterior).

Criterios (0 a 100 cada), combinados em ia_geral:
  - qualidade_dados: completude/consistencia dos dados coletados
  - convergencia_indicadores: o quanto os indicadores (forma, performance,
    estatisticas) apontam na mesma direcao
  - grau_incerteza: inverso de fatores como troca de treinador recente,
    poucos jogos na temporada, instabilidade do elenco
  - estabilidade_equipes: relacionado a lesoes/suspensoes de jogadores-chave

Os pesos sao iguais por padrao (25% cada) e configuraveis via tabela
Configuracao, seguindo o mesmo padrao do Motor IFA.
"""
from dataclasses import dataclass


@dataclass
class SinaisConfiabilidade:
    percentual_campos_preenchidos: float  # 0-100: completude dos dados da partida
    quantidade_jogos_historico: int  # nº de partidas com estatisticas registradas p/ cada clube
    trocou_treinador_recente: bool
    qtd_lesoes_ativas_chave: int  # lesoes de titulares nos dois clubes
    dias_desde_ultima_partida: int  # de cada clube (usar o menor dos dois, calendario apertado)


@dataclass
class ResultadoIA:
    qualidade_dados: float
    convergencia_indicadores: float
    grau_incerteza: float
    estabilidade_equipes: float
    ia_geral: float


def _limitar_0_100(valor: float) -> float:
    return max(0.0, min(100.0, valor))


def calcular_ia(sinais: SinaisConfiabilidade) -> ResultadoIA:
    qualidade_dados = _limitar_0_100(sinais.percentual_campos_preenchidos)

    # Mais jogos no historico = indicadores convergem com mais confianca.
    # Satura em 20 jogos (amostra considerada suficiente).
    convergencia = _limitar_0_100((sinais.quantidade_jogos_historico / 20) * 100)

    # Grau de incerteza comeca em 100 (baixa incerteza) e cai com sinais de
    # instabilidade: troca de treinador (-25) e calendario apertado (-1 por
    # dia abaixo de 4 dias de descanso).
    incerteza = 100.0
    if sinais.trocou_treinador_recente:
        incerteza -= 25
    if sinais.dias_desde_ultima_partida < 4:
        incerteza -= (4 - sinais.dias_desde_ultima_partida) * 5
    incerteza = _limitar_0_100(incerteza)

    # Estabilidade cai 10 pontos por lesao ativa de jogador-chave.
    estabilidade = _limitar_0_100(100 - sinais.qtd_lesoes_ativas_chave * 10)

    ia_geral = round(
        (qualidade_dados + convergencia + incerteza + estabilidade) / 4, 1
    )

    return ResultadoIA(
        qualidade_dados=round(qualidade_dados, 1),
        convergencia_indicadores=round(convergencia, 1),
        grau_incerteza=round(incerteza, 1),
        estabilidade_equipes=round(estabilidade, 1),
        ia_geral=ia_geral,
    )
