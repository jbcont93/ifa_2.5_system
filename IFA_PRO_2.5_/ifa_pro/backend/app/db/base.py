"""Importa todos os modelos para que o Alembic (autogenerate) e o
Base.metadata.create_all os enxerguem."""
from app.db.base_class import Base  # noqa: F401
from app.models.usuario import Usuario  # noqa: F401
from app.models.clube import Clube  # noqa: F401
from app.models.partida import Partida  # noqa: F401
from app.models.estatistica import EstatisticaPartida  # noqa: F401
from app.models.performance import PerformanceClube  # noqa: F401
from app.models.lesao import Lesao  # noqa: F401
from app.models.modelo_ia import ModeloIA, LogML  # noqa: F401
from app.models.analise import AnaliseIFA, AnaliseIA, Consenso, Probabilidade  # noqa: F401
from app.models.configuracao import Configuracao  # noqa: F401
from app.models.log_auditoria import LogAuditoria  # noqa: F401
