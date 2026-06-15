---
titulo: Conceitos de negocio - Cadastro
dominio: cadastro
schema_principal: cadastro
fonte_json: cadastro_extraido.json
tags:
  - conhecimento-negocio
  - curadoria
  - obsidian
---

# Conceitos de negocio - Cadastro

Este arquivo e um esqueleto para curadoria humana. Ele nao deve ser usado como verdade final sem revisao do consultor.

Quando um conceito estiver validado, copie ou adapte a secao para `knowledge/manual/<schema>/conceitos.md` e regenere o RAG.

## Conceito de negocio: visao_geral_cadastro

- Nome humano: visao geral do schema cadastro.
- Perguntas comuns:
  - Preencher com perguntas reais do usuario.
- Significado: Preencher com o papel do schema no negocio.
- Entidade principal: Preencher.
- Tabelas envolvidas:
  - Preencher.
- Grao esperado: Preencher.
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - Preencher.
- Regra de contagem: Preencher.
- O que nao inferir:
  - Nao inferir regra de negocio apenas pelo nome tecnico.
- Cuidados:
  - Validar com pessoa de negocio antes de promover para o manual operacional.

## Candidatos extraidos do catalogo

## Conceito de negocio: iptucalv

- Nome humano: Valores gerados no calculo para o imóvel/matricula, ex: iptu, taxa lixo, ....
- Perguntas comuns:
  - Quantos registros existem em Valores gerados no calculo para o imóvel/matricula, ex: iptu, taxa lixo, ...?
  - Liste Valores gerados no calculo para o imóvel/matricula, ex: iptu, taxa lixo, ....
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Valores gerados no calculo para o imóvel/matricula, ex: iptu, taxa lixo, ....
- Fonte primaria: `cadastro.iptucalv`.
- Tabelas envolvidas:
  - `cadastro.iptucalv`
- Grao esperado: uma linha por matricula, exercicio e tipo de historico do valor gerado
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucalv.j21_anousu`.
- Caminho de negocio:
  - `cadastro.iptucalv.j21_codhis -> cadastro.iptucalh.j17_codhis`
  - `cadastro.iptucalv.j21_matric -> cadastro.iptubase.j01_matric`
  - `cadastro.iptucalv.j21_receit -> caixa.tabrec.k02_codigo`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j21_matric)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: zonasvalor

- Nome humano: Valores por zona fiscal e por ano.
- Perguntas comuns:
  - Quantos registros existem em Valores por zona fiscal e por ano?
  - Liste Valores por zona fiscal e por ano.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Valores por zona fiscal e por ano.
- Fonte primaria: `cadastro.zonasvalor`.
- Tabelas envolvidas:
  - `cadastro.zonasvalor`
- Grao esperado: j51_zona, j51_anousu
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.zonasvalor.j51_anousu`.
- Caminho de negocio:
  - `cadastro.zonasvalor.j51_zona -> cadastro.zonas.j50_zona`
- Regra de contagem: Para contar entidades, validar se a combinacao `j51_zona, j51_anousu` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: zonassetorvalor

- Nome humano: Estrutura criada para armazenar valor por zona e setor.
- Perguntas comuns:
  - Quantos registros existem em Estrutura criada para armazenar valor por zona e setor?
  - Liste Estrutura criada para armazenar valor por zona e setor.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Estrutura criada para armazenar valor por zona e setor.
- Fonte primaria: `cadastro.zonassetorvalor`.
- Tabelas envolvidas:
  - `cadastro.zonassetorvalor`
- Grao esperado: j141_anousu, j141_zonas, j141_setor
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.zonassetorvalor.j141_anousu`.
- Caminho de negocio:
  - `cadastro.zonassetorvalor.j141_setor -> cadastro.setor.j30_codi`
  - `cadastro.zonassetorvalor.j141_zonas -> cadastro.zonas.j50_zona`
- Regra de contagem: Para contar entidades, validar se a combinacao `j141_anousu, j141_zonas, j141_setor` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: setorfiscalvalor

- Nome humano: Valores por ano dos setores fiscais de m2 terreno.
- Perguntas comuns:
  - Quantos registros existem em Valores por ano dos setores fiscais de m2 terreno?
  - Liste Valores por ano dos setores fiscais de m2 terreno.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Valores por ano dos setores fiscais de m2 terreno.
- Fonte primaria: `cadastro.setorfiscalvalor`.
- Tabelas envolvidas:
  - `cadastro.setorfiscalvalor`
- Grao esperado: j82_codigo
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.setorfiscalvalor.j82_anousu`.
- Caminho de negocio:
  - `cadastro.setorfiscalvalor.j82_setorfiscal -> cadastro.setorfiscal.j90_codigo`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j82_codigo)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: ruashistorico

