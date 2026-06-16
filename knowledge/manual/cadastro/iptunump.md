# Tabela de negocio: `cadastro.iptunump`

## Identidade

- Nome humano: vinculo entre calculo de IPTU e numero de debito.
- O que representa: cada linha liga uma matricula e exercicio a um `numpre` usado na arrecadacao.
- Quando usar:
  - rastrear o debito gerado para uma matricula/ano;
  - sair do cadastro/calculo de IPTU para tabelas de cobranca, pagamento ou cancelamento;
  - localizar `numpre` de IPTU.
- Quando evitar:
  - para valor calculado, usar `iptucalv`;
  - para parametros do calculo, usar `iptucalc`;
  - para situacao financeira sem cruzar com arrecadacao.

## Grao e chaves

- Grao: uma linha por exercicio e matricula com numpre gerado.
- Entidade principal: debito/numpre de IPTU por matricula.
- Chave de negocio:
  - `j20_anousu`
  - `j20_matric`
- Coluna temporal:
  - `j20_anousu`

## Colunas principais

- `j20_anousu`: exercicio.
- `j20_matric`: matricula.
- `j20_numpre`: numero do debito na arrecadacao.

## Filtros de negocio

- Exercicio: `j20_anousu`.
- Matricula: `j20_matric`.
- Numpre: `j20_numpre`.

## Regra de contagem

- Contar linhas de `iptunump` conta vinculos matricula/exercicio/numpre.
- Para contar matriculas com debito gerado, usar `COUNT(DISTINCT j20_matric)` no exercicio.
- Para contar numpres, usar `COUNT(DISTINCT j20_numpre)`.

## Regra de agregacao

- `iptunump` nao possui valor; nao usar para somas financeiras.
- Usar como ponte para tabelas de arrecadacao quando a pergunta envolver cobranca/pagamento.

## Relacionamentos importantes

- `iptunump.j20_matric = iptubase.j01_matric`
- `iptunump.j20_anousu = iptucalv.j21_anousu` e `iptunump.j20_matric = iptucalv.j21_matric`
- `iptunump.j20_numpre` liga com tabelas de arrecadacao/debito conforme catalogo financeiro.

## Riscos de duplicidade

- Taxas separadas podem usar outras tabelas de numpre.
- Join com valores por historico pode multiplicar o vinculo se nao respeitar o grao.

## O que nao inferir

- Nao inferir valor do debito a partir de `j20_numpre`.
- Nao tratar `numpre` como matricula.
- Nao inferir pagamento apenas por existir numpre.

## Cuidados

- Para analise financeira completa, precisa cruzar com tabelas de arrecadacao.
- Para endereco/localizacao, preferir caminhos cadastrais documentados via `iptubase` e `lote`.
