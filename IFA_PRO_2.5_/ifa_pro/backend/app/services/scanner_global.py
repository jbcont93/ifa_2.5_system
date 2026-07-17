"""
Scanner Global (secao 3 do prompt mestre).

REGRA FUNDAMENTAL do prompt mestre: "O usuario nao escolhe as partidas" —
o Scanner Global busca automaticamente jogos no mundo todo e os
encaminha para o Filtro de Elegibilidade.

Isso exige uma fonte de dados esportivos ao vivo (ex.: API-Football,
SportRadar, Opta, etc). Este modulo define a INTERFACE (Protocol) que
qualquer provedor precisa implementar, mais uma implementacao de
exemplo em memoria para desenvolvimento/teste sem depender de rede.

Para produção: implemente `ProvedorPartidas` chamando a API do provedor
escolhido e registre-a em `PROVEDOR_ATIVO` (injecao de dependencia via
app/core/config.py). Nenhuma chave de API de terceiros esta configurada
aqui.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass
class PartidaCandidata:
    data_partida: datetime
    competicao: str
    pais_competicao: str
    nome_mandante: str
    nome_visitante: str
    fonte: str


class ProvedorPartidas(Protocol):
    def buscar_partidas_do_dia(self, data: datetime) -> list[PartidaCandidata]:
        ...


class ProvedorExemploEmMemoria:
    """Implementacao de referencia (sem rede) usada em desenvolvimento e
    nos testes automatizados. Substitua por um provedor real antes de ir
    para producao (Fase 11 do prompt mestre)."""

    def buscar_partidas_do_dia(self, data: datetime) -> list[PartidaCandidata]:
        return []


def executar_scanner(provedor: ProvedorPartidas, data: datetime) -> list[PartidaCandidata]:
    """Ponto de entrada unico do Scanner Global: sempre passa pelo
    provedor configurado, nunca por escolha manual do usuario, conforme
    a regra fundamental da secao 3."""
    return provedor.buscar_partidas_do_dia(data)
