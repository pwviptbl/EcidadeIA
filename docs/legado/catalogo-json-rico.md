# Catalogo JSON Rico para Analise Semantica

## Objetivo

Este documento descreve o formato atual do catalogo JSON usado pelo MCP e pelo Agente Externo.

O foco agora e manutencao humana. Por isso, o arquivo editavel passou a usar chaves em pt-BR. O codigo do MCP e os scripts do RAG fazem a normalizacao interna para o formato consumido pelo agente.

Em resumo:

- o **catalogo editavel** fala em pt-BR;
- o **MCP** aceita tanto o formato novo quanto o legado;
- o **RAG** e gerado a partir do formato novo;
- o catalogo continua sendo a fonte de verdade semantica do dominio.

## Estrutura Geral

Formato recomendado:

```json
{
  "domain": "cadastro",
  "rotulo": "Cadastro",
  "descricao": "Descricao funcional do dominio.",
  "schema_principal": "cadastro",
  "intencoes": {},
  "metricas": {},
  "tabelas": {},
  "templates": {},
  "exemplos": []
}
```

Responsabilidade de cada bloco:

- `domain`: nome tecnico do dominio
- `rotulo`: nome amigavel do dominio
- `descricao`: resumo funcional do dominio
- `schema_principal`: schema principal no banco
- `intencoes`: tipos de perguntas que o sistema reconhece
- `metricas`: medidas de negocio reutilizaveis
- `tabelas`: tabelas com colunas, chaves e semantica local
- `templates`: modelos de consulta declarativos
- `exemplos`: perguntas de referencia

## Tabela

Formato recomendado para tabela:

```json
"cadastro.iptucalc": {
  "descricao": "Dados dos calculos de iptu.",
  "chave_primaria": ["j23_anousu", "j23_matric"],
  "grao": ["exercicio", "matricula"],
  "chave_negocio": ["j23_matric"],
  "coluna_tempo": "j23_anousu",
  "filtros_padrao": [],
  "recomendada": true,
  "apelidos": [
    "comparacao de iptu",
    "fatores de aumento do iptu"
  ],
  "colunas": {},
  "chaves_estrangeiras": []
}
```

Campos principais:

- `descricao`: explica o que a tabela representa
- `chave_primaria`: PK tecnica da tabela
- `grao`: granularidade analitica
- `chave_negocio`: coluna que identifica a entidade comparavel
- `coluna_tempo`: coluna de ano, exercicio ou data
- `filtros_padrao`: filtros sempre aplicados quando fizer sentido
- `recomendada`: favorece a tabela no ranking
- `apelidos`: formas comuns de o usuario pedir essa tabela
- `chaves_estrangeiras`: relacionamentos conhecidos

## Coluna

Formato recomendado para coluna:

```json
"j23_matric": {
  "descricao": "Matricula do imovel do arquivo iptubase.",
  "tipo": "integer",
  "papel": "chave_negocio",
  "metrica": "",
  "apelidos": [
    "matricula do imovel",
    "codigo da matricula"
  ]
}
```

Campos principais:

- `descricao`: o que a coluna guarda
- `tipo`: tipo tecnico
- `papel`: funcao da coluna no dominio
- `metrica`: nome da metrica global associada, quando existir
- `apelidos`: nomes usados por usuarios

Valores comuns para `papel`:

- `chave_negocio`
- `coluna_tempo`
- `medida`
- `dimensao`
- `filtro`
- `chave_estrangeira`

## Metrica Global

Formato recomendado:

```json
"valor_venal_terreno": {
  "rotulo": "Valor venal do terreno",
  "tabela": "cadastro.iptucalc",
  "expressao": "j23_vlrter",
  "unidade": "BRL",
  "descricao": "Valor venal do terreno usado no calculo.",
  "apelidos": [
    "valor venal do terreno",
    "fatores de aumento"
  ],
  "semantica_filtros": {}
}
```

Use `metricas` quando voce precisar nomear um conceito de negocio reaproveitavel, e nao apenas descrever uma coluna.

## Mapeamento do Legado

Os scripts e o MCP aceitam o formato antigo, mas o padrao novo e este:

- `label` -> `rotulo`
- `description` -> `descricao`
- `primary_schema` -> `schema_principal`
- `tables` -> `tabelas`
- `columns` -> `colunas`
- `primary_key` -> `chave_primaria`
- `entity_key` -> `chave_negocio`
- `time_key` -> `coluna_tempo`
- `grain` -> `grao`
- `default_filters` -> `filtros_padrao`
- `recommended` -> `recomendada`
- `semantic_role` -> `papel`
- `metric` -> `metrica`
- `question_hints` -> `apelidos`
- `foreign_keys` -> `chaves_estrangeiras`
- `references` -> `referencia`
- `referenced_columns` -> `colunas_referenciadas`
- `intents` -> `intencoes`
- `metrics` -> `metricas`
- `examples` -> `exemplos`

## Exemplo Minimo

Arquivo de referencia:

- [cadastro.exemplo.min.json](/home/dbseller/Modelos/MVP/doc/cadastro.exemplo.min.json)

Esse arquivo mostra:

- tabela de calculo de IPTU com coluna de tempo e chave de negocio
- metricas globais de valor venal e isencao
- tabela de ruas para perguntas simples de contagem

## Regra Pratica de Preenchimento

Se a pessoa estiver enriquecendo o catalogo manualmente:

1. preencher `descricao` da tabela;
2. marcar `chave_primaria`;
3. definir `chave_negocio` se houver entidade comparavel;
4. definir `coluna_tempo` se houver ano, exercicio ou data;
5. preencher `descricao`, `tipo` e `papel` das colunas principais;
6. adicionar `apelidos` quando houver linguagem comum do usuario;
7. criar `metricas` apenas quando existir conceito reutilizavel de negocio.

## Observacao de Arquitetura

O catalogo editavel foi simplificado para pessoas.

Quem faz a traducao para a estrutura interna do agente sao:

- [tools/extract_catalog.py](/home/dbseller/Modelos/MVP/tools/extract_catalog.py)
- [tools/build_rag_documents.py](/home/dbseller/Modelos/MVP/tools/build_rag_documents.py)
- [mcp/services/catalog.py](/home/dbseller/Modelos/MVP/mcp/services/catalog.py)

Isso separa duas preocupacoes:

- **edicao humana do catalogo**
- **consumo tecnico pelo MCP e pelo agente**
