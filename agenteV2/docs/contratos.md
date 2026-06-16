# Contratos do AgenteV2

Este documento define os objetos que passam entre as etapas. A V2 deve preferir
JSON validavel a texto livre.

## IntentSpec

```json
{
  "intent": "compare_periods",
  "confidence": 0.86,
  "years": [2025, 2026],
  "literal_filters": ["entidades ativas"],
  "requested_entities": ["entidade"],
  "requested_metrics": ["valor total"],
  "requested_dimensions": [],
  "ambiguities": []
}
```

## BusinessSpec

```json
{
  "resolved_terms": [
    {
      "term": "entidades ativas",
      "meaning": "entidades com status ativo",
      "filter": {
        "table": "dim.entidade",
        "column": "status",
        "operator": "=",
        "value": "ATIVA"
      },
      "evidence": "knowledge/manual/fin/entidade.md"
    }
  ],
  "metrics": [
    {
      "name": "valor_total",
      "meaning": "valor total registrado por exercicio",
      "table": "fin.mov",
      "column": "valor",
      "aggregation": "sum",
      "required_classification": {
        "table": "dim.entidade",
        "join": "fin.mov.entidade_id = dim.entidade.entidade_id",
        "filter": "status da entidade representa a situacao valida do registro"
      }
    }
  ],
  "business_risks": [
    "movimentos podem misturar categorias diferentes sem filtro adequado",
    "joins podem multiplicar entidades se o grao nao for respeitado"
  ]
}
```

## SchemaPlan

```json
{
  "entity": "entidade",
  "grain": ["exercicio", "entidade"],
  "time_axis": {
    "table": "fin.mov",
    "column": "ano"
  },
  "tables": [
    "fin.mov",
    "dim.entidade"
  ],
  "joins": [
    {
      "left_table": "fin.mov",
      "left_column": "entidade_id",
      "right_table": "dim.entidade",
      "right_column": "entidade_id",
      "kind": "inner",
      "evidence": "catalog_fk_or_relationship_recipe"
    }
  ],
  "group_by": [
    {
      "table": "fin.mov",
      "column": "ano",
      "alias": "exercicio"
    }
  ]
}
```

## QueryPlan

```json
{
  "operation": "compare_periods",
  "intent": "compare_periods",
  "entity": "entidade",
  "grain": ["exercicio"],
  "periods": [2025, 2026],
  "final_metrics": [
    {
      "name": "valor_total",
      "table": "fin.mov",
      "column": "valor",
      "aggregation": "sum",
      "alias": "valor_total"
    }
  ],
  "explanatory_metrics": [],
  "filters": [],
  "joins": [],
  "risks": []
}
```

## SqlArtifact

```json
{
  "sql": "select ...",
  "limit": 1000,
  "operation": "compare_periods",
  "sources": [
    "catalog/cadastro_extraido.json",
    "knowledge/manual/cadastro/conceitos.md"
  ],
  "audit": {
    "tables": [],
    "columns": [],
    "filters": [],
    "joins": []
  }
}
```

## CriticResult

```json
{
  "approved": true,
  "severity": "ok",
  "findings": [],
  "required_repairs": []
}
```

## ExecutionResult

```json
{
  "ok": true,
  "rows": [],
  "row_count": 0,
  "sql": "select ...",
  "error": null
}
```

## AnswerPayload

```json
{
  "answer": "Resposta humana.",
  "source_details": {
    "sql": "select ...",
    "tables": [],
    "filters": [],
    "limitations": []
  }
}
```
