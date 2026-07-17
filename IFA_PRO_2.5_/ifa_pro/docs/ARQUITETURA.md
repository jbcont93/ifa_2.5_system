# IFA PRO 2.5 APP — Arquitetura (Fase 1 e 2 do prompt mestre)

## Stack

- **Backend**: Python 3.12 + FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL + Redis + Docker
- **Mobile**: Flutter (Android/iOS/Tablet)
- **Auth**: JWT (secao 15)

## Fluxo oficial (secao 2), mapeado para modulos de codigo

```
Scanner Global        -> app/services/scanner_global.py
Filtro Elegibilidade  -> app/services/filtro_elegibilidade.py
Motor IFA             -> app/services/motor_ifa.py
Motor IA              -> app/services/motor_ia.py
Motor de Consenso     -> app/services/motor_consenso.py
Probabilidades        -> app/services/motor_probabilistico.py
Relatorio Analitico   -> app/api/v1/endpoints/analises.py (schema RelatorioAnaliticoOut)
Banco de Aprendizado  -> tabelas analises_ifa / analises_ia / consensos / probabilidades
                          + Probabilidade.resultado_final para calibracao (secao 11)
```

`app/services/pipeline_analise.py` orquestra os 4 motores centrais em
sequencia numa unica transacao (`processar_partida`).

## Rodando localmente

```bash
cd IFA_PRO_2.5
cp backend/.env.example backend/.env
docker compose up --build
```

A API sobe em `http://localhost:8000`, com Swagger em `/docs`. As
migrações do Alembic rodam automaticamente no start do container `api`.

Para criar a primeira migracao (schema inicial):

```bash
docker compose run --rm api alembic revision --autogenerate -m "schema inicial"
docker compose run --rm api alembic upgrade head
```

## Rodando o app Flutter

```bash
cd mobile/ifa_pro_app
flutter pub get
flutter run
```

Ajuste `ApiClient.baseUrl` em `lib/core/api_client.dart` para o endereco
real do backend (o valor padrao `10.0.2.2` so funciona no emulador
Android apontando para o `localhost` da maquina host).

## O que ja esta implementado nesta entrega

- Modelo de dados completo (Fase 2), migrado das 12 tabelas originais do
  Excel/VBA + as 4 novas tabelas do nucleo analitico (analises_ifa,
  analises_ia, consensos, probabilidades) e usuarios/log_auditoria.
- Motor IFA (Fase 4) — formula portada com fidelidade de `modAnaliseIFA.bas`.
- Motor IA (Fase 5) — modulo novo, nao existia no sistema anterior.
- Motor de Consenso (Fase 6) — classificacao Elite/Forte/Descartado
  exatamente conforme os limiares da secao 7.
- Motor Probabilistico (Fase 7) — modelo logistico simples com fator casa.
- API REST (Fase 8): autenticacao JWT, CRUD de clubes/partidas, relatorio
  analitico, lista Elite/Forte, resumo do dashboard.
- App mobile (Fase 9): login, dashboard com KPIs, lista de partidas
  Elite/Forte com cores por classificacao.
- Auditoria (secao 15): toda insercao/alteracao relevante grava em
  `log_auditoria`.
- Painel Administrativo (Fase 9 / Modulo 6): usuarios, auditoria e
  configuracoes, restrito ao papel `admin`.
- Scripts operacionais: `criar_admin.py` (usuario inicial) e
  `importar_xlsx.py` (migra os dados do sistema Excel/VBA anterior).

## Primeiro acesso (depois do `docker compose up`)

Sem um usuario nao da pra fazer login em lugar nenhum. Crie o primeiro
administrador rodando:

```bash
docker compose run --rm api python scripts/criar_admin.py \
    --nome "Seu Nome" --email voce@exemplo.com --senha "escolha-uma-senha-forte"
```

## Painel Administrativo (Modulo 6, secao 13)

Endpoints em `/api/v1/admin/*` (exigem papel `admin`):

- `GET/POST /admin/usuarios` — gerenciar quem acessa o sistema
- `PATCH /admin/usuarios/{id}/desativar`
- `GET /admin/auditoria` — consultar o log de auditoria (secao 15)
- `GET /admin/configuracoes` e `PUT /admin/configuracoes/{chave}` — ajustar
  parametros como os pesos do Motor IFA sem mudar codigo (secao 11: toda
  alteracao fica registrada na auditoria, nada muda sozinho)

## Importando os dados do sistema Excel/VBA anterior

```bash
docker compose run --rm api python scripts/importar_xlsx.py \
    --arquivo /caminho/para/IFA_Analysis_System.xlsx
```

Importa Clubes, Partidas, Estatisticas e Configuracoes. Depois disso,
rode o pipeline de analise (`processar_partida`) para gerar os
Consensos/Probabilidades — eles nao existiam no sistema antigo porque
dependiam do Motor IA, que e novo.

## O que ainda depende de decisao ou de acesso externo

- **Scanner Global real**: a secao 3 exige buscar partidas do mundo todo
  automaticamente. Isso requer uma fonte de dados esportivos ao vivo
  (API-Football, SportRadar, Opta, etc.) com contrato/chave de API — nao
  incluida aqui. A interface `ProvedorPartidas` em `scanner_global.py`
  ja esta pronta para receber essa integracao.
- **Escalacoes provaveis, lesoes e suspensoes em tempo real** dependem da
  mesma fonte de dados.
- **Calibracao do modelo (secao 11)**: os campos `resultado_final` e
  `acertou_cenario` em `Probabilidade` estao prontos para receber o
  resultado real apos a partida, mas o job de comparacao/recalibracao
  automatica ainda nao foi escrito — nenhuma alteracao automatica pode
  ocorrer sem validacao humana, conforme a secao 11 do prompt mestre.
- **Graficos do dashboard** (secao 14): o endpoint `/dashboard/resumo`
  cobre os KPIs numericos e a distribuicao por campeonato; graficos
  visuais no app/painel web ficam para uma proxima fase.
- **Deploy de producao** (Fase 11): domínio, servidor/hospedagem, HTTPS
  e variaveis de ambiente reais — depende de onde voce vai hospedar.

## Migracao de dados do Excel/VBA

Ver `MIGRACAO.md` para o mapeamento tabela a tabela.
