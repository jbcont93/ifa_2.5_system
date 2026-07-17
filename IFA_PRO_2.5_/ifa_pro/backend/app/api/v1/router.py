from fastapi import APIRouter

from app.api.v1.endpoints import admin, analises, auth, clubes, dashboard, partidas

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Autenticacao"])
api_router.include_router(clubes.router, prefix="/clubes", tags=["Clubes"])
api_router.include_router(partidas.router, prefix="/partidas", tags=["Partidas"])
api_router.include_router(analises.router, prefix="/analises", tags=["Analises"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(admin.router, prefix="/admin", tags=["Painel Administrativo"])
