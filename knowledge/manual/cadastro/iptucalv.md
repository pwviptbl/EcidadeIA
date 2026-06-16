# Tabela de negocio: `cadastro.iptucalv`

## Identidade

- Nome humano: valores gerados no calculo do IPTU.
- O que representa: cada linha representa um valor calculado para uma matricula em um exercicio, associado a receita e historico de calculo.
- Quando usar:
  - soma de IPTU calculado;
  - comparacao de valores calculados entre exercicios;
  - composicao do calculo por historico/receita;
  - ligacao entre calculo de IPTU e debito gerado.
- Quando evitar:
  - para pagamento/arrecadacao efetiva, usar tabelas de arrecadacao;
  - para parametros fisicos do calculo, usar `cadastro.iptucalc` ou `cadastro.iptucale`;
  - para contar imoveis cadastrados, usar `cadastro.iptubase`.

## Grao e chaves

- Grao: uma linha por matricula, exercicio, receita e historico de calculo.
- Entidade principal: valor calculado por matricula/exercicio/historico.
- Chave de negocio recomendada:
  - `j21_anousu`
  - `j21_matric`
  - `j21_receit`
  - `j21_codhis`
- Coluna temporal:
  - `j21_anousu`

## Colunas principais

- `j21_anousu`: exercicio do calculo.
- `j21_matric`: matricula do imovel.
- `j21_receit`: codigo da receita.
- `j21_codhis`: codigo do historico do calculo.
- `j21_valor`: valor calculado.
- `j21_quant`: quantidade associada ao valor, quando aplicavel.

## Metricas atomicas

- `valor_calculado`: `j21_valor`, agregacao comum `sum`, significado depende do historico/receita.
- `quantidade_calculo`: `j21_quant`, agregacao depende da regra municipal e nao deve ser somada sem validar.

## Filtros de negocio

- Exercicio: `j21_anousu`.
- Matricula: `j21_matric`.
- Receita: `j21_receit`.
- Historico: `j21_codhis`.
- Regra catalogada: `historico_iptu_local`.
  - table: `cadastro.iptucalh`
  - column: `j17_descr`
  - operator: `CONTAINS`
  - value: `iptu`
  - observacao: a descricao do historico pode variar entre municipios e incluir IPTU, taxa de lixo, isencao ou desconto.
- Somente IPTU: classificar por `cadastro.iptucalh` usando `j21_codhis`.

## Classificacao obrigatoria

- `iptucalv` pode misturar IPTU, taxas, isencoes e outros componentes.
- Para responder "IPTU", nao usar `j21_valor` cru.
- Caminho recomendado:
  - `iptucalv.j21_codhis -> iptucalh.j17_codhis`
  - validar descricao ou regra local do historico para identificar IPTU.
- Em perguntas de valor calculado, `iptubase.j01_baixa` nao e filtro obrigatorio; use-o apenas quando a pergunta pedir imoveis ativos.
- A classificacao do historico deve ser lida como regra local do municipio; `j17_descr` pode representar IPTU, taxa de lixo, isencao ou desconto.

## Regra de contagem

- Linhas de `iptucalv` nao sao imoveis.
- Para contar imoveis com valor calculado, usar `COUNT(DISTINCT j21_matric)` no recorte correto.
- Para quantidade de componentes/historicos, contar linhas ou historicos conforme a pergunta.

## Regra de agregacao

- Para soma de IPTU por ano, agregar `j21_valor` por `j21_anousu` apos filtro de historico/receita de IPTU.
- Para comparacao entre anos, manter o exercicio como eixo temporal.
- Para explicar fatores de aumento, usar `iptucalv` para valor final e `iptucalc` para parametros do calculo.

## Relacionamentos importantes

- `iptucalv.j21_matric = iptubase.j01_matric`
- `iptucalv.j21_codhis = iptucalh.j17_codhis`
- `iptucalv.j21_anousu = iptucalc.j23_anousu` e `iptucalv.j21_matric = iptucalc.j23_matric`, quando comparar valor final com parametros do calculo.
- `iptucalv.j21_anousu = iptunump.j20_anousu` e `iptucalv.j21_matric = iptunump.j20_matric`, quando precisar chegar ao debito/numpre.

## Riscos de duplicidade

- Uma matricula pode ter varias linhas no mesmo exercicio.
- Join com `iptubase` nao multiplica por si so, mas join com historicos, receitas ou debitos pode alterar o grao.
- Se cruzar com construcoes ou caracteristicas, preferir agregacao previa por matricula/exercicio para nao multiplicar valores.

## O que nao inferir

- Nao inferir pagamento, arrecadacao ou inadimplencia a partir de `iptucalv`.
- Nao inferir que todo `j21_valor` e IPTU.
- Nao explicar aumento por inflacao, lei ou recadastramento sem dados retornados.

## Cuidados

- Valor negativo pode representar isencao ou ajuste, dependendo do historico e regras locais.
- Receita e historico respondem classificacoes diferentes; quando a pergunta for "somente IPTU", o historico costuma ser o caminho mais seguro se estiver documentado.
