# Mapeamento: Excel/VBA (IFA Analysis System) -> IFA PRO 2.5 (Postgres)

| Tabela Excel (`tbl_...`)     | Tabela Postgres         | Observacoes |
|---|---|---|
| tbl_Clubes                   | clubes                  | 1:1 |
| tbl_Partidas                 | partidas                | + campos `pais_competicao`, `motivo_descarte` (novo, do Filtro de Elegibilidade) |
| tbl_EstatisticasPartida      | estatisticas_partida    | 1:1 |
| tbl_PerformanceClubes        | performance_clubes      | 1:1 |
| tbl_Lesoes                   | lesoes                  | 1:1 |
| tbl_AnaliseIFA               | analises_ifa            | agora por partida+clube (era so por clube) — o IFA passa a ser contextual ao confronto |
| tbl_ModelosIA                | modelos_ia              | 1:1 |
| tbl_LogML                    | log_ml                  | 1:1 |
| tbl_LogAuditoria             | log_auditoria            | 1:1 |
| tbl_Configuracoes            | configuracoes            | 1:1 |
| (nao existia)                | analises_ia              | novo — Motor IA (secao 6) |
| (nao existia)                | consensos                 | novo — Motor de Consenso (secao 7) |
| (nao existia)                | probabilidades            | novo — Motor Probabilistico (secao 8) |
| (nao existia)                | usuarios                  | novo — autenticacao JWT (secao 15) |

## Script de exportacao do .xlsx (ponto de partida)

O arquivo `IFA_Analysis_System.xlsx` original pode ser lido com
`openpyxl`/`pandas` e cada Tabela Estruturada exportada para CSV, depois
carregada nas tabelas Postgres equivalentes acima com `COPY` ou um script
Python simples usando os models de `app/models/`. Como o volume de dados
de exemplo tende a ser pequeno (sistema recem-criado), a recomendacao e
escrever um script `scripts/importar_xlsx.py` (proxima entrega) que:

1. Abre o `.xlsx` com `openpyxl`;
2. Para cada `tbl_*`, le as linhas e insere via SQLAlchemy respeitando a
   ordem de dependencia (Clubes -> Partidas -> Estatisticas/Performance/
   Lesoes -> ModelosIA/LogML -> Configuracoes -> LogAuditoria);
3. Roda `AnaliseIFA` como estava (por clube) para popular o historico,
   mas sem tentar recriar `consensos`/`probabilidades` (que dependem do
   Motor IA, inexistente no sistema antigo).
