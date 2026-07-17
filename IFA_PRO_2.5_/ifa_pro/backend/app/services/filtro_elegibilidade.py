"""
Filtro de Elegibilidade (secao 4 do prompt mestre).

Roda ANTES do Motor IFA. Uma partida so passa se houver dados minimos
confiaveis; caso contrario e descartada com o motivo registrado (para
auditoria e para o Banco de Aprendizado saber por que a partida nunca
chegou a ser analisada).
"""
from dataclasses import dataclass


@dataclass
class CriteriosElegibilidade:
    tem_estatisticas_recentes: bool  # ao menos N partidas com estatisticas nos ultimos 90 dias
    qtd_jogos_historico_mandante: int
    qtd_jogos_historico_visitante: int
    tem_escalacao_provavel: bool
    dados_desatualizados: bool  # ultima atualizacao de estatisticas > limite configurado


MINIMO_JOGOS_HISTORICO = 3


@dataclass
class ResultadoElegibilidade:
    elegivel: bool
    motivo_descarte: str | None


def avaliar_elegibilidade(criterios: CriteriosElegibilidade) -> ResultadoElegibilidade:
    if not criterios.tem_estatisticas_recentes:
        return ResultadoElegibilidade(False, "Sem estatisticas recentes suficientes")

    if criterios.qtd_jogos_historico_mandante < MINIMO_JOGOS_HISTORICO:
        return ResultadoElegibilidade(
            False, f"Mandante com menos de {MINIMO_JOGOS_HISTORICO} partidas no historico"
        )

    if criterios.qtd_jogos_historico_visitante < MINIMO_JOGOS_HISTORICO:
        return ResultadoElegibilidade(
            False, f"Visitante com menos de {MINIMO_JOGOS_HISTORICO} partidas no historico"
        )

    if criterios.dados_desatualizados:
        return ResultadoElegibilidade(False, "Dados desatualizados alem do limite configurado")

    if not criterios.tem_escalacao_provavel:
        return ResultadoElegibilidade(False, "Escalacao provavel indisponivel")

    return ResultadoElegibilidade(True, None)
