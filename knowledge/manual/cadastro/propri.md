# Tabela de negocio: `cadastro.propri`

## Identidade

- Nome humano: outros proprietarios/coparticipantes da matricula.
- O que representa: cada linha registra um CGM proprietario adicional ou participante associado a uma matricula.
- Quando usar:
  - listar coproprietarios de uma matricula;
  - identificar CGMs que participam da titularidade;
  - analisar fracao por proprietario;
  - complementar o proprietario principal de `iptubase`.
- Quando evitar:
  - para proprietario principal isolado, usar `iptubase.j01_numcgm`;
  - para promitentes compradores, usar `promitente`;
  - para titularidade completa sem combinar todas as fontes de envolvidos.

## Grao e chaves

- Grao: uma linha por matricula e CGM proprietario.
- Entidade principal: vinculo matricula-proprietario.
- Chave de negocio:
  - `j42_matric`
  - `j42_numcgm`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j42_matric`: matricula.
- `j42_numcgm`: CGM do proprietario/coparticipante.
- `j42_fracaoproprietario`: fracao do proprietario.
- `j42_arealoteproprietario`: area do lote atribuida ao proprietario.
- `j42_tipoproprietario`: tipo de proprietario.

## Filtros de negocio

- Matricula: `j42_matric`.
- CGM: `j42_numcgm`.
- Tipo de proprietario: `j42_tipoproprietario`.

## Regra de contagem

- Contar linhas de `propri` conta vinculos matricula-proprietario.
- Para contar proprietarios distintos, usar `COUNT(DISTINCT j42_numcgm)`.
- Para contar matriculas com coproprietario, usar `COUNT(DISTINCT j42_matric)`.

## Regra de agregacao

- Fracao e area por proprietario podem ser somadas por matricula para conferir consistencia, mas nao devem ser usadas como valor financeiro.

## Relacionamentos importantes

- `propri.j42_matric = iptubase.j01_matric`
- `propri.j42_numcgm` se relaciona logicamente com CGM.
- `propri.j42_tipoproprietario` se relaciona com tipo de proprietario conforme catalogo local.

## Riscos de duplicidade

- Uma matricula pode ter varios proprietarios.
- `iptubase` tambem possui proprietario principal; unir sem cuidado pode duplicar envolvidos.

## O que nao inferir

- Nao considerar `propri` como unica fonte de titularidade.
- Nao ignorar `iptubase.j01_numcgm` quando a pergunta pedir proprietario principal.

## Cuidados

- Para titularidade completa, consolidar proprietario principal, coproprietarios e promitentes.
