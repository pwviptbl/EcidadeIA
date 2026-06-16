# Tabela de negocio: `cadastro.bairro`

## Identidade

- Nome humano: cadastro de bairros.
- O que representa: cada linha representa um bairro cadastrado.
- Quando usar:
  - listar bairros;
  - filtrar imoveis por bairro via lote;
  - agrupar matriculas, lotes ou valores de IPTU por bairro;
  - chegar nas ruas do bairro via tabela de vinculo.
- Quando evitar:
  - para achar matriculas diretamente sem passar por lote;
  - para ruas do bairro sem usar `ruasbairro`;
  - para valores de IPTU sem passar por matricula e tabela de valores.

## Grao e chaves

- Grao: uma linha por bairro.
- Entidade principal: bairro.
- Chave de negocio:
  - `j13_codi`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j13_codi`: codigo do bairro.
- `j13_descr`: descricao/nome do bairro.

## Filtros de negocio

- Bairro por codigo: `j13_codi`.
- Bairro por nome: `j13_descr`.

## Regra de contagem

- Contar linhas de `bairro` conta bairros cadastrados.
- Para contar imoveis por bairro, cruzar com `lote` e `iptubase`, contando `COUNT(DISTINCT iptubase.j01_matric)`.
- Para contar lotes por bairro, contar `COUNT(DISTINCT lote.j34_idbql)`.
- Para contar ruas por bairro, usar `ruasbairro` e contar logradouros distintos.

## Regra de agregacao

- Para valores de IPTU por bairro, caminho recomendado:
  - `bairro -> lote -> iptubase -> iptucalv -> iptucalh`.
- Aplicar filtro de historico para IPTU antes de somar valores.
- Para maior IPTU por bairro, usar a receita `bairro_para_ranking_iptu`.

## Relacionamentos importantes

- `bairro.j13_codi = lote.j34_bairro`
- `bairro.j13_codi = ruasbairro.j16_bairro`
- `ruasbairro.j16_lograd = ruas.j14_codigo`

## Riscos de duplicidade

- Um bairro possui varios lotes.
- Um lote pode ter uma ou mais matriculas.
- Uma rua pode aparecer em mais de um bairro conforme cadastro local.

## O que nao inferir

- Nao inferir ruas do bairro direto de `bairro`; usar `ruasbairro`.
- Nao inferir valores de IPTU por bairro sem passar pela matricula/lote.
- Nao inferir ranking de IPTU por bairro sem ordenar a soma final por `iptucalv`.

## Cuidados

- Nome de bairro pode ter abreviacao, acento ou variacao local.
- Para filtros textuais, o agente deve tratar como busca por descricao, nao como codigo.
