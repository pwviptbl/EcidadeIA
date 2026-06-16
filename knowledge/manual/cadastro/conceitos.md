# Conceitos de negocio - Cadastro imobiliario

Este arquivo descreve conceitos de negocio antes de falar em SQL. Use para ensinar ao agente o significado das perguntas do usuario e os caminhos seguros para chegar nas tabelas.

## Conceito de negocio: matricula_ativa

- Nome humano: matricula imobiliaria ativa.
- Perguntas comuns:
  - Quantos imoveis ativos existem?
  - Liste matriculas ativas.
  - Some IPTU apenas de matriculas ativas.
- Significado: matricula ainda vigente no cadastro imobiliario.
- Entidade principal: matricula/imovel.
- Tabelas envolvidas:
  - `cadastro.iptubase`
- Grao esperado: uma linha por matricula em `iptubase`.
- Filtros de negocio:
  - Regra catalogada `matricula_ativa`: `iptubase.j01_baixa IS NULL`
- Regra de contagem:
  - Para contar matriculas ativas, usar `COUNT(DISTINCT j01_matric)` ou `COUNT(1)` quando a consulta partir diretamente de `iptubase` sem multiplicar por joins.
- O que nao inferir:
  - Nao inferir baixa somente por ausencia em tabelas de calculo.
  - Nao confundir matricula ativa com construcao ativa.
- Cuidados:
  - Se houver join com tabelas de valores, caracteristicas ou construcoes, usar `COUNT(DISTINCT j01_matric)` para nao multiplicar matriculas.

## Conceito de negocio: construcao_ativa

- Nome humano: construcao cadastrada sem baixa/demolicao.
- Perguntas comuns:
  - Quantas construcoes ativas existem?
  - Some area construida ativa.
  - Considere apenas construcoes sem data de baixa.
- Significado: construcao vinculada a uma matricula que nao possui data de demolicao/baixa.
- Entidade principal: construcao dentro de uma matricula.
- Tabelas envolvidas:
  - `cadastro.iptuconstr`
- Grao esperado: uma linha por `j39_matric, j39_idcons`.
- Filtros de negocio:
  - `iptuconstr.j39_dtdemo IS NULL`
- Regra de contagem:
  - Para contar construcoes, usar a combinacao `j39_matric, j39_idcons`.
  - Se a consulta parte de `iptuconstr`, `COUNT(1)` conta construcoes cadastradas.
  - Se houver join com caracteristicas, usar cuidado porque uma construcao pode ter varias caracteristicas.
- O que nao inferir:
  - Nao inferir matricula ativa apenas porque a construcao esta ativa; cruzar com `iptubase` quando a pergunta pedir matriculas ativas.

## Conceito de negocio: bairro_do_imovel

- Nome humano: bairro cadastral do lote/matricula.
- Perguntas comuns:
  - Qual bairro tem maior soma de IPTU?
  - Quantos imoveis existem por bairro?
  - Filtre imoveis do bairro Icarai.
- Significado: bairro territorial associado ao lote da matricula.
- Entidade principal: bairro como dimensao territorial do imovel.
- Tabelas envolvidas:
  - `cadastro.iptubase`
  - `cadastro.lote`
  - `cadastro.bairro`
- Grao esperado:
  - `iptubase` identifica matricula.
  - `lote` identifica o lote territorial.
  - `bairro` identifica a dimensao bairro.
- Caminho de negocio:
  - `iptubase.j01_idbql -> lote.j34_idbql`
  - `lote.j34_bairro -> bairro.j13_codi`
- Filtros de negocio:
  - Para bairro por nome, usar `bairro.j13_descr`.
- O que nao inferir:
  - Nao inventar coluna de bairro em `iptucalv`.
  - Nao usar `iptubase` isolada para nome do bairro.

## Conceito de negocio: ruas_do_bairro

- Nome humano: logradouros vinculados a um bairro.
- Perguntas comuns:
  - Quais ruas existem no bairro Icarai?
  - Liste logradouros de um bairro.
  - Quantas ruas tem cada bairro?
- Significado: rua/logradouro associado ao bairro por tabela de vinculo.
- Entidade principal: rua/logradouro.
- Tabelas envolvidas:
  - `cadastro.bairro`
  - `cadastro.ruasbairro`
  - `cadastro.ruas`
- Grao esperado:
  - `bairro` e dominio de bairro.
  - `ruas` e dominio de logradouro.
  - `ruasbairro` e vinculo entre bairro e logradouro.
