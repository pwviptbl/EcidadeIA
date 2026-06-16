# Tabela de negocio: `cadastro.carconstr`

## Identidade

- Nome humano: caracteristicas vinculadas a construcoes.
- O que representa: cada linha associa uma caracteristica cadastrada a uma construcao de uma matricula.
- Quando usar:
  - listar caracteristicas de construcoes;
  - contar construcoes por caracteristica;
  - identificar uso real de uma caracteristica em construcoes;
  - cruzar caracteristicas com cadastro mestre em `caracter`.
- Quando evitar:
  - para listar caracteristicas cadastradas sem uso, usar `cadastro.caracter`;
  - para area, data ou status da construcao, usar `cadastro.iptuconstr`;
  - para caracteristicas de lote, usar `cadastro.carlote`.

## Grao e chaves

- Grao: uma linha por matricula, construcao e caracteristica.
- Entidade principal: vinculo construcao-caracteristica.
- Chave de negocio:
  - `j48_matric`
  - `j48_idcons`
  - `j48_caract`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j48_matric`: matricula.
- `j48_idcons`: identificador da construcao.
- `j48_caract`: codigo da caracteristica.

## Dimensoes relacionadas

- Caracteristica: via `carconstr.j48_caract -> caracter.j31_codigo`.
- Grupo/tipo da caracteristica: via `caracter.j31_grupo -> cargrup.j32_grupo`.
- Construcao fisica: via `j48_matric, j48_idcons -> iptuconstr.j39_matric, j39_idcons`.

## Filtros de negocio

- Matricula: `j48_matric`.
- Construcao: `j48_matric` e `j48_idcons`.
- Caracteristica: `j48_caract`.
- Caracteristica de construcao: confirmar em `cargrup.j32_tipo = 'C'` quando a pergunta exigir separar tipo.
- Construcao ativa: cruzar com `iptuconstr` e aplicar `j39_dtdemo IS NULL`.

## Regra de contagem

- Para contar vinculos de caracteristicas, contar linhas de `carconstr`.
- Para contar construcoes por caracteristica nesse grao, `COUNT(1)` e adequado quando nao houver join que multiplique o vinculo.
- Para contar imoveis por caracteristica, usar `COUNT(DISTINCT j48_matric)`.
- Se juntar com outras tabelas de detalhe, proteger o grao `j48_matric, j48_idcons, j48_caract`.

## Regra de agregacao

- Agrupar por `j48_caract` ou pela descricao em `caracter.j31_descr` para relacao por caracteristica.
- Quando descricoes forem duplicadas ou genericas, incluir tambem o codigo `j31_codigo`.

## Relacionamentos importantes

- `carconstr.j48_caract = caracter.j31_codigo`
- `caracter.j31_grupo = cargrup.j32_grupo`
- `carconstr.j48_matric = iptuconstr.j39_matric`
- `carconstr.j48_idcons = iptuconstr.j39_idcons`

## Riscos de duplicidade

- Uma construcao pode ter varias caracteristicas.
- Uma matricula pode ter varias construcoes.
- Descricoes de caracteristicas podem se repetir conforme parametrizacao local.

## O que nao inferir

- Nao contar linhas de `caracter` para medir uso real.
- Nao assumir que toda caracteristica e de construcao sem validar grupo quando a pergunta pedir separacao.
- Nao inferir impacto financeiro sem cruzar com regra de calculo.

## Cuidados

- Caracteristicas sao parametrizaveis por municipio.
- O mesmo codigo ou descricao deve ser interpretado dentro da base analisada.
