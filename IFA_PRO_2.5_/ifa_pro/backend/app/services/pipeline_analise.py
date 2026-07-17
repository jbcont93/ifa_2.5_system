"""
Orquestra o fluxo obrigatorio da secao 2 do prompt mestre, a partir do
ponto em que uma partida ja passou pelo Scanner Global + Filtro de
Elegibilidade:

    MOTOR IFA -> MOTOR IA -> MOTOR DE CONSENSO -> PROBABILIDADES
    -> RELATORIO ANALITICO -> BANCO DE APRENDIZADO

`processar_partida` roda os quatro motores em sequencia e persiste tudo
(analises_ifa x2, analises_ia, consensos, probabilidades). Partidas
classificadas como "Descartado" pelo Motor de Consenso NAO geram
Probabilidade nem entram no relatorio (secao 7), mas o registro de
Consenso fica salvo para fins de auditoria/calibracao (secao 11).
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.analise import AnaliseIA, AnaliseIFA, Consenso, Probabilidade
from app.services.motor_consenso import calcular_consenso
from app.services.motor_ia import ResultadoIA
from app.services.motor_ifa import MediasClube, ResultadoIFA, calcular_ifa
from app.services.motor_probabilistico import calcular_probabilidades


def processar_partida(
    db: Session,
    id_partida: int,
    id_clube_mandante: int,
    id_clube_visitante: int,
    medias_mandante: MediasClube,
    medias_visitante: MediasClube,
    resultado_ia: ResultadoIA,
    peso_ofensivo: float,
    peso_defensivo: float,
) -> Consenso:
    ifa_mandante: ResultadoIFA = calcular_ifa(medias_mandante, peso_ofensivo, peso_defensivo)
    ifa_visitante: ResultadoIFA = calcular_ifa(medias_visitante, peso_ofensivo, peso_defensivo)

    db.add(AnaliseIFA(
        id_partida=id_partida, id_clube=id_clube_mandante,
        indice_forca_ofensiva=ifa_mandante.indice_forca_ofensiva,
        indice_forca_defensiva=ifa_mandante.indice_forca_defensiva,
        ifa_geral=ifa_mandante.ifa_geral, classificacao=ifa_mandante.classificacao,
    ))
    db.add(AnaliseIFA(
        id_partida=id_partida, id_clube=id_clube_visitante,
        indice_forca_ofensiva=ifa_visitante.indice_forca_ofensiva,
        indice_forca_defensiva=ifa_visitante.indice_forca_defensiva,
        ifa_geral=ifa_visitante.ifa_geral, classificacao=ifa_visitante.classificacao,
    ))
    db.add(AnaliseIA(
        id_partida=id_partida,
        qualidade_dados=resultado_ia.qualidade_dados,
        convergencia_indicadores=resultado_ia.convergencia_indicadores,
        grau_incerteza=resultado_ia.grau_incerteza,
        estabilidade_equipes=resultado_ia.estabilidade_equipes,
        ia_geral=resultado_ia.ia_geral,
    ))

    consenso_calc = calcular_consenso(ifa_mandante.ifa_geral, ifa_visitante.ifa_geral, resultado_ia.ia_geral)

    consenso = Consenso(
        id_partida=id_partida,
        ifa_mandante=ifa_mandante.ifa_geral,
        ifa_visitante=ifa_visitante.ifa_geral,
        ia_geral=resultado_ia.ia_geral,
        consenso_final=consenso_calc.consenso_final,
        classificacao=consenso_calc.classificacao,
        grau_risco=consenso_calc.grau_risco,
        calculado_em=datetime.now(timezone.utc),
    )
    db.add(consenso)
    db.flush()  # garante consenso.id antes de criar a Probabilidade

    if consenso_calc.classificacao != "Descartado":
        probs = calcular_probabilidades(ifa_mandante.ifa_geral, ifa_visitante.ifa_geral)
        db.add(Probabilidade(
            id_consenso=consenso.id,
            prob_vitoria_mandante=probs.prob_vitoria_mandante,
            prob_empate=probs.prob_empate,
            prob_vitoria_visitante=probs.prob_vitoria_visitante,
            cenario_principal=probs.cenario_principal,
        ))

    db.commit()
    db.refresh(consenso)
    return consenso
