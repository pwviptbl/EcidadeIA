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
- conceitos de negocio que o usuario cita antes de existir SQL;
- receitas de relacionamento que explicam caminhos entre entidades.

Bom exemplo: explicar que `j21_valor` nao e IPTU puro sem classificar por historico ou receita.

O manual completo nao entra diretamente no RAG.

### Rascunhos de curadoria em `docs/exemplos/obsidian/`

Use para material inicial que sera revisado fora do agente:

- catalogo tecnico exportado;
- esqueleto de conceitos de negocio;
- esqueleto de receitas de relacionamento;
- listas candidatas extraidas de FK, PK, colunas e descricoes.

Gere com:

```bash
python3 tools/run_knowledge_pipeline.py --schema cadastro --export-obsidian --skip-knowledge-rag --skip-rag-documents
```

Depois da curadoria, copie apenas secoes validadas para `knowledge/manual/`.

### Snippets para IA em `knowledge/rag/`

Use para conhecimento curto e operacional:

- quando usar a tabela;
- quando nao usar;
- grao;
- significado de contagem;
- joins seguros;
- filtros seguros;
- regras que evitam erro de SQL ou interpretacao.
- conceitos de negocio;
- receitas de relacionamento;
- regras de contagem.

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
- Secao `## Regra operacional recorrente`
- Secao `## Relacao com outras tabelas`

## Conceitos e receitas de relacionamento

Para aproximar a IA de um consultor de negocio, documente primeiro o conceito e
o caminho de negocio. A SQL deve ser consequencia desse entendimento.

Arquivos recomendados:

```text
knowledge/manual/<schema>/conceitos.md
knowledge/manual/<schema>/relacionamentos_negocio.md
```

Use `conceitos.md` para explicar termos como matricula ativa, construcao ativa,
IPTU calculado, bairro do imovel ou caracteristica da construcao.

Use `relacionamentos_negocio.md` para explicar caminhos que a FK isolada nao
deixa obvios. Exemplo: bairro nao possui FK direta para ruas; o caminho de
negocio e `bairro -> ruasbairro -> ruas`.

Modelos de preenchimento:

```text
knowledge/manual/_modelos/conceito_negocio.md
knowledge/manual/_modelos/receita_relacionamento.md
```

Arquivos em `_modelos` nao entram no RAG.

Exemplo de regra operacional recorrente dentro do Markdown:


## Regra para consultas validadas

Quando uma pergunta vira problema recorrente, registre a regra de negocio, o caminho entre entidades e os filtros obrigatorios no JSON estruturado ou no Markdown. Se a resposta precisar de execucao automatica, implemente depois um plano deterministico no agente.
