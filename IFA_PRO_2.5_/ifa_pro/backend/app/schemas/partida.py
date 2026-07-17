from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PartidaBase(BaseModel):
    data_partida: datetime
    rodada: int | None = None
    competicao: str
    pais_competicao: str | None = None
    id_clube_mandante: int
    id_clube_visitante: int
    local: str | None = None
    status: str = "Agendada"


class PartidaCreate(PartidaBase):
    pass


class PartidaResultado(BaseModel):
    gols_mandante: int
    gols_visitante: int


class PartidaOut(PartidaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    gols_mandante: int | None = None
    gols_visitante: int | None = None
    motivo_descarte: str | None = None
