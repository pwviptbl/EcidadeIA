# Tabela de negocio: `cadastro.carlote`

## Identidade

- Nome humano: caracteristicas vinculadas a lotes.
- O que representa: cada linha associa uma caracteristica cadastrada a um lote.
- Quando usar:
  - listar caracteristicas de lotes;
  - contar lotes por caracteristica;
  - filtrar lotes por atributo territorial;
  - analisar caracteristicas de lote por bairro, setor ou zona.
- Quando evitar:
  - para caracteristicas de construcao, usar `carconstr`;
  - para listar cadastro mestre de caracteristicas, usar `caracter`;
  - para contar matriculas por caracteristica sem cruzar com `iptubase`.

## Grao e chaves

- Grao: uma linha por lote e caracteristica.
- Entidade principal: vinculo lote-caracteristica.
- Chave de negocio:
  - `j35_idbql`
  - `j35_caract`
- Coluna temporal:
  - `j35_dtlanc`, data de lancamento da caracteristica no lote.

## Colunas principais

- `j35_idbql`: identificador do lote.
- `j35_caract`: codigo da caracteristica.
- `j35_dtlanc`: data de lancamento.

## Filtros de negocio

- Lote: `j35_idbql`.
- Caracteristica: `j35_caract`.
- Data de lancamento: `j35_dtlanc`.
- Caracteristica de lote: confirmar via `caracter -> cargrup` quando precisar separar tipo.

## Regra de contagem

- Para contar vinculos de caracteristicas em lotes, contar linhas de `carlote`.
- Para contar lotes com caracteristica, usar `COUNT(DISTINCT j35_idbql)`.
- Para contar matriculas com caracteristica de lote, cruzar com `iptubase` por `j01_idbql` e usar `COUNT(DISTINCT j01_matric)`.

## Regra de agregacao

- Agrupar por `j35_caract` ou por `caracter.j31_descr` para uso por caracteristica.
- Quando agrupar por descricao, incluir codigo para evitar mistura de descricoes duplicadas.

## Relacionamentos importantes

- `carlote.j35_idbql = lote.j34_idbql`
- `carlote.j35_caract = caracter.j31_codigo`
- `caracter.j31_grupo = cargrup.j32_grupo`
- `lote.j34_idbql = iptubase.j01_idbql`
- `lote.j34_bairro = bairro.j13_codi`

## Riscos de duplicidade

- Um lote pode ter varias caracteristicas.
- Um lote pode estar ligado a mais de uma matricula.
- Uma caracteristica pode aparecer em muitos lotes.

## O que nao inferir

- Nao inferir caracteristica de construcao por `carlote`.
- Nao contar matriculas sem passar por `iptubase`.
- Nao inferir regra financeira completa a partir da caracteristica.

## Cuidados

- Caracteristicas de lote sao parametrizaveis por municipio.
- `j35_dtlanc` indica lancamento cadastral da caracteristica, nao necessariamente data real da condicao fisica.
