# Contratos do AgenteV2

Este documento define os objetos que passam entre as etapas. A V2 deve preferir
JSON validavel a texto livre.

## IntentSpec

```json
{
  "intent": "compare_periods",
  "confidence": 0.86,
  "years": [2025, 2026],
  "literal_filters": ["imoveis ativos"],
  "requested_entities": ["imovel"],
  "requested_metrics": ["valor de IPTU"],
  "requested_dimensions": [],
  "ambiguities": []
}
```

## BusinessSpec

```json
{
  "resolved_terms": [
    {
      "term": "imoveis ativos",
      "meaning": "matriculas imobiliarias sem baixa cadastral",
      "filter": {
        "table": "cadastro.iptubase",
        "column": "j01_baixa",
        "operator": "is_null"
      },
      "evidence": "knowledge/manual/cadastro/iptubase.md"
    }
  ],
  "metrics": [
    {
      "name": "valor_iptu",
      "meaning": "valor de IPTU gerado no calculo",
      "table": "cadastro.iptucalv",
      "column": "j21_valor",
      "aggregation": "sum",
      "required_classification": {
        "table": "cadastro.iptucalh",
        "join": "cadastro.iptucalv.j21_codhis = cadastro.iptucalh.j17_codhis",
        "filter": "descricao do historico representa IPTU"
      }
    }
  ],
  "business_risks": [
    "iptucalv mistura IPTU, taxas e outros valores",
    "joins podem multiplicar matriculas se o grao nao for respeitado"
  ]
}
```

## SchemaPlan

```json
{
  "entity": "matricula_imobiliaria",
  "grain": ["exercicio", "matricula"],
  "time_axis": {
    "table": "cadastro.iptucalv",
    "column": "j21_anousu"
  },
  "tables": [
    "cadastro.iptubase",
    "cadastro.iptucalv",
    "cadastro.iptucalh"
  ],
  "joins": [
    {
      "left_table": "cadastro.iptubase",
      "left_column": "j01_matric",
      "right_table": "cadastro.iptucalv",
      "right_column": "j21_matric",
      "kind": "inner",
      "evidence": "catalog_fk_or_relationship_recipe"
    }
  ],
  "group_by": [
    {
      "table": "cadastro.iptucalv",
      "column": "j21_anousu",
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
  "entity": "matricula_imobiliaria",
  "grain": ["exercicio"],
  "periods": [2025, 2026],
  "final_metrics": [
    {
      "name": "valor_iptu",
      "table": "cadastro.iptucalv",
      "column": "j21_valor",
      "aggregation": "sum",
      "alias": "valor_iptu"
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
