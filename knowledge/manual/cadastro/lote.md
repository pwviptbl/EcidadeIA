# Tabela de negocio: `cadastro.lote`

## Identidade

- Nome humano: cadastro de lotes/terrenos.
- O que representa: cada linha representa um lote territorial identificado por `j34_idbql`.
- Quando usar:
  - ligar matriculas a bairro, setor, zona e quadra/lote;
  - analisar dimensoes territoriais do imovel;
  - contar lotes;
  - chegar em caracteristicas territoriais via `carlote`.
- Quando evitar:
  - para contar matriculas sem considerar que um lote pode ter mais de uma matricula;
  - para valor calculado de IPTU, usar tabelas de calculo/valor;
  - para construcoes, usar `iptuconstr`.

## Grao e chaves

- Grao: uma linha por lote.
- Entidade principal: lote/terreno.
- Chave de negocio:
  - `j34_idbql`
- Coluna temporal:
  - nao informada como padrao geral.

## Colunas principais

- `j34_idbql`: identificador do lote.
- `j34_bairro`: bairro do lote.
- `j34_setor`: setor cadastral/fiscal.
- `j34_zona`: zona de valor, quando aplicavel.
- `j34_quadra`: quadra.
- `j34_lote`: identificacao do lote.

## Filtros de negocio

- Lote especifico: `j34_idbql`.
- Bairro: `j34_bairro`.
- Setor: `j34_setor`.
- Zona: `j34_zona`.
- Quadra/lote: colunas locais de quadra e lote.

## Regra de contagem

- Para contar lotes, usar `COUNT(DISTINCT j34_idbql)`.
- Para contar matriculas associadas a lotes, cruzar com `iptubase` e contar `COUNT(DISTINCT j01_matric)`.
- Nao contar lotes usando `iptubase.j01_matric`.

## Regra de agregacao

- Agregacoes territoriais por bairro, setor ou zona devem partir do grao de lote ou matricula conforme a pergunta.
- Para valores de IPTU por lote/bairro, agregar valores por matricula antes de agrupar dimensoes quando houver risco de multiplicacao.

## Relacionamentos importantes

- `lote.j34_idbql = iptubase.j01_idbql`
- `lote.j34_bairro = bairro.j13_codi`
- `lote.j34_idbql = carlote.j35_idbql`
- `lote.j34_setor = setor.j30_codi`, quando `setor` estiver no contexto.

## Riscos de duplicidade

- Um lote pode estar ligado a uma ou mais matriculas.
- Um lote pode ter varias caracteristicas.
- Um lote pode ter varias testadas.

## O que nao inferir

- Nao tratar lote e matricula como a mesma entidade.
- Nao inferir bairro por texto livre sem usar `bairro`.
- Nao inferir valor de IPTU diretamente do lote.

## Cuidados

- Em analises de imoveis, confirme se a pergunta quer lote territorial ou matricula imobiliaria.
