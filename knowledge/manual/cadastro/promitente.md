# Tabela de negocio: `cadastro.promitente`

## Identidade

- Nome humano: promitentes vinculados a matricula.
- O que representa: cada linha registra um CGM promitente associado a uma matricula imobiliaria.
- Quando usar:
  - listar promitentes de uma matricula;
  - identificar promitente responsavel;
  - analisar fracao de promitente;
  - complementar titularidade da matricula.
- Quando evitar:
  - para proprietario principal, usar `iptubase.j01_numcgm`;
  - para coproprietarios/outros proprietarios, usar `propri`;
  - para concluir titularidade completa sem combinar as tabelas de envolvidos.

## Grao e chaves

- Grao: uma linha por matricula e CGM promitente.
- Entidade principal: vinculo matricula-promitente.
- Chave de negocio:
  - `j41_matric`
  - `j41_numcgm`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j41_matric`: matricula.
- `j41_numcgm`: CGM do promitente.
- `j41_tipopro`: indicador de responsavel/principal.
- `j41_promitipo`: abreviacao do tipo do promitente.
- `j41_tipopromitente`: tipo numerico do promitente.
- `j41_fracao`: fracao do promitente.

## Filtros de negocio

- Matricula: `j41_matric`.
- CGM: `j41_numcgm`.
- Responsavel: `j41_tipopro`.
- Tipo de promitente: `j41_promitipo` ou `j41_tipopromitente`.

## Regra de contagem

- Contar linhas de `promitente` conta vinculos matricula-promitente.
- Para contar promitentes distintos, usar `COUNT(DISTINCT j41_numcgm)`.
- Para contar matriculas com promitente, usar `COUNT(DISTINCT j41_matric)`.

## Relacionamentos importantes

- `promitente.j41_matric = iptubase.j01_matric`
- `promitente.j41_numcgm` se relaciona logicamente com CGM.
- `promitente.j41_promitipo` ou `j41_tipopromitente` se relaciona com tipo de promitente conforme catalogo local.

## Riscos de duplicidade

- Uma matricula pode ter varios promitentes.
- Join com tipo de promitente pode duplicar se houver mais de uma regra de relacionamento possivel.

## O que nao inferir

- Nao substituir proprietario principal por promitente.
- Nao inferir titularidade completa apenas por esta tabela.

## Cuidados

- Fracao pode ter regra condicional conforme responsavel/tipo.
- Para analise completa de envolvidos da matricula, combinar `iptubase`, `propri` e `promitente`.
