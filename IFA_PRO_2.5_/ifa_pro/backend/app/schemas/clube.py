from pydantic import BaseModel, ConfigDict


class ClubeBase(BaseModel):
    nome: str
    sigla: str
    cidade: str
    estado: str
    pais: str
    fundacao: int | None = None
    estadio: str | None = None
    capacidade_estadio: int | None = None
    tecnico: str | None = None
    ativo: bool = True


class ClubeCreate(ClubeBase):
    pass


class ClubeOut(ClubeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
