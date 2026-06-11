# Fluxo do Agente

## 1. Entrada

O endpoint do chat recebe a pergunta e cria um evento `handle.start`.

## 2. Busca inicial no catalogo

O agente chama:

```text
ecidade_catalog_search
```

Essa busca retorna tabelas candidatas e evidencias RAG, incluindo:

- `business_rule`
- `classification`
- `filter_semantics`
- `validated_query`
- `grouping_rule`
- `markdown_rule`
- `markdown_sql`
- `markdown_reference`

## 3. Rota

A rota pode ser decidida por:

- atalho de `validated_query`, quando a evidencia e forte;
- selecao por LLM, quando a pergunta e aberta;
- reparo de selecao, quando a LLM escolhe tabela fraca mas o catalogo tem evidencia forte.

## 4. Contexto

O contexto para SQL deve conter somente o que ajuda a consulta:

- tabelas selecionadas;
- colunas;
- grao;
- chaves;
- regras de filtro;
- classificacoes por historico/receita;
- consultas validadas;
- relacionamentos confirmados.

## 5. SQL

Ordem recomendada:

1. Plano deterministico para perguntas conhecidas.
2. Consulta validada do catalogo/RAG.
3. LLM gerando SQL com contexto compacto.

Para IPTU, a regra ja validada e:

```sql
select coalesce(sum(v.j21_valor), 0) as total_valor
from cadastro.iptucalv v
join cadastro.iptucalh h on h.j17_codhis = v.j21_codhis
where v.j21_anousu = 2025
  and position('iptu' in lower(h.j17_descr)) > 0
```

Evitar `LIKE '%IPTU%'` neste fluxo porque o caminho atual do MCP pode interpretar `%I` como placeholder.

## 6. Execucao

O MCP valida:

- somente `SELECT` ou `WITH`;
- uma unica statement;
- schemas permitidos;
- tabelas existentes no catalogo;
- limite de linhas;
- transacao read-only.

## 7. Resposta

A LLM de resposta deve explicar apenas os dados retornados pela query executada.
