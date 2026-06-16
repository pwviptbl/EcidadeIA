# Fase 2

Objetivo: compilar o plano validado em SQL auditavel.

Entrada:

- resultado da Fase 1;
- `intent_spec`;
- `business_spec`;
- `schema_plan` validado.

Saida:

- `sql_artifact` com operacao, SQL, tabelas, joins, filtros e metricas.

Escopo inicial:

- `compare_periods`;
- `count_by_dimension`;
- `sum_by_dimension`;
- `detail_listing`.

Regra:

- nao usar SQL pronto por pergunta;
- nao executar banco ainda;
- manter o SQL somente como artefato auditavel.

Exemplo:

```bash
cd /home/dbseller/Modelos/MVP
python3 agenteV2/run_phase2.py "Compare o IPTU 2025 e 2026 e explique os principais fatores de aumento"
```