- Nome humano: Histórico das alterações do cadastro de ruas.
- Perguntas comuns:
  - Quantos registros existem em Histórico das alterações do cadastro de ruas?
  - Liste Histórico das alterações do cadastro de ruas.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Histórico das alterações do cadastro de ruas.
- Fonte primaria: `cadastro.ruashistorico`.
- Tabelas envolvidas:
  - `cadastro.ruashistorico`
- Grao esperado: j136_sequencial
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.ruashistorico.j136_dataalteracao`.
  - Candidato a tempo/exercicio: `cadastro.ruashistorico.j136_datalei`.
- Caminho de negocio:
  - `cadastro.ruashistorico.j136_ruas -> cadastro.ruas.j14_codigo`
  - `cadastro.ruashistorico.j136_ruastipo -> cadastro.ruastipo.j88_codigo`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j136_sequencial)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: propri

- Nome humano: Cadastro dos outros proprietarios do imovel.
- Perguntas comuns:
  - Quantos registros existem em Cadastro dos outros proprietarios do imovel?
  - Liste Cadastro dos outros proprietarios do imovel.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Cadastro dos outros proprietarios do imovel.
- Fonte primaria: `cadastro.propri`.
- Tabelas envolvidas:
  - `cadastro.propri`
- Grao esperado: j42_matric, j42_numcgm
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.propri.j42_matric -> cadastro.iptubase.j01_matric`
  - `cadastro.propri.j42_numcgm -> protocolo.cgm.z01_numcgm`
  - `cadastro.propri.j42_tipo_contribuinte, j42_tipo_contribuinte, j42_tipo_contribuinte -> cadastro.tipocontribuinte.j147_sequencial, j147_sequencial, j147_sequencial`
- Regra de contagem: Para contar entidades, validar se a combinacao `j42_matric, j42_numcgm` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: promitente

- Nome humano: Cadastro dos promitente compradores. Identificacao dos contribuintes que compram imoveis financiados e so averbam em seu nome apos o termino do pagamento..
- Perguntas comuns:
  - Quantos registros existem em Cadastro dos promitente compradores. Identificacao dos contribuintes que compram imoveis financiados e so averbam em seu nome apos o termino do pagamento.?
  - Liste Cadastro dos promitente compradores. Identificacao dos contribuintes que compram imoveis financiados e so averbam em seu nome apos o termino do pagamento..
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Cadastro dos promitente compradores. Identificacao dos contribuintes que compram imoveis financiados e so averbam em seu nome apos o termino do pagamento..
- Fonte primaria: `cadastro.promitente`.
- Tabelas envolvidas:
  - `cadastro.promitente`
- Grao esperado: j41_matric, j41_numcgm
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.promitente.j41_matric -> cadastro.iptubase.j01_matric`
  - `cadastro.promitente.j41_numcgm -> protocolo.cgm.z01_numcgm`
- Regra de contagem: Para contar entidades, validar se a combinacao `j41_matric, j41_numcgm` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: moblevatamento

- Nome humano: Levantamento do cadastro PDA.
- Perguntas comuns:
  - Quantos registros existem em Levantamento do cadastro PDA?
  - Liste Levantamento do cadastro PDA.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Levantamento do cadastro PDA.
- Fonte primaria: `cadastro.moblevatamento`.
- Tabelas envolvidas:
  - `cadastro.moblevatamento`
- Grao esperado: j97_sequen
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.moblevatamento.j97_codimporta -> cadastro.mobimportacao.j95_codimporta`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j97_sequen)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: isenexe

- Nome humano: Cadastro dos exercicios da isencao.
- Perguntas comuns:
  - Quantos registros existem em Cadastro dos exercicios da isencao?
  - Liste Cadastro dos exercicios da isencao.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Cadastro dos exercicios da isencao.
- Fonte primaria: `cadastro.isenexe`.
- Tabelas envolvidas:
  - `cadastro.isenexe`
- Grao esperado: j47_codigo, j47_anousu
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.isenexe.j47_anousu`.
- Caminho de negocio:
  - `cadastro.isenexe.j47_codigo -> cadastro.iptuisen.j46_codigo`
- Regra de contagem: Para contar entidades, validar se a combinacao `j47_codigo, j47_anousu` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptuisen

- Nome humano: cadastro das matricula com suas isencoes.
- Perguntas comuns:
  - Quantos registros existem em cadastro das matricula com suas isencoes?
  - Liste cadastro das matricula com suas isencoes.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: cadastro das matricula com suas isencoes.
- Fonte primaria: `cadastro.iptuisen`.
- Tabelas envolvidas:
  - `cadastro.iptuisen`
- Grao esperado: j46_codigo
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptuisen.j46_dtfim`.
  - Candidato a tempo/exercicio: `cadastro.iptuisen.j46_dtinc`.
  - Candidato a tempo/exercicio: `cadastro.iptuisen.j46_dtini`.
