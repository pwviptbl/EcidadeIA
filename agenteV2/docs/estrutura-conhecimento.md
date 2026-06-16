# Estrutura de Conhecimento para Enriquecimento

Este documento define onde enriquecer o conhecimento do agente e o que escrever
em cada lugar. A prioridade da V2 e facilitar curadoria humana sem transformar o
sistema em um catalogo de SQL pronto.

## Regra principal

O consultor deve conseguir enriquecer a IA respondendo perguntas de negocio:

- O que este conceito significa?
- Quando usar esta tabela?
- Qual e o grao correto?
- Qual filtro de negocio e obrigatorio?
- Qual caminho liga uma entidade a outra?
- O que nao pode ser inferido?
- Qual erro comum causa numero errado?

Nao deve precisar escrever SQL.

## Onde editar

### 1. `knowledge/manual/<schema>/conceitos.md`

Use para conceitos que aparecem nas perguntas dos usuarios.

Exemplos:

- `matricula_ativa`
- `iptu_calculado`
- `comparacao_iptu_entre_exercicios`
- `caracteristica_da_construcao`
- `bairro_do_imovel`

Esse arquivo responde: "o que o usuario quis dizer?"

### 2. `knowledge/manual/<schema>/relacionamentos_negocio.md`

Use para caminhos entre entidades.

Exemplos:

- bairro -> lote -> iptubase
- iptucalv -> iptucalh
- carconstr -> caracter -> cargrup

Esse arquivo responde: "como sair de uma entidade e chegar em outra?"

### 3. `knowledge/manual/<schema>/<tabela>.md`

Use para semantica local da tabela.

Exemplos:

- grao da tabela;
- chave de negocio;
- coluna temporal;
- cuidados;
- filtros comuns;
- regra de contagem;
- quando preferir ou evitar a tabela.

Esse arquivo responde: "como usar esta tabela sem errar?"

### 4. `catalog/*.json`

Use para metadado estruturado e validavel.

Exemplos:

- tabelas;
- colunas;
- PK/FK;
- `entity_key`;
- `time_key`;
- tipos e descricoes;
- metricas atomicas se houver estrutura para isso.

Esse arquivo responde: "o campo existe e pode ser validado?"

## Onde nao editar

Nao editar manualmente:

- `knowledge/rag/*`;
- `rag/catalog_documents.jsonl`.

Eles sao saidas geradas.

## Modelo mental do agente

O `BusinessResolver` usa `conceitos.md` para resolver termos humanos.

O `SchemaPlanner` usa `relacionamentos_negocio.md` para montar caminhos entre
entidades.

O `PlanValidator` usa `catalog/*.json` e arquivos de tabela para validar
tabelas, colunas, grao, filtros e riscos.

## O que evitar

- SQL pronto.
- "Relatorio X usa a consulta Y".
- Regra incompleta sem grao.
- Join sem explicar cardinalidade.
- Filtro de negocio sem dizer quando aplicar.
- Conceito com tabela mas sem significado humano.

## Checklist de qualidade

Um conceito esta bom quando responde:

- Quais perguntas comuns ativam este conceito?
- Qual entidade principal ele representa?
- Qual o grao esperado?
- Quais tabelas participam?
- Quais filtros sao obrigatorios?
- Quais metricas ou dimensoes fazem sentido?
- O que o agente nao deve inferir?

Um relacionamento esta bom quando responde:

- Quando usar?
- Qual origem e destino de negocio?
- Quais tabelas entram no caminho?
- Quais joins logicos existem?
- Qual a cardinalidade?
- Qual filtro recomendado acompanha o caminho?
- Qual cuidado evita duplicidade ou valor errado?

Uma tabela esta boa quando responde:

- O que cada linha representa?
- Qual chave identifica a entidade?
- Qual coluna temporal existe?
- Quando usar esta tabela?
- Quando nao usar esta tabela?
- Qual contagem correta?
- Quais joins podem multiplicar linhas?
