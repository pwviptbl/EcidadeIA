# Tabela de negocio: `cadastro.iptubase`

## Identidade

- Nome humano: cadastro principal da matricula imobiliaria.
- O que representa: cada linha representa uma matricula/imovel no cadastro imobiliario.
- Quando usar:
  - perguntas sobre imoveis, matriculas, proprietario principal, lote vinculado ou situacao cadastral;
  - ponto de partida para ligar o cadastro imobiliario a lote, bairro, construcoes e calculos de IPTU;
  - filtro de matriculas ativas.
- Quando evitar:
  - para valor calculado de IPTU, usar `cadastro.iptucalv` e classificar o historico;
  - para parametros do calculo, usar `cadastro.iptucalc`;
  - para construcoes, usar `cadastro.iptuconstr`.

## Grao e chaves

- Grao: uma linha por matricula imobiliaria.
- Entidade principal: matricula/imovel.
- Chave de negocio:
  - `j01_matric`
- Coluna temporal:
  - `j01_baixa`, como indicativo de baixa cadastral; nao representa data de criacao do imovel.

## Colunas principais

- `j01_matric`: matricula do imovel.
- `j01_numcgm`: CGM do contribuinte/proprietario principal.
- `j01_idbql`: identificador do lote vinculado.
- `j01_baixa`: data de baixa; `NULL` indica matricula ativa.
- `j01_fracao`: fracao ideal da matricula.
- `j01_tipoimovel`: tipo de imovel, quando preenchido.
- `j01_situcad`: situacao cadastral textual/local.

## Filtros de negocio

- Matricula ativa: `j01_baixa IS NULL`.
- Matricula baixada: `j01_baixa IS NOT NULL`.
- Lote especifico: `j01_idbql = :idbql`.
- Proprietario principal: `j01_numcgm = :numcgm`.

## Dimensoes relacionadas

- Bairro do imovel: via `iptubase.j01_idbql -> lote.j34_idbql -> bairro.j13_codi`.
- Lote: via `iptubase.j01_idbql -> lote.j34_idbql`.
- Construcoes: via `iptubase.j01_matric -> iptuconstr.j39_matric`.
- Valores calculados de IPTU: via `iptubase.j01_matric -> iptucalv.j21_matric`.
- Parametros do calculo: via `iptubase.j01_matric -> iptucalc.j23_matric`.
- Proprietarios/coproprietarios: `propri` e tabelas de titularidade, quando a pergunta pedir titularidade completa.

## Regra de contagem

- Para contar matriculas diretamente em `iptubase`, `COUNT(1)` conta registros de matricula.
- Para contar imoveis ativos, aplicar `j01_baixa IS NULL`.
- Se houver join com construcoes, caracteristicas, valores ou proprietarios, usar `COUNT(DISTINCT j01_matric)` para evitar multiplicacao.
- `j01_idbql` pode se repetir em mais de uma matricula; para contar lotes, usar chave de lote e nao matricula.

## Regra de agregacao

- Agregacoes por bairro, setor, lote ou valores devem respeitar o grao da tabela agregada.
- Ao agregar valores de IPTU, nao somar campos de `iptubase`; ela e dimensao/cadastro, nao fato financeiro.

## Relacionamentos importantes

- `iptubase.j01_idbql = lote.j34_idbql`
- `lote.j34_bairro = bairro.j13_codi`
- `iptubase.j01_matric = iptuconstr.j39_matric`
- `iptubase.j01_matric = iptucalc.j23_matric`
- `iptubase.j01_matric = iptucalv.j21_matric`
- `iptubase.j01_matric = propri.j42_matric`, quando precisar coproprietarios.
- `iptubase.j01_matric = promitente.j41_matric`, quando precisar promitentes.

## Riscos de duplicidade

- Uma matricula pode ter varias construcoes.
- Uma matricula pode ter varias linhas de valores calculados por exercicio/historico/receita.
- Uma matricula pode ter mais de um proprietario/coparticipante.
- Um lote pode estar ligado a mais de uma matricula.

## O que nao inferir

- Nao inferir valor de IPTU a partir de `iptubase`.
- Nao inferir matricula ativa apenas por existir calculo em determinado ano.
- Nao usar `j01_numcgm` sozinho como titularidade completa quando a pergunta pedir todos os proprietarios.
- Nao usar `j01_idbql` como matricula.

## Cuidados

- `iptubase` e a tabela central para localizar a matricula e conectar outras entidades.
- Para analise fisica do imovel, combinar com lote, construcoes, testadas, bairro, setor e caracteristicas.
- Para analise financeira/tributaria, combinar com `iptucalc`, `iptucalv`, `iptunump` e historicos conforme a pergunta.