- Caminho de negocio:
  - `cadastro.iptuisen.j46_matric -> cadastro.iptubase.j01_matric`
  - `cadastro.iptuisen.j46_tipo -> cadastro.tipoisen.j45_tipo`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j46_codigo)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptufrac

- Nome humano: Fracionamento dos lotes. É utilizado para calcular a area ou testada fracionada para uma matricula. É bastante comum utilizar em lote que tenham construcoes do tipo apartamento, onde devemos fracionar o valor vanel de um imovel.
- Perguntas comuns:
  - Quantos registros existem em Fracionamento dos lotes. É utilizado para calcular a area ou testada fracionada para uma matricula. É bastante comum utilizar em lote que tenham construcoes do tipo apartamento, onde devemos fracionar o valor vanel de um imovel?
  - Liste Fracionamento dos lotes. É utilizado para calcular a area ou testada fracionada para uma matricula. É bastante comum utilizar em lote que tenham construcoes do tipo apartamento, onde devemos fracionar o valor vanel de um imovel.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Fracionamento dos lotes. É utilizado para calcular a area ou testada fracionada para uma matricula. É bastante comum utilizar em lote que tenham construcoes do tipo apartamento, onde devemos fracionar o valor vanel de um imovel.
- Fonte primaria: `cadastro.iptufrac`.
- Tabelas envolvidas:
  - `cadastro.iptufrac`
- Grao esperado: j25_anousu, j25_matric
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptufrac.j25_anousu`.
- Caminho de negocio:
  - `cadastro.iptufrac.j25_matric -> cadastro.iptubase.j01_matric`
- Regra de contagem: Para contar entidades, validar se a combinacao `j25_anousu, j25_matric` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptuender

- Nome humano: Cadastro de endereco de entrega dos carnes de iptu.
- Perguntas comuns:
  - Quantos registros existem em Cadastro de endereco de entrega dos carnes de iptu?
  - Liste Cadastro de endereco de entrega dos carnes de iptu.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Cadastro de endereco de entrega dos carnes de iptu.
- Fonte primaria: `cadastro.iptuender`.
- Tabelas envolvidas:
  - `cadastro.iptuender`
- Grao esperado: j43_matric
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.iptuender.j43_matric -> cadastro.iptubase.j01_matric`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j43_matric)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptuconstr

- Nome humano: Cadastro das construcoes que foram medidas pelo municipio.
- Perguntas comuns:
  - Quantos registros existem em Cadastro das construcoes que foram medidas pelo municipio?
  - Liste Cadastro das construcoes que foram medidas pelo municipio.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Cadastro das construcoes que foram medidas pelo municipio.
- Fonte primaria: `cadastro.iptuconstr`.
- Tabelas envolvidas:
  - `cadastro.iptuconstr`
- Grao esperado: j39_matric, j39_idcons
- Filtros de negocio:
  - Validar se `cadastro.iptuconstr.j39_dtdemo IS NULL` representa registro ativo/vigente.
  - Candidato a tempo/exercicio: `cadastro.iptuconstr.j39_ano`.
  - Candidato a tempo/exercicio: `cadastro.iptuconstr.j39_dtdemo`.
  - Candidato a tempo/exercicio: `cadastro.iptuconstr.j39_dtlan`.
- Caminho de negocio:
  - `cadastro.iptuconstr.j39_codigo -> cadastro.ruas.j14_codigo`
  - `cadastro.iptuconstr.j39_matric -> cadastro.iptubase.j01_matric`
- Regra de contagem: Para contar entidades, validar se a combinacao `j39_matric, j39_idcons` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucale

- Nome humano: Registra os valores venais calculados para as construcoes.
- Perguntas comuns:
  - Quantos registros existem em Registra os valores venais calculados para as construcoes?
  - Liste Registra os valores venais calculados para as construcoes.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Registra os valores venais calculados para as construcoes.
- Fonte primaria: `cadastro.iptucale`.
- Tabelas envolvidas:
  - `cadastro.iptucale`
- Grao esperado: j22_anousu, j22_matric, j22_idcons
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucale.j22_anousu`.
- Caminho de negocio:
  - `cadastro.iptucale.j22_matric, j22_matric, j22_idcons, j22_idcons -> cadastro.iptuconstr.j39_matric, j39_idcons, j39_matric, j39_idcons`
- Regra de contagem: Para contar entidades, validar se a combinacao `j22_anousu, j22_matric, j22_idcons` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalcpadraoorigem

- Nome humano: dados da origem da importação.
- Perguntas comuns:
  - Quantos registros existem em dados da origem da importação?
  - Liste dados da origem da importação.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: dados da origem da importação.
- Fonte primaria: `cadastro.iptucalcpadraoorigem`.
- Tabelas envolvidas:
  - `cadastro.iptucalcpadraoorigem`
- Grao esperado: j27_sequencial
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucalcpadraoorigem.j27_anousu`.
- Caminho de negocio:
  - `cadastro.iptucalcpadraoorigem.j27_anousu, j27_anousu, j27_matric, j27_matric -> cadastro.iptucalc.j23_matric, j23_anousu, j23_anousu, j23_matric`
  - `cadastro.iptucalcpadraoorigem.j27_iptucalcpadrao -> cadastro.iptucalcpadrao.j10_sequencial`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j27_sequencial)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalcpadraolog

