"""
Motor Probabilistico (secao 8 do prompt mestre).

Converte a diferenca de forca (IFA) entre mandante e visitante em
probabilidades de vitoria mandante / empate / vitoria visitante,
aplicando o fator casa (vantagem de mando de campo). O metodo e um
modelo logistico simples de 3 vias — o campo fica pronto para, no
futuro, ser substituido por um modelo treinado (tbl_ModelosIA /
modelos_ia ja esta preparado para registrar esse tipo de modelo,
conforme a secao 7 da documentacao tecnica original).
"""
import math
from dataclasses import dataclass

FATOR_CASA = 5.0  # pontos de IFA adicionados ao mandante para refletir o mando de campo


@dataclass
class ResultadoProbabilidades:
    prob_vitoria_mandante: float
    prob_empate: float
    prob_vitoria_visitante: float
    cenario_principal: str


def calcular_probabilidades(ifa_mandante: float, ifa_visitante: float) -> ResultadoProbabilidades:
    diferenca = (ifa_mandante + FATOR_CASA) - ifa_visitante

    # Funcao logistica para vitoria mandante vs. "nao mandante"
    prob_mandante_bruta = 1 / (1 + math.exp(-diferenca / 15))

    # A fatia de empate encolhe quando a diferenca de forca e grande
    # (jogos muito desequilibrados tem menos chance de terminar empatados)
    prob_empate_bruta = 0.30 - min(abs(diferenca), 30) * 0.004

    prob_mandante = prob_mandante_bruta * (1 - prob_empate_bruta)
    prob_visitante = (1 - prob_mandante_bruta) * (1 - prob_empate_bruta)
    prob_empate = prob_empate_bruta

    total = prob_mandante + prob_empate + prob_visitante
    prob_mandante, prob_empate, prob_visitante = (
        round((prob_mandante / total) * 100, 1),
        round((prob_empate / total) * 100, 1),
        round((prob_visitante / total) * 100, 1),
    )

    probs = {"Vitoria do mandante": prob_mandante, "Empate": prob_empate, "Vitoria do visitante": prob_visitante}
    cenario_principal = max(probs, key=probs.get)

    return ResultadoProbabilidades(
        prob_vitoria_mandante=prob_mandante,
        prob_empate=prob_empate,
        prob_vitoria_visitante=prob_visitante,
        cenario_principal=cenario_principal,
    )
