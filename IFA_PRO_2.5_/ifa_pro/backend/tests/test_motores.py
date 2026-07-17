"""Testes unitarios dos motores centrais (rodam sem banco de dados)."""
from app.services.filtro_elegibilidade import CriteriosElegibilidade, avaliar_elegibilidade
from app.services.motor_ia import SinaisConfiabilidade, calcular_ia
from app.services.motor_ifa import MediasClube, calcular_ifa
from app.services.motor_probabilistico import calcular_probabilidades


def test_motor_ifa_classifica_elite_para_time_dominante():
    medias = MediasClube(
        posse_bola_pct=65, finalizacoes=18, finalizacoes_no_alvo=9, escanteios=8,
        faltas=8, cartoes_amarelos=1, cartoes_vermelhos=0,
        passes_certos=500, passes_errados=60, xg=2.4,
    )
    resultado = calcular_ifa(medias)
    assert resultado.classificacao in ("Elite", "Forte")
    assert 0 <= resultado.ifa_geral <= 100


def test_motor_ifa_limita_entre_0_e_100():
    medias = MediasClube(
        posse_bola_pct=10, finalizacoes=1, finalizacoes_no_alvo=0, escanteios=0,
        faltas=25, cartoes_amarelos=6, cartoes_vermelhos=2,
        passes_certos=50, passes_errados=200, xg=0.1,
    )
    resultado = calcular_ifa(medias)
    assert 0 <= resultado.indice_forca_ofensiva <= 100
    assert 0 <= resultado.indice_forca_defensiva <= 100
    assert 0 <= resultado.ifa_geral <= 100


def test_motor_ia_penaliza_troca_de_treinador():
    base = SinaisConfiabilidade(
        percentual_campos_preenchidos=90, quantidade_jogos_historico=20,
        trocou_treinador_recente=False, qtd_lesoes_ativas_chave=0, dias_desde_ultima_partida=7,
    )
    com_troca = SinaisConfiabilidade(**{**base.__dict__, "trocou_treinador_recente": True})

    assert calcular_ia(com_troca).ia_geral < calcular_ia(base).ia_geral


def test_motor_probabilistico_soma_100():
    probs = calcular_probabilidades(80, 60)
    total = round(probs.prob_vitoria_mandante + probs.prob_empate + probs.prob_vitoria_visitante, 0)
    assert total == 100


def test_motor_probabilistico_favorece_mandante_mais_forte():
    probs = calcular_probabilidades(85, 50)
    assert probs.prob_vitoria_mandante > probs.prob_vitoria_visitante
    assert probs.cenario_principal == "Vitoria do mandante"


def test_filtro_elegibilidade_descarta_sem_historico():
    criterios = CriteriosElegibilidade(
        tem_estatisticas_recentes=True, qtd_jogos_historico_mandante=1,
        qtd_jogos_historico_visitante=5, tem_escalacao_provavel=True, dados_desatualizados=False,
    )
    resultado = avaliar_elegibilidade(criterios)
    assert resultado.elegivel is False
    assert "Mandante" in resultado.motivo_descarte


def test_filtro_elegibilidade_aprova_dados_completos():
    criterios = CriteriosElegibilidade(
        tem_estatisticas_recentes=True, qtd_jogos_historico_mandante=10,
        qtd_jogos_historico_visitante=8, tem_escalacao_provavel=True, dados_desatualizados=False,
    )
    resultado = avaliar_elegibilidade(criterios)
    assert resultado.elegivel is True
    assert resultado.motivo_descarte is None
