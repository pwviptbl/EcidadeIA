# Arquitetura do AgenteV2

## Objetivo

Construir um agente de analise para o e-Cidade que consiga transformar perguntas
humanas em consultas seguras usando regra de negocio, catalogo e validacao
estruturada.

O objetivo nao e criar um conjunto de relatorios prontos. O objetivo e fazer o
agente raciocinar em cima de contratos:

```text
pergunta
-> intencao
-> conceitos de negocio
-> plano de esquema
-> plano analitico validado
-> SQL compilado
-> critica
-> execucao
-> resposta auditavel
```

## Fluxo

### 1. IntentExtractor

Extrai o que o usuario quer, sem escolher SQL.

Responsabilidades:

- detectar intencao: `compare_periods`, `count_by_dimension`,
  `sum_by_dimension`, `detail_listing`, `ranking`, `knowledge_review`;
- extrair anos, periodos e filtros literais;
- identificar entidade principal mencionada;
- identificar metrica pedida quando houver;
- marcar ambiguidades que precisam ser resolvidas depois.

Saida: `intent_spec`.

### 2. BusinessResolver

Resolve termos humanos usando o conhecimento curado.

Fontes:

- `knowledge/manual/<schema>/conceitos.md`;
- `knowledge/manual/<schema>/relacionamentos_negocio.md`;
- arquivos por tabela em `knowledge/manual/<schema>/<tabela>.md`;
- RAG gerado a partir dessas fontes.

Exemplos:

- "entidade ativa" -> `dim.entidade.status = 'ATIVA'`;
- "valor total" -> valor agregado em `fin.mov.valor`,
  filtrado e relacionado conforme o conhecimento estruturado;
- "caracteristica da construcao" -> caminho entre `carconstr` e `caracter`.

Saida: `business_spec`.

### 3. SchemaPlanner

Escolhe tabelas, grao, chaves e caminho de relacionamento.

Regras:

- nao gera SQL;
- nao inventa join;
- so usa relacionamento documentado no catalogo ou em receita de negocio;
- quando houver mais de um caminho possivel, explicita a escolha e o risco.

Saida: `schema_plan`.

### 4. PlanValidator

Valida se o plano e executavel antes da SQL.

Checagens minimas:

- toda tabela existe no catalogo;
- toda coluna existe no catalogo;
- toda metrica possui tabela, coluna, agregacao e significado;
- todo filtro obrigatorio foi resolvido;
- todo join esta documentado;
- grao e agregacao sao compativeis;
- risco de duplicidade foi tratado.

Saida: `validated_plan` ou lista de bloqueios.

### 5. SqlCompiler

Compila plano validado para SQL.

Operacoes iniciais:

- `compare_periods`;
- `count_by_dimension`;
- `sum_by_dimension`;
- `detail_listing`.

Regras:

- nao recebe pergunta bruta;
- nao usa SQL pronto armazenado;
- gera SQL a partir de operacoes, metricas, filtros e joins validados;
- deve produzir apenas `SELECT` ou `WITH`;
- deve manter aliases simples e auditaveis.

Saida: `sql_artifact`.

### 6. SqlCritic

Revisa a SQL antes da execucao.

Checagens:

- SQL e somente leitura;
- filtros obrigatorios foram aplicados;
- `COUNT(DISTINCT)` foi usado quando o grao exige;
- historico/classificacao foi aplicado quando a tabela mistura valores;
- joins podem multiplicar linhas;
- exercicio/periodo foi aplicado corretamente;
- limites e ordenacao fazem sentido.

Saida: SQL aprovado ou pedido de reparo.

### 7. Executor

Executa via MCP read-only.

Regras:

- nunca executa SQL fora do validador;
- aplica limite;
- registra SQL usado;
- registra linhas retornadas e erro do banco.

Saida: `execution_result`.

### 8. RepairLoop

Corrige falhas controladas.

Casos:

- coluna inexistente;
- tabela fora do contexto;
- erro de sintaxe;
- timeout;
- validacao semantica falhou;
- resultado vazio inesperado.

Limite inicial: 3 tentativas.

O reparo deve voltar para a etapa correta:

- erro de conceito -> `BusinessResolver`;
- erro de coluna/join -> `SchemaPlanner`;
- erro de SQL -> `SqlCompiler`;
- erro de risco -> `SqlCritic`.

### 9. AnswerSynthesizer

Transforma resultado em resposta humana.

Regras:

- responder a pergunta diretamente;
- explicar filtros e recortes aplicados;
- mencionar limitacoes relevantes;
- incluir fonte dos dados em bloco recolhivel;
- nunca esconder que houve fallback, reparo ou pendencia.

Saida sugerida:

- resposta curta e direta;
- bloco recolhivel com `sql` e fonte tecnica;
- payload estruturado para debug e auditoria.

## Nao Objetivos

- Nao criar relatorios fixos disfarçados de agente.
- Nao colocar SQL pronto no catalogo humano.
- Nao depender de uma unica chamada LLM para decidir tudo.
- Nao executar SQL que nao passou por plano e critica.
