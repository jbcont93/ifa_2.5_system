# IFA PRO 2.5 APP

Migracao do sistema Excel/VBA (`IFA_Analysis_System`) para a arquitetura
oficial definida no prompt mestre: **Python/FastAPI/PostgreSQL/Redis/
Docker** no backend e **Flutter** no app mobile.

Comece por `docs/ARQUITETURA.md`.

## Estrutura

```
IFA_PRO_2.5/
├── backend/            # API FastAPI (Fases 1, 2, 4-8, 12, 13)
│   ├── app/
│   │   ├── core/        # config, seguranca (JWT)
│   │   ├── db/           # base declarativa, sessao
│   │   ├── models/       # SQLAlchemy — 14 tabelas
│   │   ├── schemas/      # Pydantic
│   │   ├── services/     # os "motores": IFA, IA, Consenso, Probabilistico,
│   │   │                  Scanner Global, Filtro de Elegibilidade, Auditoria
│   │   └── api/v1/       # endpoints REST
│   ├── alembic/          # migracoes
│   ├── tests/            # testes unitarios dos motores
│   └── docker-compose (na raiz)
├── mobile/
│   └── ifa_pro_app/      # Flutter (Fase 9): login, dashboard, lista Elite/Forte
└── docs/
    ├── ARQUITETURA.md    # o que ja esta pronto, o que falta, como rodar
    └── MIGRACAO.md        # mapeamento tabela a tabela do Excel -> Postgres
```

## O que so depende de voce agora (nao posso decidir por voce)

1. **Escolher e contratar um provedor de dados esportivos** (ex.:
   API-Football, SportRadar) e plugar a chave em `ProvedorPartidas`
   (`app/services/scanner_global.py`) — sem isso o Scanner Global nao
   busca jogos reais do mundo todo.
2. **Decidir onde hospedar** (Fase 11): servidor, dominio, HTTPS.

## Como rodar o que ja esta pronto

```bash
cp backend/.env.example backend/.env
docker compose up --build
docker compose run --rm api alembic revision --autogenerate -m "schema inicial"
docker compose run --rm api alembic upgrade head
docker compose run --rm api python scripts/criar_admin.py --nome "Seu Nome" --email voce@exemplo.com --senha "sua-senha"
# opcional: trazer os dados do sistema Excel/VBA anterior
docker compose run --rm api python scripts/importar_xlsx.py --arquivo /caminho/para/IFA_Analysis_System.xlsx
```

A API sobe em `http://localhost:8000/docs`. Detalhes de cada peça em
`docs/ARQUITETURA.md`.