- Caminho de negocio:
  - `bairro.j13_codi -> ruasbairro.j16_bairro`
  - `ruasbairro.j16_lograd -> ruas.j14_codigo`
- Regra de contagem:
  - Para contar ruas por bairro, contar logradouros distintos por `ruas.j14_codigo`.
- O que nao inferir:
  - Nao assumir que `bairro` tem FK direta para `ruas`.
  - Nao usar apenas `ruas.j14_bairro` como relacionamento normalizado sem validar a regra municipal.

## Conceito de negocio: iptu_calculado

- Nome humano: valor de IPTU gerado no calculo.
- Perguntas comuns:
  - Qual a soma do IPTU de 2025?
  - Qual bairro tem maior IPTU?
  - Some IPTU filtrando matriculas ativas.
- Significado: item de valor calculado classificado como IPTU.
- Entidade principal: valor calculado por matricula/exercicio/historico.
- Tabelas envolvidas:
  - `cadastro.iptucalv`
  - `cadastro.iptucalh`
- Grao esperado: `iptucalv` possui linhas por matricula, exercicio e historico/receita do valor.
- Caminho de negocio:
  - `iptucalv.j21_codhis -> iptucalh.j17_codhis`
- Filtros de negocio:
  - Exercicio em `iptucalv.j21_anousu`.
  - Regra catalogada `historico_iptu_local`: `iptucalh.j17_descr` com conteudo de IPTU, ou a regra local equivalente do municipio.
- Regra de contagem/soma:
  - Para somar IPTU, nao somar `j21_valor` puro por ano sem classificar o historico.
  - Usar `position('iptu' in lower(iptucalh.j17_descr)) > 0` quando o catalogo nao trouxer codigo de receita validado, ou a regra local equivalente do municipio.
- O que nao inferir:
  - Nao confundir valor calculado com valor pago/arrecadado.
  - Nao misturar IPTU, taxa de lixo, isencao e desconto sem filtro de historico/classificacao.

## Conceito de negocio: comparacao_iptu_entre_exercicios

- Nome humano: comparacao do IPTU calculado entre dois exercicios.
- Perguntas comuns:
  - Compare o IPTU de 2025 e 2026.
  - Explique os principais fatores de aumento do IPTU.
  - O que mudou no calculo do IPTU entre dois anos?
- Significado: analise da variacao do valor calculado de IPTU e dos parametros cadastrais/tributarios que podem explicar a variacao.
- Entidade principal: matricula imobiliaria comparada entre exercicios.
- Tabelas envolvidas:
  - `cadastro.iptucalv`, para valor final calculado/classificado como IPTU.
  - `cadastro.iptucalh`, para classificar historico de IPTU.
  - `cadastro.iptucalc`, para parametros e fatores do calculo por matricula e exercicio.
- Grao esperado:
  - Valor final: uma linha agregada por `j21_anousu, j21_matric` depois de filtrar historico de IPTU.
  - Fatores: uma linha por `j23_anousu, j23_matric` em `iptucalc`.
- Filtros de negocio:
  - Exercicios em `iptucalv.j21_anousu` e `iptucalc.j23_anousu`.
  - Somente IPTU via `iptucalv.j21_codhis -> iptucalh.j17_codhis` e classificacao local do historico.
- Caminho de negocio:
  - `iptucalv.j21_codhis -> iptucalh.j17_codhis`
  - `iptucalv.j21_matric, j21_anousu -> iptucalc.j23_matric, j23_anousu`
- Regra de comparacao:
  - Para explicar fatores, comparar a mesma matricula entre os dois exercicios usando `j23_matric`.
  - Separar a variacao total do IPTU da explicacao dos fatores. O total pode incluir matriculas que existem em apenas um ano; fatores devem ser calculados preferencialmente em matriculas presentes nos dois anos.
  - Fatores candidatos em `iptucalc`: `j23_vlrter`, `j23_areaed`, `j23_arealo`, `j23_areafr`, `j23_m2terr`, `j23_testad`, `j23_aliq`, `j23_vlrisen`, `j23_tipoim`.
- Metricas recomendadas para a resposta:
  - Valor do debito/IPTU calculado por ano: somar `iptucalv.j21_valor` por exercicio, filtrando somente historicos de IPTU em `iptucalh`.
  - Area gerada no momento do calculo: usar `iptucalc.j23_arealo` como area territorial considerada no calculo.
  - Valor do m2 lancado para o calculo do valor venal do terreno: usar `iptucalc.j23_m2terr`.
  - Area total edificada gerada no momento do calculo: usar `iptucalc.j23_areaed`.
  - Area fracionada gerada no momento do calculo: usar `iptucalc.j23_areafr`.
