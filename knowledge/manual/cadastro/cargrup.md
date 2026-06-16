# Tabela de negocio: `cadastro.cargrup`

## Identidade

- Nome humano: grupos de caracteristicas.
- O que representa: cada linha representa um grupo que classifica caracteristicas por contexto de uso.
- Quando usar:
  - separar caracteristicas de lote, construcao, face ou outros contextos;
  - interpretar o grupo de `caracter`;
  - contar caracteristicas por grupo.
- Quando evitar:
  - para contar uso real de caracteristicas em imoveis, usar tabelas de vinculo como `carconstr`, `carlote` ou `carface`.

## Grao e chaves

- Grao: uma linha por grupo de caracteristicas.
- Entidade principal: grupo de caracteristica.
- Chave de negocio:
  - `j32_grupo`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j32_grupo`: codigo do grupo.
- `j32_descr`: descricao do grupo.
- `j32_tipo`: tipo/contexto de aplicacao do grupo.

## Filtros de negocio

- Grupo especifico: `j32_grupo`.
- Tipo de caracteristica: `j32_tipo`.
- Descricao do grupo: `j32_descr`.

## Regra de contagem

- Contar linhas de `cargrup` conta grupos, nao caracteristicas individuais nem uso cadastral.
- Para contar caracteristicas por grupo, cruzar com `caracter`.
- Para contar construcoes/lotes/faces por grupo, cruzar com a tabela de vinculo adequada.

## Regra de agregacao

- Agrupar por `j32_grupo` e `j32_descr` para mostrar grupos.
- Para analise por tipo, agrupar por `j32_tipo`.

## Relacionamentos importantes

- `cargrup.j32_grupo = caracter.j31_grupo`
- `caracter.j31_codigo = carconstr.j48_caract`, para uso em construcoes.
- `caracter.j31_codigo = carlote.j35_caract`, para uso em lotes.

## Riscos de duplicidade

- Um grupo possui varias caracteristicas.
- Tipos podem variar conforme parametrizacao local.

## O que nao inferir

- Nao inferir uso real de caracteristicas por contar grupos.
- Nao tratar valores de `j32_tipo` como dominio universal sem validar localmente.

## Cuidados

- Valores comuns de tipo podem indicar lote, construcao, face, ITBI, obras ou agua, mas devem ser interpretados dentro da base.
