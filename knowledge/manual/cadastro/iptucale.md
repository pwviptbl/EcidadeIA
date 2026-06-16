# Tabela de negocio: `cadastro.iptucale`

## Identidade

- Nome humano: calculo venal por edificacao/construcao.
- O que representa: cada linha representa o resultado de calculo de uma construcao de uma matricula em um exercicio.
- Quando usar:
  - valor venal edificado por construcao;
  - area edificada usada no calculo por construcao;
  - pontos e valor de metro quadrado da construcao;
  - explicar composicao edificada do calculo.
- Quando evitar:
  - para cadastro fisico atual da construcao, usar `iptuconstr`;
  - para valor final do IPTU, usar `iptucalv`;
  - para parametros gerais da matricula, usar `iptucalc`.

## Grao e chaves

- Grao: uma linha por exercicio, matricula e construcao calculada.
- Entidade principal: calculo de edificacao.
- Chave de negocio:
  - `j22_anousu`
  - `j22_matric`
  - `j22_idcons`
- Coluna temporal:
  - `j22_anousu`

## Colunas principais

- `j22_anousu`: exercicio do calculo.
- `j22_matric`: matricula.
- `j22_idcons`: identificador da construcao.
- `j22_areaed`: area edificada processada no calculo.
- `j22_pontos`: pontuacao calculada.
- `j22_valor`: valor venal calculado da edificacao.
- `j22_vm2`: valor do metro quadrado da construcao usado no calculo.

## Metricas atomicas

- `valor_venal_edificacao`: `j22_valor`, agregacao comum `sum`.
- `area_edificada_calculo`: `j22_areaed`, agregacao comum `sum`.
- `pontos_construcao`: `j22_pontos`, agregacao depende da pergunta.
- `valor_m2_construcao`: `j22_vm2`, agregacao comum `avg` ou distribuicao.

## Filtros de negocio

- Exercicio: `j22_anousu`.
- Matricula: `j22_matric`.
- Construcao: `j22_idcons`.

## Regra de contagem

- Contar linhas de `iptucale` conta construcoes calculadas por exercicio.
- Para contar imoveis com edificacao calculada, usar `COUNT(DISTINCT j22_matric)`.
- Para contar construcoes distintas, usar combinacao `j22_matric, j22_idcons` no exercicio.

## Regra de agregacao

- Valor venal edificado total da matricula: somar `j22_valor` por `j22_anousu, j22_matric`.
- Area edificada calculada total da matricula: somar `j22_areaed` por `j22_anousu, j22_matric`.
- Para comparacao anual, manter `j22_anousu` no agrupamento.

## Relacionamentos importantes

- `iptucale.j22_matric = iptubase.j01_matric`
- `iptucale.j22_anousu = iptucalc.j23_anousu`
- `iptucale.j22_matric = iptucalc.j23_matric`
- `iptucale.j22_matric = iptuconstr.j39_matric`
- `iptucale.j22_idcons = iptuconstr.j39_idcons`

## Riscos de duplicidade

- Uma matricula pode ter varias construcoes no mesmo exercicio.
- Join com caracteristicas pode multiplicar construcoes.

## O que nao inferir

- `j22_areaed` e area processada no calculo, nao necessariamente area cadastral atual.
- `j22_valor` e valor venal da edificacao, nao valor final do IPTU.
- `j22_vm2` e parametro de calculo, nao valor de mercado.

## Cuidados

- A chave correta inclui exercicio, matricula e construcao.
- Usar apenas matricula mistura exercicios e construcoes.
