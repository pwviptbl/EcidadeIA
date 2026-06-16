# Tabela de negocio: `cadastro.iptucalc`

## Identidade

- Nome humano: parametros principais do calculo de IPTU por matricula e exercicio.
- O que representa: resultado principal do calculo cadastral/tributario de uma matricula em um exercicio.
- Quando usar:
  - explicar variacao de IPTU entre exercicios;
  - analisar valor venal territorial, area considerada, area edificada, aliquota, isencao e tipo de imposto;
  - comparar parametros do calculo por matricula/ano.
- Quando evitar:
  - para valor final detalhado por historico/receita, usar `cadastro.iptucalv`;
  - para construcao individual, usar `cadastro.iptucale` ou `cadastro.iptuconstr`;
  - para pagamento/arrecadacao, usar tabelas financeiras de arrecadacao.

## Grao e chaves

- Grao: uma linha por exercicio e matricula calculada.
- Entidade principal: calculo de IPTU da matricula.
- Chave de negocio:
  - `j23_anousu`
  - `j23_matric`
- Coluna temporal:
  - `j23_anousu`

## Colunas principais

- `j23_anousu`: exercicio do calculo.
- `j23_matric`: matricula.
- `j23_testad`: testada usada no calculo.
- `j23_arealo`: area territorial/area calculada usada no calculo.
- `j23_areafr`: area fracionada usada no calculo.
- `j23_areaed`: area total edificada considerada.
- `j23_m2terr`: valor do metro quadrado do terreno usado no calculo.
- `j23_vlrter`: valor venal territorial calculado.
- `j23_aliq`: aliquota aplicada.
- `j23_vlrisen`: valor de isencao considerado.
- `j23_tipoim`: tipo de imposto/imovel no calculo.
- `j23_manual`: log textual do calculo.
- `j23_tipocalculo`: tipo/modalidade de calculo.

## Metricas atomicas

- `valor_venal_territorial`: `j23_vlrter`, agregacao comum `sum`.
- `valor_m2_terreno`: `j23_m2terr`, agregacao comum `avg` ou analise por faixa; nao somar sem regra.
- `area_territorial_calculo`: `j23_arealo`, agregacao comum `sum`.
- `area_fracionada_calculo`: `j23_areafr`, agregacao comum `sum`.
- `area_total_edificada_calculo`: `j23_areaed`, agregacao comum `sum`.
- `testada_calculo`: `j23_testad`, agregacao comum depende da pergunta.
- `aliquota`: `j23_aliq`, agregacao comum `avg` ou distribuicao; soma nao tem significado.
- `valor_isencao`: `j23_vlrisen`, agregacao comum `sum`.

## Filtros de negocio

- Exercicio: `j23_anousu`.
- Matricula: `j23_matric`.
- Tipo de imposto/imovel: `j23_tipoim`.
- Tipo de calculo: `j23_tipocalculo`.

## Regra de contagem

- Contar linhas de `iptucalc` conta calculos por matricula/exercicio.
- Para contar imoveis calculados em um ano, usar `COUNT(DISTINCT j23_matric)` filtrando `j23_anousu`.
- Nao contar `iptucalc` como quantidade de debitos ou quantidade de construcoes.

## Regra de agregacao

- Para quadro geral por ano, agrupar por `j23_anousu`.
- Para comparar fatores entre anos, comparar as mesmas metricas por exercicio.
- Para explicar causa de aumento, `iptucalc` fornece fatores candidatos; o valor final deve vir de `iptucalv` classificado como IPTU.

## Relacionamentos importantes

- `iptucalc.j23_matric = iptubase.j01_matric`
- `iptucalc.j23_anousu = iptucalv.j21_anousu` e `iptucalc.j23_matric = iptucalv.j21_matric`
- `iptucalc.j23_matric = iptuconstr.j39_matric`, quando precisar confrontar cadastro atual de construcoes.
- `iptucalc.j23_anousu = iptucale.j22_anousu`, `iptucalc.j23_matric = iptucale.j22_matric`, quando detalhar calculo por edificacao.

## Riscos de duplicidade

- Join com `iptucalv` pode multiplicar linhas porque `iptucalv` tem varios historicos/receitas por matricula/exercicio.
- Para comparar com valor de IPTU, agregue ou filtre `iptucalv` corretamente antes de juntar.
- Join com construcoes pode multiplicar uma linha de calculo por varias edificacoes.

## O que nao inferir

- `j23_vlrter` nao e o valor total do imovel quando ha construcao.
- `j23_areaed` e area considerada no calculo, nao necessariamente a area fisica atual em `iptuconstr`.
- `j23_m2terr` nao e valor de mercado; e parametro do calculo.
- `j23_manual` nao deve ser usado como regra estruturada sem interpretacao.

## Cuidados

- A chave correta sempre inclui exercicio e matricula.
- Consultar apenas por matricula mistura anos.
- Isencao em `j23_vlrisen` pode reduzir o IPTU final e deve ser considerada em explicacoes.
