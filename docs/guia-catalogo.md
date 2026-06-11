# Guia de Conhecimento

## Onde colocar cada coisa

### JSON em `catalog/`

Use para conhecimento estruturado e pequeno:

- descricao de tabela;
- grao;
- chave primaria;
- chave de negocio;
- coluna de tempo;
- colunas;
- relacionamentos;
- filtros padrao;
- classificacao por tipo;
- consultas validadas.

Bom exemplo: `cadastro.iptucalv` informa que `j21_codhis` classifica o valor pelo historico.

### Manual humano em `knowledge/manual/`

Use para conhecimento maior e editavel por humanos:

- explicacao de regra de negocio;
- cuidados;
- exemplos SQL;
- contexto extraido de classe PHP legada;
- quando usar ou nao usar uma tabela;
- relacao funcional entre tabelas.

Bom exemplo: explicar que `j21_valor` nao e IPTU puro sem classificar por historico ou receita.

O manual completo nao entra diretamente no RAG.

### Snippets para IA em `knowledge/rag/`

Use para conhecimento curto e operacional:

- quando usar a tabela;
- quando nao usar;
- grao;
- significado de contagem;
- joins seguros;
- filtros seguros;
- regras que evitam erro de SQL ou interpretacao.

Gere snippets a partir do manual:

```bash
python3 tools/build_knowledge_rag.py
```

### RAG em `rag/`

Nao edite manualmente. Gere com:

```bash
python3 tools/build_rag_documents.py
```

## Padrao recomendado de Markdown

No manual, use o formato que for melhor para humano. No snippet operacional, prefira:

- Titulo: `# e-Cidade - Cadastro - nome_tabela`
- Secao `## Resumo para IA`
- Secao `## Regras de negocio`
- Secao `## SQL validado`
- Secao `## Relacao com outras tabelas`

Exemplo de SQL validado dentro do Markdown:

```sql
select ...
```

## Regra para consultas validadas

Quando uma pergunta vira problema recorrente, coloque a query validada no JSON estruturado ou no Markdown. Se a query precisa ser usada sem criatividade da LLM, implemente tambem um plano deterministico no agente.
