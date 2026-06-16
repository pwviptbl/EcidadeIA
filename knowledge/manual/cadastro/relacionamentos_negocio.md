# Relacionamentos de negocio - Cadastro imobiliario

Este arquivo documenta caminhos semanticos entre entidades. Use quando a FK isolada nao explica o caminho que o usuario espera.

## Receita de relacionamento: bairro_para_ruas

- Quando usar: perguntas sobre ruas, logradouros ou quantidade de ruas de um bairro.
- Origem de negocio: bairro.
- Destino de negocio: rua/logradouro.
- Tabelas no caminho:
  - `cadastro.bairro`
  - `cadastro.ruasbairro`
  - `cadastro.ruas`
- Caminho de negocio:
  - bairro -> ruasbairro -> ruas
- Join logico:
  - `bairro.j13_codi = ruasbairro.j16_bairro`
  - `ruasbairro.j16_lograd = ruas.j14_codigo`
- Cardinalidade: um bairro pode ter varias ruas; uma rua pode aparecer em mais de um bairro conforme cadastro local.
- Filtros recomendados:
  - Nome do bairro em `bairro.j13_descr`.
  - Codigo da rua em `ruas.j14_codigo`.
- Cuidados:
  - `bairro` nao possui FK direta para `ruas`; a ponte correta e `ruasbairro`.
  - Nao usar apenas `ruas.j14_bairro` como regra normalizada sem validar.

## Receita de relacionamento: bairro_para_imoveis

- Quando usar: perguntas de matriculas, imoveis, lotes ou IPTU por bairro.
- Origem de negocio: bairro.
- Destino de negocio: matricula/imovel.
- Tabelas no caminho:
  - `cadastro.bairro`
  - `cadastro.lote`
  - `cadastro.iptubase`
- Caminho de negocio:
  - bairro -> lote -> iptubase
- Join logico:
  - `bairro.j13_codi = lote.j34_bairro`
  - `lote.j34_idbql = iptubase.j01_idbql`
- Cardinalidade: um bairro possui varios lotes; um lote pode estar ligado a uma ou mais matriculas.
- Filtros recomendados:
  - Matriculas ativas: `iptubase.j01_baixa IS NULL`.
- Cuidados:
  - Para contar imoveis por bairro, usar `COUNT(DISTINCT iptubase.j01_matric)` quando houver joins com tabelas de detalhe.

## Receita de relacionamento: bairro_para_valores_iptu

- Quando usar: perguntas de soma, ranking ou comparacao de IPTU por bairro.
- Origem de negocio: bairro.
- Destino de negocio: valor calculado de IPTU.
- Tabelas no caminho:
  - `cadastro.bairro`
  - `cadastro.lote`
  - `cadastro.iptubase`
  - `cadastro.iptucalv`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - bairro -> lote -> iptubase -> iptucalv -> iptucalh
- Join logico:
  - `bairro.j13_codi = lote.j34_bairro`
  - `lote.j34_idbql = iptubase.j01_idbql`
  - `iptubase.j01_matric = iptucalv.j21_matric`
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- Filtros recomendados:
  - Exercicio: `iptucalv.j21_anousu = :ano`.
  - Somente IPTU: `position('iptu' in lower(iptucalh.j17_descr)) > 0`.
  - Matriculas ativas: `iptubase.j01_baixa IS NULL`.
- Cuidados:
  - Nao somar `iptucalv.j21_valor` sem classificar o historico.
  - Se filtrar construcoes, preferir `EXISTS` para nao multiplicar o valor calculado.

## Receita de relacionamento: bairro_para_ranking_iptu

- Quando usar: perguntas de maior/menor IPTU por bairro, top N de bairros ou ranking territorial do IPTU.
- Origem de negocio: bairro.
- Destino de negocio: valor calculado de IPTU por bairro.
- Tabelas no caminho:
  - `cadastro.bairro`
  - `cadastro.lote`
  - `cadastro.iptubase`
  - `cadastro.iptucalv`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - bairro -> lote -> iptubase -> iptucalv -> iptucalh
