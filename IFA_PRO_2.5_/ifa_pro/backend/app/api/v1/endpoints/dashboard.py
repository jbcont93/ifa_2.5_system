from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.analise import Consenso
from app.models.clube import Clube
from app.models.partida import Partida

router = APIRouter()


@router.get("/resumo")
def resumo_dashboard(db: Session = Depends(get_db), _=Depends(get_current_user)):
    """Equivalente ao modDashboard.bas / secao 14 do prompt mestre."""
    total_clubes = db.query(func.count(Clube.id)).scalar()
    total_partidas_analisadas = db.query(func.count(func.distinct(Consenso.id_partida))).scalar()
    total_elite = db.query(func.count(Consenso.id)).filter(Consenso.classificacao == "Elite").scalar()
    total_forte = db.query(func.count(Consenso.id)).filter(Consenso.classificacao == "Forte").scalar()
    total_descartado = db.query(func.count(Consenso.id)).filter(Consenso.classificacao == "Descartado").scalar()
    media_consenso = db.query(func.avg(Consenso.consenso_final)).scalar() or 0

    por_campeonato = (
        db.query(Partida.competicao, func.count(Consenso.id))
        .join(Consenso, Consenso.id_partida == Partida.id)
        .filter(Consenso.classificacao.in_(["Elite", "Forte"]))
        .group_by(Partida.competicao)
        .all()
    )

    return {
        "total_clubes": total_clubes,
        "jogos_analisados": total_partidas_analisadas,
        "jogos_elite": total_elite,
        "jogos_forte": total_forte,
        "jogos_descartados": total_descartado,
        "media_consenso": round(float(media_consenso), 1),
        "desempenho_por_campeonato": [{"campeonato": c, "qtd_aprovados": q} for c, q in por_campeonato],
    }
