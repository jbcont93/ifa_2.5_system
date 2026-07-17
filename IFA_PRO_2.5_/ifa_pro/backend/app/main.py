from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API do IFA PRO 2.5 — plataforma de analise esportiva baseada em "
        "ciencia de dados, IA e aprendizado continuo. Fluxo oficial: "
        "Scanner Global -> Filtro de Elegibilidade -> Motor IFA -> Motor IA "
        "-> Motor de Consenso -> Probabilidades -> Relatorio Analitico -> "
        "Banco de Aprendizado."
    ),
    version="2.5.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "sistema": settings.PROJECT_NAME}
