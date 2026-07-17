from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.analise import Consenso, Probabilidade
from app.models.clube import Clube
from app.models.partida import Partida
from app.schemas.analise import ProbabilidadeOut, RelatorioAnaliticoOut

router = APIRouter()


@router.get("/relatorio/{id_partida}", response_model=RelatorioAnaliticoOut)
def obter_relatorio(id_partida: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Retorna o Relatorio Analitico (secao 9) de uma partida ja
    processada pelo pipeline (Motor IFA -> IA -> Consenso -> Prob.)."""
    consenso = db.query(Consenso).filter(Consenso.id_partida == id_partida).first()
    if not consenso:
        raise HTTPException(404, "Partida ainda nao possui Consenso calculado")
    if consenso.classificacao == "Descartado":
        raise HTTPException(409, "Partida foi Descartada pelo Motor de Consenso e nao gera relatorio")

    partida = db.get(Partida, id_partida)
    mandante = db.get(Clube, partida.id_clube_mandante)
    visitante = db.get(Clube, partida.id_clube_visitante)
    prob = db.query(Probabilidade).filter(Probabilidade.id_consenso == consenso.id).first()

    return RelatorioAnaliticoOut(
        id_partida=partida.id,
        data=partida.data_partida,
        campeonato=partida.competicao,
        mandante=mandante.nome,
        visitante=visitante.nome,
        ifa_mandante=consenso.ifa_mandante,
        ifa_visitante=consenso.ifa_visitante,
        ia_geral=consenso.ia_geral,
        consenso=consenso.consenso_final,
        classificacao=consenso.classificacao,
        grau_risco=consenso.grau_risco,
        cenario_principal=prob.cenario_principal,
        probabilidades=ProbabilidadeOut.model_validate(prob),
        pontos_favoraveis=(consenso.pontos_favoraveis or "").split("|") if consenso.pontos_favoraveis else [],
        pontos_atencao=(consenso.pontos_atencao or "").split("|") if consenso.pontos_atencao else [],
        fatores_risco=(consenso.fatores_risco or "").split("|") if consenso.fatores_risco else [],
    )


@router.get("/elite-forte", response_model=list[RelatorioAnaliticoOut])
def listar_elite_e_forte(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Lista oficial de saida do sistema (secao 7): so partidas Elite ou
    Forte aparecem aqui — a mesma logica usada no ranking diario do
    Dashboard (secao 14)."""
    consensos = (
        db.query(Consenso)
        .filter(Consenso.classificacao.in_(["Elite", "Forte"]))
        .order_by(Consenso.consenso_final.desc())
        .all()
    )
    relatorios = []
    for consenso in consensos:
        partida = db.get(Partida, consenso.id_partida)
        mandante = db.get(Clube, partida.id_clube_mandante)
        visitante = db.get(Clube, partida.id_clube_visitante)
        prob = db.query(Probabilidade).filter(Probabilidade.id_consenso == consenso.id).first()
        if not prob:
            continue
        relatorios.append(RelatorioAnaliticoOut(
            id_partida=partida.id, data=partida.data_partida, campeonato=partida.competicao,
            mandante=mandante.nome, visitante=visitante.nome,
            ifa_mandante=consenso.ifa_mandante, ifa_visitante=consenso.ifa_visitante,
            ia_geral=consenso.ia_geral, consenso=consenso.consenso_final,
            classificacao=consenso.classificacao, grau_risco=consenso.grau_risco,
            cenario_principal=prob.cenario_principal, probabilidades=ProbabilidadeOut.model_validate(prob),
            pontos_favoraveis=[], pontos_atencao=[], fatores_risco=[],
        ))
    return relatorios
