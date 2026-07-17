"""
Configuracoes globais da aplicacao (equivalente a tbl_Configuracoes do
sistema anterior em Excel/VBA, agora como variaveis de ambiente + tabela
Configuracao para os parametros ajustaveis em runtime).
"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "IFA PRO 2.5 API"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = "postgresql+psycopg2://ifa:ifa@db:5432/ifa_pro"
    REDIS_URL: str = "redis://redis:6379/0"

    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    # Pesos padrao do Motor IFA (secao 5) - sobrepostos pela tabela
    # Configuracao em runtime, mantendo o mesmo padrao do modConfig.bas
    PESO_OFENSIVO_IFA: float = 0.5
    PESO_DEFENSIVO_IFA: float = 0.5

    # Limiares oficiais do Motor de Consenso (secao 7 do prompt mestre)
    CONSENSO_LIMIAR_ELITE: float = 90.0
    CONSENSO_LIMIAR_FORTE: float = 85.0

    CORS_ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
