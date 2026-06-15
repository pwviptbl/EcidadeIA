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
- `business_concept`
- `relationship_recipe`
- `business_filter`
- `table_role`
- `counting_rule`
- `classification`
- `filter_semantics`
- `validated_query`
- `grouping_rule`
- `markdown_rule`
- `markdown_reference`

## 3. Rota

A rota pode ser decidida por:

- atalho de `validated_query`, quando a evidencia e forte e aderente;
- selecao por LLM, quando a pergunta e aberta;
- reparo de selecao, quando a LLM escolhe tabela fraca mas o catalogo tem evidencia forte;
- reforco por conceito/receita, quando uma regra de negocio cita tabelas sem `metadata.table` direto.

O ponto central agora e: a rota nao deve depender apenas de FK ou nome de
coluna. Conceitos como "matricula ativa", "construcao ativa" ou "ruas do
bairro" entram como evidencia de negocio antes da SQL.

## 4. Contexto

O contexto para SQL deve conter somente o que ajuda a consulta:

- tabelas selecionadas;
- colunas;
- grao;
- chaves;
- conceitos de negocio;
- receitas de relacionamento;
- regras de contagem;
- regras de filtro;
- classificacoes por historico/receita;
- consultas validadas;
- relacionamentos confirmados.

Exemplo: para "ruas do bairro", o contexto deve trazer `bairro`,
`ruasbairro` e `ruas` pela receita `bairro -> ruasbairro -> ruas`, mesmo que
`bairro` nao tenha FK direta para `ruas`.

## 5. Plano analitico

Modo padrao atual: conhecimento primeiro.

O agente nao usa mais `generic_sql` por padrao. Se a pergunta nao tiver plano
deterministico ou regra executavel validada, ele para depois do contexto e
devolve:

- intent detectada;
- tabelas selecionadas e expandidas;
- evidencias de negocio usadas;
- `query_spec` estruturado;
- lacunas de curadoria antes de executar.

Antes de pensar em SQL, o agente deve produzir um plano intermediario:

- intent;
- entidade principal;
- grao;
- eixo temporal;
- medida final;
- fatores explicativos;
- filtros obrigatorios;
- caminho de relacionamento;
- forma esperada da resposta.

Ordem recomendada quando a execucao estiver habilitada:

1. `query_spec` coerente com a regra de negocio.
2. Compilador deterministico de SQL a partir do `query_spec`.
3. Consulta validada do catalogo/RAG quando existir como regra reutilizavel.
4. LLM gerando SQL com contexto compacto somente se `AGENTE_ALLOW_GENERIC_SQL=true`.

Antes de gerar SQL, o agente deve interpretar:

- qual conceito de negocio foi citado;
- qual entidade esta sendo contada, somada, ranqueada ou detalhada;
- qual caminho entre entidades e valido;
- qual filtro de negocio muda o grao ou evita duplicidade.

Evitar `LIKE '%IPTU%'` neste fluxo porque o caminho atual do MCP pode interpretar `%I` como placeholder.

## 6. Execucao

Se `AGENTE_ALLOW_GENERIC_SQL=false` e nao houver plano deterministico, nao ha
execucao no MCP. Isso e intencional enquanto o catalogo de conhecimento estiver
sendo enriquecido.

Antes de executar no MCP, o agente faz validação semântica contra o contexto de
catálogo. Se a SQL usar coluna fora do contexto, esquecer tabela de
classificação ou não respeitar comparação entre períodos, o planner tenta gerar
outra SQL passando o erro anterior para a IA.

O MCP valida:

- somente `SELECT` ou `WITH`;
- uma unica statement;
- schemas permitidos;
- tabelas existentes no catalogo;
- limite de linhas;
- transacao read-only.

## 7. Resposta

A LLM de resposta deve explicar apenas os dados retornados pela query executada.

A resposta deve manter a parte principal limpa e anexar a fonte em bloco
recolhivel/consultavel quando houver SQL:

- SQL usado;
- limite usado;
- tentativas, quando houver mais de uma;
- aviso se a consulta foi fallback ou se houve reparo.