- Join logico:
  - `bairro.j13_codi = lote.j34_bairro`
  - `lote.j34_idbql = iptubase.j01_idbql`
  - `iptubase.j01_matric = iptucalv.j21_matric`
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- Filtros recomendados:
  - Exercicio: `iptucalv.j21_anousu = :ano`.
  - Somente IPTU: `position('iptu' in lower(iptucalh.j17_descr)) > 0`.
  - Matriculas ativas: `iptubase.j01_baixa IS NULL`, se a pergunta pedir imoveis ativos.
- Regra de ranking:
  - Agrupar por `bairro.j13_codi` e `bairro.j13_descr`.
  - Ordenar por `SUM(iptucalv.j21_valor)` em ordem decrescente.
  - Para o maior IPTU, usar `LIMIT 1` ou `FETCH FIRST 1 ROW ONLY`.
- Cuidados:
  - Nao usar apenas `bairro` para ranking; o valor vem de `iptucalv` com classificacao de `iptucalh`.
  - Nao explicar o resultado sem o filtro de historico de IPTU.
  - Se a pergunta pedir "bairro com maior IPTU", esse caminho tem prioridade sobre listagens genéricas de bairro.

## Receita de relacionamento: matricula_para_construcoes

- Quando usar: perguntas sobre construcoes de uma matricula, area construida ou construcoes ativas.
- Origem de negocio: matricula/imovel.
- Destino de negocio: construcao.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptuconstr`
- Caminho de negocio:
  - iptubase -> iptuconstr
- Join logico:
  - `iptubase.j01_matric = iptuconstr.j39_matric`
- Filtros recomendados:
  - Construcoes ativas: `iptuconstr.j39_dtdemo IS NULL`.
  - Matriculas ativas: `iptubase.j01_baixa IS NULL`.
- Cuidados:
  - Uma matricula pode ter varias construcoes.
  - Para contar imoveis com construcao, usar `COUNT(DISTINCT iptubase.j01_matric)`.

## Receita de relacionamento: construcao_para_caracteristicas

- Quando usar: perguntas sobre caracteristicas de construcoes, quantidade por caracteristica ou padrao construtivo cadastrado.
- Origem de negocio: construcao.
- Destino de negocio: caracteristica.
- Tabelas no caminho:
  - `cadastro.carconstr`
  - `cadastro.caracter`
  - `cadastro.cargrup`
  - `cadastro.iptuconstr`, somente quando precisar filtrar construcao ativa, area, data ou outro atributo fisico.
- Caminho de negocio:
  - carconstr -> caracter -> cargrup
  - carconstr -> iptuconstr, apenas para enriquecer com dados fisicos da construcao.
- Join logico:
  - `carconstr.j48_caract = caracter.j31_codigo`
  - `caracter.j31_grupo = cargrup.j32_grupo`
  - `carconstr.j48_matric = iptuconstr.j39_matric`, quando usar `iptuconstr`.
  - `carconstr.j48_idcons = iptuconstr.j39_idcons`, quando usar `iptuconstr`.
- Filtros recomendados:
  - Caracteristicas de construcao: `cargrup.j32_tipo = 'C'`, quando for necessario separar de lote/face.
  - Construcoes ativas: `iptuconstr.j39_dtdemo IS NULL`.
- Cuidados:
  - Uma construcao pode ter varias caracteristicas.
  - `caracter` e cadastro mestre; uso real esta em `carconstr`.
  - Se a pergunta pedir somente quantidade de construcoes por caracteristica e nao pedir construcao ativa, evitar join com `iptuconstr`; `carconstr` ja esta no grao `matricula, construcao, caracteristica`.
  - Para esse caso simples, `COUNT(1)` em `carconstr` agrupado pela caracteristica tende a ser mais leve que `COUNT(DISTINCT (j48_matric, j48_idcons))`.

## Receita de relacionamento: lote_para_caracteristicas

- Quando usar: perguntas sobre caracteristicas territoriais/lote.
- Origem de negocio: lote.
- Destino de negocio: caracteristica.
- Tabelas no caminho:
  - `cadastro.lote`
  - `cadastro.carlote`
  - `cadastro.caracter`
  - `cadastro.cargrup`
- Caminho de negocio:
  - lote -> carlote -> caracter -> cargrup
- Join logico:
  - `lote.j34_idbql = carlote.j35_idbql`
  - `carlote.j35_caract = caracter.j31_codigo`
  - `caracter.j31_grupo = cargrup.j32_grupo`
- Filtros recomendados:
  - Caracteristicas de lote: `cargrup.j32_tipo = 'L'`, quando for necessario separar de construcao/face.
- Cuidados:
  - Um lote pode estar vinculado a mais de uma matricula em `iptubase`.

## Receita de relacionamento: valor_iptu_para_historico

- Quando usar: perguntas sobre soma de IPTU, composicao de valores, taxa ou historico do calculo.
- Origem de negocio: valor calculado.
- Destino de negocio: historico/classificacao do valor.
- Tabelas no caminho:
  - `cadastro.iptucalv`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - iptucalv -> iptucalh
- Join logico:
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- Filtros recomendados:
  - Somente IPTU: descricao do historico contendo IPTU.
  - Exercicio: `iptucalv.j21_anousu = :ano`.
- Cuidados:
  - `iptucalv` pode misturar IPTU, taxas e outros componentes.

## Receita de relacionamento: valor_iptu_para_fatores_calculo

- Quando usar: perguntas que comparam IPTU entre exercicios e pedem explicacao dos fatores de aumento/reducao.
- Origem de negocio: valor calculado de IPTU.
- Destino de negocio: parametros/fatores do calculo.
- Tabelas no caminho:
  - `cadastro.iptucalv`
  - `cadastro.iptucalh`
  - `cadastro.iptucalc`
- Caminho de negocio:
  - iptucalv -> iptucalh, para identificar somente IPTU.
  - iptucalv -> iptucalc, para comparar parametros do calculo por matricula e exercicio.
- Join logico:
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
  - `iptucalv.j21_matric = iptucalc.j23_matric`
  - `iptucalv.j21_anousu = iptucalc.j23_anousu`
- Filtros recomendados:
  - Somente IPTU: descricao do historico contendo IPTU.
  - Exercicios: `iptucalv.j21_anousu IN (:ano_base, :ano_comparado)` e `iptucalc.j23_anousu IN (:ano_base, :ano_comparado)`.
- Metricas que devem ser comparadas:
  - Valor final do IPTU por ano: `SUM(iptucalv.j21_valor)` filtrando somente IPTU.
  - Area gerada no momento do calculo: `SUM(iptucalc.j23_arealo)`.
  - Valor do m2 usado no calculo do valor venal territorial: `AVG(iptucalc.j23_m2terr)` ou outra agregacao validada pelo municipio.
  - Area total edificada gerada no calculo: `SUM(iptucalc.j23_areaed)`.
  - Area fracionada gerada no calculo: `SUM(iptucalc.j23_areafr)`.
- Regra de leitura:
  - Primeiro identificar o valor final do IPTU por exercicio.
  - Depois comparar as metricas agregadas de `iptucalc` entre os dois anos.
  - Usar as metricas como fatores explicativos do aumento/reducao, nao como substitutas do valor final.
- Cuidados:
  - Para explicar fatores, comparar a mesma matricula entre anos.
  - Nao explicar aumento somente com total por ano; total mostra variacao, mas fatores exigem comparar campos de `iptucalc`.
  - Se incluir matriculas novas ou ausentes em um dos anos, separar esse efeito da comparacao de fatores das matriculas comuns.
