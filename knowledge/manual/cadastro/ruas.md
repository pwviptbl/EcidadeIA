# Tabela de negocio: `cadastro.ruas`

## Identidade

- Nome humano: cadastro de ruas/logradouros.
- O que representa: cada linha representa um logradouro cadastrado.
- Quando usar:
  - listar ruas/logradouros;
  - buscar rua por nome ou codigo;
  - listar ruas de um bairro via `ruasbairro`;
  - enriquecer localizacao de lote/testada.
- Quando evitar:
  - para descobrir bairro sem usar tabela de vinculo ou caminho documentado;
  - para contar imoveis por rua sem passar por testada/lote/matricula conforme a regra local.

## Grao e chaves

- Grao: uma linha por logradouro.
- Entidade principal: rua/logradouro.
- Chave de negocio:
  - `j14_codigo`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j14_codigo`: codigo do logradouro.
- `j14_nome`: nome do logradouro, quando disponivel no catalogo local.
- `j14_tipo`: tipo do logradouro, quando usado.

## Filtros de negocio

- Rua por codigo: `j14_codigo`.
- Rua por nome: coluna de nome/descricao existente no catalogo local.
- Tipo de logradouro: `j14_tipo`, quando precisar separar rua, avenida etc.

## Regra de contagem

- Contar linhas de `ruas` conta logradouros cadastrados.
- Para contar ruas por bairro, usar `ruasbairro` e contar `COUNT(DISTINCT ruas.j14_codigo)`.
- Para contar imoveis por rua, precisa de caminho via testada/lote/matricula documentado.

## Regra de agregacao

- Agrupar por codigo e nome para evitar mistura de logradouros com nomes iguais.

## Relacionamentos importantes

- `ruas.j14_codigo = ruasbairro.j16_lograd`
- `ruasbairro.j16_bairro = bairro.j13_codi`
- `ruas.j14_codigo` pode se relacionar com face/testada conforme caminho cadastral documentado.

## Riscos de duplicidade

- Uma rua pode pertencer a mais de um bairro.
- Nomes de ruas podem se repetir.

## O que nao inferir

- Nao usar `bairro` direto para chegar em `ruas`; usar `ruasbairro`.
- Nao assumir que nome de rua e unico.

## Cuidados

- Para perguntas por bairro, a receita de negocio correta e `bairro_para_ruas`.