- Regra de agregacao das metricas:
  - Para mostrar o quadro geral do ano, agregar as metricas por exercicio.
  - Para explicar fator de aumento, comparar as metricas agregadas dos dois anos e apontar quais cresceram junto com o valor final do IPTU.
  - Se a pergunta pedir explicacao dos fatores, nao responder apenas com total anual; trazer junto as metricas de `iptucalc` que sustentam a narrativa.
- Estrutura esperada da resposta:
  - Um bloco com os valores finais de IPTU por ano.
  - Um bloco com as metricas comparativas por ano.
  - Uma explicacao curta relacionando o aumento/reducao do IPTU com variacao de `j23_m2terr`, `j23_arealo`, `j23_areaed` e `j23_areafr`, quando houver diferenca relevante.
- O que nao inferir:
  - Nao atribuir aumento a inflacao, legislacao, valorizacao imobiliaria ou novos imoveis sem dados retornados pela consulta.
  - Nao usar apenas totais anuais para explicar causa; totais mostram variacao, mas nao fatores.
- Cuidados:
  - `iptucalv` responde valor calculado; `iptucalc` ajuda a explicar parametros do calculo.
  - Isencao (`j23_vlrisen`) reduz valor; aumento de isencao pode reduzir o IPTU calculado.

## Conceito de negocio: caracteristica_da_construcao

- Nome humano: caracteristica vinculada a uma construcao.
- Perguntas comuns:
  - Relacao de construcoes por caracteristica.
  - Quantidade de construcoes por caracteristica.
  - Quais caracteristicas uma construcao possui?
- Significado: vinculo entre uma construcao de uma matricula e uma caracteristica cadastrada.
- Entidade principal: vinculo construcao-caracteristica.
- Fonte primaria: `cadastro.carconstr`.
- Tabelas envolvidas:
  - `cadastro.carconstr`
  - `cadastro.caracter`
  - `cadastro.cargrup`, quando precisar confirmar que a caracteristica e de construcao.
  - `cadastro.iptuconstr`, quando precisar filtrar construcoes ativas.
- Grao esperado: uma linha por `j48_matric, j48_idcons, j48_caract`.
- Caminho de negocio:
  - `carconstr.j48_caract -> caracter.j31_codigo`
  - `caracter.j31_grupo -> cargrup.j32_grupo`
  - `carconstr.j48_matric, j48_idcons -> iptuconstr.j39_matric, j39_idcons`
- Regra de contagem:
  - Para contar construcoes por caracteristica usando `carconstr`, agrupar pela caracteristica e contar linhas quando a PK contem matricula, construcao e caracteristica.
  - Quando a pergunta nao pedir filtro de construcao ativa, periodo, area ou outro dado de `iptuconstr`, preferir `COUNT(1)` direto em `carconstr`; isso evita `COUNT(DISTINCT (j48_matric, j48_idcons))` desnecessario.
  - Para contar imoveis por caracteristica, usar `COUNT(DISTINCT j48_matric)`.
- O que nao inferir:
  - Nao contar linhas de `caracter` para saber uso real; `caracter` e cadastro mestre.
  - Nao inferir que a caracteristica impacta financeiramente sem cruzar com regra de calculo.
- Cuidados:
  - Juntar com `iptuconstr` apenas quando precisar filtrar construcoes ativas, area, data de lancamento, demolicao ou outro atributo fisico da construcao.

## Conceito de negocio: caracteristica_do_lote

- Nome humano: caracteristica territorial vinculada ao lote.
- Perguntas comuns:
  - Quantos lotes possuem determinada caracteristica?
  - Quais caracteristicas de lote aparecem por bairro?
- Significado: vinculo entre lote e caracteristica cadastrada.
- Entidade principal: lote-caracteristica.
- Tabelas envolvidas:
  - `cadastro.carlote`
  - `cadastro.caracter`
  - `cadastro.cargrup`, quando precisar confirmar que a caracteristica e de lote.
  - `cadastro.iptubase`, quando precisar chegar em matriculas.
- Grao esperado: uma linha por lote e caracteristica.
- Caminho de negocio:
  - `carlote.j35_caract -> caracter.j31_codigo`
  - `carlote.j35_idbql -> iptubase.j01_idbql`
- Regra de contagem:
  - Para contar lotes com caracteristica, usar `COUNT(DISTINCT j35_idbql)`.
  - Para contar matriculas/imoveis com caracteristica de lote, cruzar com `iptubase` e usar `COUNT(DISTINCT j01_matric)`.
