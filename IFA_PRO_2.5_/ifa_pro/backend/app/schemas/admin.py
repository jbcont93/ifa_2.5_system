from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    papel: str = "analista"  # admin | analista | leitor


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str
    papel: str
    ativo: bool


class LogAuditoriaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    data_hora: datetime
    usuario: str
    tabela_afetada: str
    id_registro: str
    acao: str
    valor_anterior: str | None
    valor_novo: str | None


class ConfiguracaoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    chave: str
    valor: str
    descricao: str | None
    categoria: str


class ConfiguracaoUpdate(BaseModel):
    valor: str
