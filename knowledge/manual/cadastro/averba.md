# Tabela de negocio: `cadastro.averba`

## Identidade

- Nome humano: averbacoes da matricula imobiliaria.
- O que representa: cada linha registra uma averbacao vinculada a uma matricula, com data, registro de imovel, cidade e CGM associado.
- Quando usar:
  - listar averbacoes de uma matricula;
  - analisar eventos cartoriais associados ao imovel;
  - identificar CGM associado a uma averbacao;
  - filtrar averbacoes por periodo.
- Quando evitar:
  - para titularidade atual completa, usar tambem `iptubase`, `propri`, `promitente` e regras de titularidade;
  - para afirmar transferencia efetiva de propriedade sem regra funcional adicional.

## Grao e chaves

- Grao: uma linha por averbacao.
- Entidade principal: averbacao.
- Chave de negocio:
  - `j55_codave`
- Coluna temporal:
  - `j55_data`

## Colunas principais

- `j55_codave`: codigo da averbacao.
- `j55_matric`: matricula.
- `j55_data`: data da averbacao.
- `j55_regimo`: registro de imovel.
- `j55_cidade`: cidade do registro.
- `j55_numcgm`: CGM associado a averbacao.

## Filtros de negocio

- Matricula: `j55_matric`.
- CGM: `j55_numcgm`.
- Periodo: `j55_data`.
- Codigo da averbacao: `j55_codave`.

## Regra de contagem

- Contar linhas de `averba` conta averbacoes.
- Para contar matriculas com averbacao, usar `COUNT(DISTINCT j55_matric)`.
- Para contar CGMs envolvidos, usar `COUNT(DISTINCT j55_numcgm)`.

## Relacionamentos importantes

- `averba.j55_matric = iptubase.j01_matric`
- `averba.j55_numcgm` se relaciona logicamente com CGM.
- `iptubase.j01_idbql = lote.j34_idbql`, quando precisar do lote.

## Riscos de duplicidade

- Uma matricula pode ter varias averbacoes.
- Uma consulta pode envolver dois CGMs: CGM da averbacao e CGM principal da matricula.

## O que nao inferir

- Nao inferir que `j55_numcgm` e sempre proprietario anterior.
- Nao inferir troca de titularidade apenas por existir averbacao.

## Cuidados

- Averbacao registra evento/dado cartorial, mas a regra de titularidade pode depender de outras tabelas.