- Nome humano: Log do calculo padrão.
- Perguntas comuns:
  - Quantos registros existem em Log do calculo padrão?
  - Liste Log do calculo padrão.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Log do calculo padrão.
- Fonte primaria: `cadastro.iptucalcpadraolog`.
- Tabelas envolvidas:
  - `cadastro.iptucalcpadraolog`
- Grao esperado: j19_sequencial
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucalcpadraolog.j19_data`.
- Caminho de negocio:
  - `cadastro.iptucalcpadraolog.j19_iptucalcpadrao -> cadastro.iptucalcpadrao.j10_sequencial`
  - `cadastro.iptucalcpadraolog.j19_usuario -> configuracoes.db_usuarios.id_usuario`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j19_sequencial)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalcpadraoconstr

- Nome humano: Construções.
- Perguntas comuns:
  - Quantos registros existem em Construções?
  - Liste Construções.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Construções.
- Fonte primaria: `cadastro.iptucalcpadraoconstr`.
- Tabelas envolvidas:
  - `cadastro.iptucalcpadraoconstr`
- Grao esperado: j11_sequencial
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.iptucalcpadraoconstr.j11_iptucalcpadrao -> cadastro.iptucalcpadrao.j10_sequencial`
  - `cadastro.iptucalcpadraoconstr.j11_matric, j11_matric, j11_idcons, j11_idcons -> cadastro.iptuconstr.j39_matric, j39_idcons, j39_idcons, j39_matric`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j11_sequencial)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalcpadrao

- Nome humano: Calculo padrão do iptu.
- Perguntas comuns:
  - Quantos registros existem em Calculo padrão do iptu?
  - Liste Calculo padrão do iptu.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Calculo padrão do iptu.
- Fonte primaria: `cadastro.iptucalcpadrao`.
- Tabelas envolvidas:
  - `cadastro.iptucalcpadrao`
- Grao esperado: j10_sequencial
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucalcpadrao.j10_anousu`.
- Caminho de negocio:
  - `cadastro.iptucalcpadrao.j10_matric -> cadastro.iptubase.j01_matric`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j10_sequencial)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalclogmat

- Nome humano: Matriculas do log do calculo do iptu.
- Perguntas comuns:
  - Quantos registros existem em Matriculas do log do calculo do iptu?
  - Liste Matriculas do log do calculo do iptu.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Matriculas do log do calculo do iptu.
- Fonte primaria: `cadastro.iptucalclogmat`.
- Tabelas envolvidas:
  - `cadastro.iptucalclogmat`
- Grao esperado: j28_codigo, j28_matric
- Filtros de negocio:
  - Preencher.
- Caminho de negocio:
  - `cadastro.iptucalclogmat.j28_codigo -> cadastro.iptucalclog.j27_codigo`
  - `cadastro.iptucalclogmat.j28_matric -> cadastro.iptubase.j01_matric`
  - `cadastro.iptucalclogmat.j28_tipologcalc -> cadastro.iptucadlogcalc.j62_codigo`
- Regra de contagem: Para contar entidades, validar se a combinacao `j28_codigo, j28_matric` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.

## Conceito de negocio: iptucalclog

- Nome humano: Log do calculo do iptu.
- Perguntas comuns:
  - Quantos registros existem em Log do calculo do iptu?
  - Liste Log do calculo do iptu.
- Significado: Preencher em linguagem de negocio.
- Entidade principal: Log do calculo do iptu.
- Fonte primaria: `cadastro.iptucalclog`.
- Tabelas envolvidas:
  - `cadastro.iptucalclog`
- Grao esperado: j27_codigo
- Filtros de negocio:
  - Candidato a tempo/exercicio: `cadastro.iptucalclog.j27_anousu`.
  - Candidato a tempo/exercicio: `cadastro.iptucalclog.j27_data`.
- Caminho de negocio:
  - `cadastro.iptucalclog.j27_usuario -> configuracoes.db_usuarios.id_usuario`
- Regra de contagem: Para contar entidades, validar se `COUNT(DISTINCT j27_codigo)` representa o grao correto.
- O que nao inferir:
  - Nao inferir status, periodo, valor financeiro ou entidade principal sem regra validada.
- Cuidados:
  - Confirmar se esta tabela e fonte primaria, tabela de movimento, tabela de dominio ou tabela de historico.
