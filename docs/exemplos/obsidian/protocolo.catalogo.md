---
titulo: Catalogo Protocolo
dominio: protocolo
schema_principal: protocolo
fonte_json: protocolo.json
tags:
  - catalogo
  - ecidade
  - protocolo
---

# Catalogo Protocolo

- Dominio: `protocolo`
- Schema principal: `protocolo`
- Arquivo origem: `protocolo.json`
- Descricao: Catalogo extraido automaticamente para o schema protocolo.

## Como usar esta nota

- Esta nota preserva a estrutura tecnica do catalogo.
- O objetivo e enriquecer regra de negocio em linguagem humana.
- Preencha principalmente os blocos de perguntas, regras, filtros e cuidados.

## Tabelas deste dominio

- `protocolo.andpadrao`
- `protocolo.arqandam`
- `protocolo.arqproc`
- `protocolo.arreproc`
- `protocolo.camposandpadrao`
- `protocolo.camposandpadraoresposta`
- `protocolo.cepbairros`
- `protocolo.cepbairrosfaixa`
- `protocolo.cepestados`
- `protocolo.cepestadosfaixa`
- `protocolo.cepgu`
- `protocolo.ceplocalidades`
- `protocolo.ceplogradouros`
- `protocolo.certidao`
- `protocolo.certidaocgm`
- `protocolo.certidaoinscr`
- `protocolo.certidaomatric`
- `protocolo.cgm`
- `protocolo.cgm_campos_obrigatorios`
- `protocolo.cgmalt`
- `protocolo.cgmcomposicaofamiliar`
- `protocolo.cgmcorreto`
- `protocolo.cgmdepara`
- `protocolo.cgmdoc`
- `protocolo.cgmenderecoexterior`
- `protocolo.cgmerrado`
- `protocolo.cgmerradolog`
- `protocolo.cgmestrangeiro`
- `protocolo.cgmfamilia`
- `protocolo.cgmfisico`
- `protocolo.cgmfoto`
- `protocolo.cgmjuridico`
- `protocolo.cgmsaude`
- `protocolo.cgmtipoempresa`
- `protocolo.db_ceplog`
- `protocolo.db_cepmunic`
- `protocolo.db_cgmbairro`
- `protocolo.db_cgmcgc`
- `protocolo.db_cgmcpf`
- `protocolo.db_cgmruas`
- `protocolo.db_uf`
- `protocolo.gestaodepartamentoprocesso`
- `protocolo.gestaoprocessovencido`
- `protocolo.historico_tipo_processo`
- `protocolo.historicovisualizacaoprocandam`
- `protocolo.mensageriaprocesso`
- `protocolo.procandam`
- `protocolo.procandamint`
- `protocolo.procandamintand`
- `protocolo.procandamintusu`
- `protocolo.procarquiv`
- `protocolo.procdoc`
- `protocolo.procdoctipo`
- `protocolo.processoinscr`
- `protocolo.processomatric`
- `protocolo.processosapensados`
- `protocolo.processosvinculados`
- `protocolo.procimag`
- `protocolo.procinscr`
- `protocolo.procmatric`
- `protocolo.procprocessodesp`
- `protocolo.procprocessodoc`
- `protocolo.procrec`
- `protocolo.proctipovar`
- `protocolo.proctransand`
- `protocolo.proctransfer`
- `protocolo.proctransferint`
- `protocolo.proctransferintand`
- `protocolo.proctransferintusu`
- `protocolo.proctransferproc`
- `protocolo.proctransferworkflowativexec`
- `protocolo.procvar`
- `protocolo.protdoc`
- `protocolo.protparam`
- `protocolo.protparamglobal`
- `protocolo.protprocesso`
- `protocolo.protprocessodocumento`
- `protocolo.protprocessonumeracao`
- `protocolo.protprocessonumeracaoorgao`
- `protocolo.prottipodocumentoprocesso`
- `protocolo.recibocanc`
- `protocolo.tipoarq`
- `protocolo.tipodespacho`
- `protocolo.tipofamiliar`
- `protocolo.tipoproc`
- `protocolo.tipoprocesso`
- `protocolo.tipoprocessoformulario`
- `protocolo.tiporece`

## Tabela de negocio: `protocolo.andpadrao`

### Identidade

- Nome humano: Andamento Padrão do Processo. Especifica cada departamento o qual o processo passará e quantidade de dias que o processo poderá ficar em cada departamento..
- O que representa: Andamento Padrão do Processo. Especifica cada departamento o qual o processo passará e quantidade de dias que o processo poderá ficar em cada departamento.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p53_codigo`
  - `p53_ordem`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p53_codigo, p53_dias
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p53_coddepto`: código do departamento
- `p53_codigo`: código do tipo de processo
- `p53_dias`: Quantidade de dias que o processo precisa ficar em cada departamento para ser analisado
- `p53_ordem`: Ordem cronológica do andamento do processo.

### Metricas atomicas

- `p53_dias`: Quantidade de dias que o processo precisa ficar em cada departamento para ser analisado

### Dimensoes

- `p53_codigo`: código do tipo de processo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p53_coddepto` -> `configuracoes.db_depart` (coddepto) [andpadrao_coddepto_fk]
- `p53_codigo` -> `protocolo.tipoproc` (p51_codigo) [andpadrao_codigo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.arqandam`

### Identidade

- Nome humano: andamento do arquivamento.
- O que representa: andamento do arquivamento
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p69_arquivado`: Se processo foi arquivado ou desarquivado
- `p69_codandam`: Código andamento
- `p69_codarquiv`: Código do Arquivamento

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p69_codandam` -> `protocolo.procandam` (p61_codandam) [arqandam_codandam_fk]
- `p69_codarquiv` -> `protocolo.procarquiv` (p67_codarquiv) [arqandam_codarquiv_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.arqproc`

### Identidade

- Nome humano: Reabertura de Processos.
- O que representa: Reabertura de Processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p68_codarquiv`: Código do Arquivamento
- `p68_codproc`: Código do Processo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.arreproc`

### Identidade

- Nome humano: Arrecadação de processo.
- O que representa: Arrecadação de processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `k80_codproc`
  - `k80_numpre`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `k80_codproc`: Processo
- `k80_numpre`: Numpre

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.camposandpadrao`

### Identidade

- Nome humano: Tabela que vincula campos do sistema ao andamento padrão, para que seja possivel preencher informações ao fazer um despacho no processo.
- O que representa: Tabela que vincula campos do sistema ao andamento padrão, para que seja possivel preencher informações ao fazer um despacho no processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p110_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p110_andpadrao_codigo, p110_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p110_andpadrao_codigo`: Tipo de processo do andamento padrão ao qual o campo está vinculado
- `p110_andpadrao_ordem`: Ordem do andamento padrão
- `p110_codcam`: Código do campo que está vinculado ao andamento padrão
- `p110_obrigatorio`: Informa se o campo terá o preenchimento obrigatório ou não
- `p110_sequencial`: Código sequencial da tabela que serve de primary key e facilita manutenção na tabela.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p110_andpadrao_codigo`: Tipo de processo do andamento padrão ao qual o campo está vinculado

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p110_andpadrao_codigo, p110_andpadrao_codigo, p110_andpadrao_ordem, p110_andpadrao_ordem` -> `protocolo.andpadrao` (p53_codigo, p53_ordem, p53_codigo, p53_ordem) [camposandpadrao_p110_andpadrao_codigo_p110_andpadrao_ordem_fkey]
- `p110_codcam` -> `configuracoes.db_syscampo` (codcam) [camposandpadrao_p110_codcam_fkey]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.camposandpadraoresposta`

### Identidade

- Nome humano: Tabela que guarda as resposta dos campos dinâmicos do andamento, populada ao conceder despacho ao processo.
- O que representa: Tabela que guarda as resposta dos campos dinâmicos do andamento, populada ao conceder despacho ao processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p111_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p111_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p111_camposandpadrao`: Vínculo do campo com o andamento padrão
- `p111_codandam`: Andamento atual do processo, ao qual a resposta pertence
- `p111_codcam`: Código do campo
- `p111_resposta`: Resposta do campo dinâmico
- `p111_sequencial`: Código sequencial da tabela

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p111_camposandpadrao` -> `protocolo.camposandpadrao` (p110_sequencial) [camposandpadraoresposta_p111_camposandpadrao_fkey]
- `p111_codandam` -> `protocolo.procandam` (p61_codandam) [camposandpadraoresposta_p111_codandam_fkey]
- `p111_codcam` -> `configuracoes.db_syscampo` (codcam) [camposandpadraoresposta_p111_codcam_fkey]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cepbairros`

### Identidade

- Nome humano: Cadastro de bairros igual correio.
- O que representa: Cadastro de bairros igual correio
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp01_codbairro`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: cp01_codbairro, cp01_codlocalidade
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp01_bairro`: Nome do bairro
- `cp01_codbairro`: Codigo do Bairro
- `cp01_codlocalidade`: Codigo da Localidade
- `cp01_sigla`: Sigla

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `cp01_bairro`: Nome do bairro
- `cp01_codbairro`: Codigo do Bairro
- `cp01_codlocalidade`: Codigo da Localidade

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp01_sigla` -> `protocolo.cepestados` (cp03_sigla) [cepbairros_sigla_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cepbairrosfaixa`

### Identidade

- Nome humano: Cadastro de Bairros Faixa.
- O que representa: Cadastro de Bairros Faixa
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp02_codbairro`
  - `cp02_faixa`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: cp02_codbairro
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp02_cepfinal`: Cep final
- `cp02_cepinicial`: Cep inicial
- `cp02_codbairro`: Codigo do Bairro
- `cp02_faixa`: Faixa de Ceps por Bairros

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `cp02_codbairro`: Codigo do Bairro
- `cp02_faixa`: Faixa de Ceps por Bairros

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp02_codbairro` -> `protocolo.cepbairros` (cp01_codbairro) [cepbairrosfaixa_codbairro_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cepestados`

### Identidade

- Nome humano: Cadastro de Estados conforme com correio.
- O que representa: Cadastro de Estados conforme com correio
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp03_sigla`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp03_estado`: Estado
- `cp03_sigla`: Sigla Estado

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cepestadosfaixa`

### Identidade

- Nome humano: Cadastro de Estados Faixa.
- O que representa: Cadastro de Estados Faixa
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp04_sigla`
  - `cp04_faixa`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp04_cepfinal`: Cep final
- `cp04_cepinicial`: Cep inicial
- `cp04_faixa`: Faixa de Estados
- `cp04_sigla`: Sigla Estado Faixa

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp04_sigla` -> `protocolo.cepestados` (cp03_sigla) [cepestadosfaixa_sigla_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cepgu`

### Identidade

- Nome humano: Cadastro de GU.
- O que representa: Cadastro de GU
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp07_codgu`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: cp07_codbairro, cp07_codgu, cp07_codlocalidade, cp07_codlogradouro
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp07_adicional`: Adicional
- `cp07_cep`: CEP
- `cp07_codbairro`: Codigo do Bairro
- `cp07_codgu`: Codigo GU
- `cp07_codlocalidade`: Codigo da Localidade
- `cp07_codlogradouro`: Codigo da Logradouro
- `cp07_gu`: GU
- `cp07_sigla`: Sigla Estado

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `cp07_codbairro`: Codigo do Bairro
- `cp07_codgu`: Codigo GU
- `cp07_codlocalidade`: Codigo da Localidade
- `cp07_codlogradouro`: Codigo da Logradouro

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp07_codbairro` -> `protocolo.cepbairros` (cp01_codbairro) [cepgu_codbairro_fk]
- `cp07_codlocalidade` -> `protocolo.ceplocalidades` (cp05_codlocalidades) [cepgu_codlocalidade_fk]
- `cp07_codlogradouro` -> `protocolo.ceplogradouros` (cp06_sequencial) [cepgu_codlogradouro_fk]
- `cp07_sigla` -> `protocolo.cepestados` (cp03_sigla) [cepgu_sigla_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.ceplocalidades`

### Identidade

- Nome humano: Cadastro de localidades igual do correio.
- O que representa: Cadastro de localidades igual do correio
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp05_codlocalidades`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: cp05_codlocalidades, cp05_codsubordinacao, cp05_localidades
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp05_cepfinal`: Cep final
- `cp05_cepinicial`: Cep inicial
- `cp05_codlocalidades`: Codigo da Localidade
- `cp05_codsubordinacao`: Codigo Subordinação
- `cp05_localidades`: Cadastro de Localidades
- `cp05_sigla`: Sigla Estado
- `cp05_situacao`: Situação
- `cp05_tipo`: Tipo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `cp05_codlocalidades`: Codigo da Localidade
- `cp05_codsubordinacao`: Codigo Subordinação
- `cp05_tipo`: Tipo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp05_sigla` -> `protocolo.cepestados` (cp03_sigla) [ceplocalidades_sigla_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.ceplogradouros`

### Identidade

- Nome humano: Cadastro de Logradouros.
- O que representa: Cadastro de Logradouros
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `cp06_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: cp06_codbairrofinal, cp06_codbairroinicial, cp06_codlocalidade, cp06_codlogradouro, cp06_codseccao
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `cp06_adicional`: Adicional
- `cp06_cep`: Cep
- `cp06_codbairrofinal`: Codigo do Bairro final
- `cp06_codbairroinicial`: Codigo do Bairro inicial
- `cp06_codlocalidade`: Codigo da Localidade
- `cp06_codlogradouro`: Codigo do Logradouro
- `cp06_codseccao`: Codigo Secção
- `cp06_grandeusuario`: Grande Usuario
- `cp06_lado`: Lado
- `cp06_logradouro`: Logradouro
- `cp06_numfinal`: Número Final
- `cp06_numinicial`: Número Inicial
- `cp06_sequencial`: Sequencial
- `cp06_sigla`: Sigla Estado

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `cp06_codbairrofinal`: Codigo do Bairro final
- `cp06_codbairroinicial`: Codigo do Bairro inicial
- `cp06_codlocalidade`: Codigo da Localidade
- `cp06_codlogradouro`: Codigo do Logradouro
- `cp06_codseccao`: Codigo Secção

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `cp06_codlocalidade` -> `protocolo.ceplocalidades` (cp05_codlocalidades) [ceplogradouros_codlocalidade_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.certidao`

### Identidade

- Nome humano: Certidoes geradas, positiva, negativa ou regular.
- O que representa: Certidoes geradas, positiva, negativa ou regular
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p50_sequencial`
- Coluna temporal: `p50_data`
- Candidatas a chave de negocio: p50_codimpresso, p50_data, p50_diasvalidade, p50_idusuario, p50_ip
- Candidatas a coluna temporal: p50_data

### Colunas principais

- `p50_arquivo`: Imagem
- `p50_codimpresso`: Código Impresso no documento da certidão
- `p50_codproc`: Código do processo
- `p50_data`: Data de inclusão da certidão
- `p50_diasvalidade`: Quantidade de dias de validade da certidão quando cadastrada
- `p50_exerc`: Exercício
- `p50_hist`: Historico da inclusão
- `p50_hora`: Hora da inclusão
- `p50_idusuario`: codigo do usuario
- `p50_instit`: Código da Instituição
- `p50_ip`: IP da maquina que gerou a certidão
- `p50_sequencial`: Codigo sequencial da tabela
- `p50_tipo`: Tipo da certidão se negativa, positiva ou regular
- `p50_web`: Se foi gerado pela web ou via sistema

### Metricas atomicas

- `p50_diasvalidade`: Quantidade de dias de validade da certidão quando cadastrada

### Dimensoes

- `p50_data`: Data de inclusão da certidão
- `p50_idusuario`: codigo do usuario
- `p50_sequencial`: Codigo sequencial da tabela
- `p50_tipo`: Tipo da certidão se negativa, positiva ou regular

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p50_idusuario` -> `configuracoes.db_usuarios` (id_usuario) [certidao_idusuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.certidaocgm`

### Identidade

- Nome humano: Ligacao da certidao com cgm.
- O que representa: Ligacao da certidao com cgm
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p49_numcgm, p49_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p49_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `p49_sequencial`: Codigo sequencial da tabela

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p49_sequencial`: Codigo sequencial da tabela

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p49_numcgm` -> `protocolo.cgm` (z01_numcgm) [certidaocgm_numcgm_fk]
- `p49_sequencial` -> `protocolo.certidao` (p50_sequencial) [certidaocgm_sequencial_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.certidaoinscr`

### Identidade

- Nome humano: Ligação da issbase com certidao.
- O que representa: Ligação da issbase com certidao
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p48_inscr, p48_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p48_inscr`: Inscricao Municipal no cadastro de alvará
- `p48_sequencial`: Codigo sequencial da tabela

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p48_sequencial`: Codigo sequencial da tabela

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p48_inscr` -> `issqn.issbase` (q02_inscr) [certidaoinscr_inscr_fk]
- `p48_sequencial` -> `protocolo.certidao` (p50_sequencial) [certidaoinscr_sequencial_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.certidaomatric`

### Identidade

- Nome humano: Ligação da iptubase com certidao.
- O que representa: Ligação da iptubase com certidao
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p47_matric, p47_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p47_matric`: Codigo da matrícula do imovel para identificar o proprietário de um determinado lote.
- `p47_sequencial`: Codigo sequencial da tabela

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p47_matric`: Codigo da matrícula do imovel para identificar o proprietário de um determinado lote.
- `p47_sequencial`: Codigo sequencial da tabela

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p47_matric` -> `cadastro.iptubase` (j01_matric) [certidaomatric_matric_fk]
- `p47_sequencial` -> `protocolo.certidao` (p50_sequencial) [certidaomatric_sequencial_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgm`

### Identidade

- Nome humano: Cadastro geral do municipio, nesta tabela sao cadastradas todas as pessoas fisicas e juridicas que tenham algum vínculo com o município..
- O que representa: Cadastro geral do municipio, nesta tabela sao cadastradas todas as pessoas fisicas e juridicas que tenham algum vínculo com o município.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: `z01_dtemissao`
- Candidatas a chave de negocio: z01_escolaridade, z01_ident, z01_identdtexp, z01_identorgao, z01_incest
- Candidatas a coluna temporal: z01_dtemissao, z01_dtfalecimento, z01_dthabilitacao, z01_dtvencimento, z01_identdtexp

### Colunas principais

- `z01_baicon`: Bairro do endereco comercial
- `z01_bairro`: Bairro
- `z01_cadast`: Dia em que este registro foi cadastrado
- `z01_categoria`: Categoria da carteira de motorista
- `z01_celcon`: Celular comercial
- `z01_cep`: CEP
- `z01_cepcon`: CEP do endereco comercial
- `z01_cgccpf`: Código do CNPJ quando empresa ou Código do CPF quando pessoa física
- `z01_cnh`: Número da carteira de motorista
- `z01_comcon`: Complemento do numero do endereco comercial
- `z01_compl`: Complemento do numero do endereco
- `z01_contato`: Contato,nome do responsavel.
- `z01_cxposcon`: caixa postal do endereco comercial do contribuinte
- `z01_cxpostal`: Caixa postal do contribuinte cadastrado
- `z01_dtemissao`: Data emissao da carteira de motorista
- `z01_dtfalecimento`: Falecimento
- `z01_dthabilitacao`: Data da primeira CNH
- `z01_dtvencimento`: Data Vencimento CNH
- `z01_email`: email
- `z01_emailc`: email comercial
- `z01_endcon`: Endereco Comercial
- `z01_ender`: Endereço
- `z01_escolaridade`: Escolaridade
- `z01_estciv`: Estado civil (pessoa fisica)
- `z01_fax`: Fax
- `z01_genero`: Gênero
- `z01_hora`: Hora do Cadastramento
- `z01_ident`: Identidade (pessoa fisica)
- `z01_identdtexp`: Data de Expedição
- `z01_identorgao`: Orgao emisso
- `z01_incest`: Inscrição Estadual (pessoa juridica)
- `z01_localtrabalho`: Local de Trabalho
- `z01_login`: Login do usuario que cadastrou este registro
- `z01_mae`: Mãe
- `z01_muncon`: Municipio do endereco comercial
- `z01_munic`: Município
- `z01_nacion`: Codigo da nacionalidade
- `z01_nasc`: Data de Nascimento
- `z01_naturalidade`: Naturalidade
- `z01_nome`: Nome da pessoa ou Razao Social se for Empresa
- `z01_nomecomple`: Nome Completo
- `z01_nomefanta`: Nome Fantasia da empresa
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `z01_numcon`: Numero do endereco comercial
- `z01_numero`: Numero do endereco
- `z01_obs`: Observações
- `z01_pai`: Pai
- `z01_pis`: Pis/Pasep/CI
- `z01_profis`: Profissao (pessoa fisica)
- `z01_renda`: Renda
- `z01_sexo`: Sexo
- `z01_telcel`: Telefone Celular
- `z01_telcon`: Telefone comercial
- `z01_telef`: Telefone
- `z01_tipcre`: 1=administracao publica 2=privada
- `z01_trabalha`: Trabalha
- `z01_uf`: Unidade Federativa (estado)
- `z01_ufcon`: Estado do endereco comercial para localização do contribuinte
- `z01_ultalt`: Última Alteração

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z01_baicon`: Bairro do endereco comercial
- `z01_bairro`: Bairro
- `z01_dtemissao`: Data emissao da carteira de motorista
- `z01_dthabilitacao`: Data da primeira CNH
- `z01_dtvencimento`: Data Vencimento CNH
- `z01_identdtexp`: Data de Expedição
- `z01_nacion`: Codigo da nacionalidade
- `z01_nasc`: Data de Nascimento

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgm_campos_obrigatorios`

### Identidade

- Nome humano: Tabela que identifica quais campos do CGM são obrigatórios..
- O que representa: Tabela que identifica quais campos do CGM são obrigatórios.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p73_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p73_html_id, p73_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p73_html_id`: ID do input HTML para fazer a validação dos campos obrigatórios.
- `p73_label`: Label do campo.
- `p73_obrigatorio`: Coluna indica se o campo é obrigatório.
- `p73_sequencial`: Sequencial da tabela.
- `p73_tipo_pessoa`: Indica se é pessoa física ou jurídica.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p73_tipo_pessoa`: Indica se é pessoa física ou jurídica.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmalt`

### Identidade

- Nome humano: Cgm's Alterados ou Excluidos.
- O que representa: Cgm's Alterados ou Excluidos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z05_sequencia`
- Coluna temporal: `z05_data_alt`
- Candidatas a chave de negocio: z05_cpf, z05_ident, z05_incest, z05_nacion, z05_numcgm
- Candidatas a coluna temporal: z05_data_alt, z05_nasc

### Colunas principais

- `z05_baicon`: Bairro do endereco comercial
- `z05_bairro`: Bairro
- `z05_cadast`: Dia em que este registro foi cadastrado
- `z05_celcon`: Celular comercial
- `z05_cep`: CEP
- `z05_cepcon`: CEP do endereco comercial
- `z05_cgc`: CNPJ para empresas
- `z05_cgccpf`: Código do CNPJ quando empresa ou Código do CPF quando pessoa física
- `z05_comcon`: Complemento do numero do endereco comercial
- `z05_compl`: Complemento do numero do endereco
- `z05_contato`: Contato
- `z05_cpf`: Codigo do CPF do contribuinte
- `z05_cxposcon`: caixa postal do endereco comercial do contribuinte
- `z05_cxpostal`: Caixa postal do contribuinte cadastrado
- `z05_data_alt`: Data
- `z05_email`: email
- `z05_emailc`: email comercial
- `z05_endcon`: Endereco Comercial
- `z05_ender`: Endereço
- `z05_estciv`: Estado civil (pessoa fisica)
- `z05_fax`: Fax
- `z05_hora`: Hora da Cadastramento
- `z05_hora_alt`: Hora
- `z05_ident`: Identidade (pessoa fisica)
- `z05_incest`: Inscricao Estadual (pessoa juridica)
- `z05_login`: Login do usuario que cadastrou este registro
- `z05_login_alt`: Login
- `z05_mae`: Mãe
- `z05_muncon`: Municipio do endereco comercial
- `z05_munic`: Município
- `z05_nacion`: Codigo da nacionalidade
- `z05_nasc`: Data de Nascimento
- `z05_nome`: Nome da pessoa ou Razao Social se for Empresa
- `z05_nomefanta`: Nome Fantasia da empresa
- `z05_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `z05_numcon`: Numero do endereco comercial
- `z05_numero`: Numero do endereco
- `z05_pai`: Pai
- `z05_profis`: Profissao (pessoa fisica)
- `z05_sequencia`: Sequencial da tabela
- `z05_sexo`: Sexo
- `z05_telcel`: Telefone Celular
- `z05_telcon`: Telefone comercial
- `z05_telef`: Telefone
- `z05_tipcre`: 1=administracao publica 2=privada
- `z05_tipo_alt`: Tipo de alteração
- `z05_uf`: Unidade Federativa (estado)
- `z05_ufcon`: Estado do endereco comercial para localização do contribuinte
- `z05_ultalt`: Ultima Alteração

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z05_baicon`: Bairro do endereco comercial
- `z05_bairro`: Bairro
- `z05_cpf`: Codigo do CPF do contribuinte
- `z05_data_alt`: Data
- `z05_nacion`: Codigo da nacionalidade
- `z05_nasc`: Data de Nascimento
- `z05_tipo_alt`: Tipo de alteração

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmcomposicaofamiliar`

### Identidade

- Nome humano: Composição Familiar do CGM.
- O que representa: Composição Familiar do CGM
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z15_sequencial`
- Coluna temporal: `z15_datafinal`
- Candidatas a chave de negocio: z15_numcgm, z15_sequencial
- Candidatas a coluna temporal: z15_datafinal, z15_datainicial

### Colunas principais

- `z15_cgmfamilia`: Familia do CGM
- `z15_cgmtipofamiliar`: Tipo de Familiar do CGM
- `z15_datafinal`: Data Final
- `z15_datainicial`: Data Inicial
- `z15_numcgm`: Cgm
- `z15_sequencial`: Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z15_cgmtipofamiliar`: Tipo de Familiar do CGM
- `z15_datafinal`: Data Final
- `z15_datainicial`: Data Inicial

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z15_cgmfamilia` -> `protocolo.cgmfamilia` (z13_sequencial) [cgmcomposicaofamiliar_cgmfamilia_fk]
- `z15_cgmtipofamiliar` -> `protocolo.tipofamiliar` (z14_sequencial) [cgmcomposicaofamiliar_cgmtipofamiliar_fk]
- `z15_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmcomposicaofamiliar_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmcorreto`

### Identidade

- Nome humano: Tabela utilizada para consistenciação do CGM, ou seja, tirar os duplos literalmente..
- O que representa: Tabela utilizada para consistenciação do CGM, ou seja, tirar os duplos literalmente.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z10_codigo`
- Coluna temporal: `z10_data`
- Candidatas a chave de negocio: z10_codigo, z10_login, z10_numcgm
- Candidatas a coluna temporal: z10_data

### Colunas principais

- `z10_codigo`: Código
- `z10_data`: Data da inclusão do registro
- `z10_hora`: Hora da inclusão do registro
- `z10_instit`: Código da Instituição
- `z10_login`: codigo do usuario
- `z10_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `z10_proc`: Se registro ja foi processado

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z10_codigo`: Código
- `z10_data`: Data da inclusão do registro
- `z10_login`: codigo do usuario

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z10_instit` -> `configuracoes.db_config` (codigo) [cgmcorreto_instit_fk]
- `z10_login` -> `configuracoes.db_usuarios` (id_usuario) [cgmcorreto_login_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmdepara`

### Identidade

- Nome humano: protocolo.cgmdepara.
- O que representa: Preencher em linguagem de negocio.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z01_numcgm, z01_numcgm_2
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z01_bairro`: Preencher significado.
- `z01_bairro_2`: Preencher significado.
- `z01_cep`: Preencher significado.
- `z01_cep_2`: Preencher significado.
- `z01_cgccpf`: Preencher significado.
- `z01_cgccpf_2`: Preencher significado.
- `z01_compl`: Preencher significado.
- `z01_compl_2`: Preencher significado.
- `z01_ender`: Preencher significado.
- `z01_ender_2`: Preencher significado.
- `z01_munic`: Preencher significado.
- `z01_munic_2`: Preencher significado.
- `z01_nome`: Preencher significado.
- `z01_nome_2`: Preencher significado.
- `z01_nomecomple`: Preencher significado.
- `z01_nomecomple_2`: Preencher significado.
- `z01_nomefanta`: Preencher significado.
- `z01_nomefanta_2`: Preencher significado.
- `z01_numcgm`: Preencher significado.
- `z01_numcgm_2`: Preencher significado.
- `z01_numero`: Preencher significado.
- `z01_numero_2`: Preencher significado.
- `z01_uf`: Preencher significado.
- `z01_uf_2`: Preencher significado.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z01_bairro`
- `z01_bairro_2`

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmdoc`

### Identidade

- Nome humano: Dados Adicionais do CGM.
- O que representa: Dados Adicionais do CGM
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z02_i_sequencial`
- Coluna temporal: `z02_d_certidaodata`
- Candidatas a chave de negocio: z02_c_certidaocartorio, z02_c_certidaolivro, z02_c_identorgao, z02_c_identuf, z02_c_naturalidade
- Candidatas a coluna temporal: z02_d_certidaodata, z02_d_ctpsdata, z02_d_dataentrada, z02_d_identdata

### Colunas principais

- `z02_c_agencia`: Agência
- `z02_c_banco`: Banco
- `z02_c_certidaocartorio`: Nome do Cartório
- `z02_c_certidaolivro`: Livro
- `z02_c_contacorrente`: N° Conta Corrente
- `z02_c_ctpsnum`: CTPS N°
- `z02_c_ctpsserie`: CTPS Série
- `z02_c_ctpsuf`: CTPS UF
- `z02_c_folha`: Folha
- `z02_c_identorgao`: Órgão Emissor
- `z02_c_identuf`: UF da Identidade
- `z02_c_naturalidade`: Naturalidade
- `z02_c_naturalidadeuf`: UF da Naturalidade
- `z02_c_pais`: País de Origem
- `z02_c_termo`: Termo
- `z02_d_certidaodata`: Data de Emissão
- `z02_d_ctpsdata`: CTPS Data de Emissão
- `z02_d_dataentrada`: Data de Entrada no País
- `z02_d_identdata`: Data de Expedição
- `z02_i_certidaotipo`: Tipo de Certidão
- `z02_i_cgm`: CGM
- `z02_i_cns`: Cartão Nacional de Saude
- `z02_i_escolaridade`: Escolaridade
- `z02_i_pis`: PIS / PASEP
- `z02_i_sequencial`: Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z02_d_certidaodata`: Data de Emissão
- `z02_d_ctpsdata`: CTPS Data de Emissão
- `z02_d_dataentrada`: Data de Entrada no País
- `z02_d_identdata`: Data de Expedição
- `z02_i_certidaotipo`: Tipo de Certidão

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z02_i_cgm` -> `protocolo.cgm` (z01_numcgm) [cgmdoc_cgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmenderecoexterior`

### Identidade

- Nome humano: Endereço fora do Brasil, inicialmente para atender o e-social.
- O que representa: Endereço fora do Brasil, inicialmente para atender o e-social
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z19_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z19_cidade, z19_codigopostal, z19_numcgm, z19_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z19_bairro`: Bairro do endereço
- `z19_cidade`: Cidade do endereço no exterior
- `z19_codigopostal`: Código Postal
- `z19_complemento`: Complemento do endereço
- `z19_logradouro`: Logradouro do endereço no exterior
- `z19_numcgm`: Vinculo com a tabela cgm
- `z19_numero`: Número do logradouro
- `z19_pais`: País do endereço no exterior
- `z19_sequencial`: Código Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z19_bairro`: Bairro do endereço
- `z19_codigopostal`: Código Postal

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z19_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmenderecoexterior_numcgm_fk]
- `z19_pais` -> `configuracoes.cadenderpais` (db70_sequencial) [cgmenderecoexterior_pais_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmerrado`

### Identidade

- Nome humano: Lista dos CGM's errados, os quais, serão trocados pelo cgm que está na tabela cgmcorreto.
- O que representa: Lista dos CGM's errados, os quais, serão trocados pelo cgm que está na tabela cgmcorreto
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z11_codigo`
  - `z11_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z11_codigo, z11_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z11_codigo`: Código
- `z11_nome`: Nome da pessoa ou Razao Social se for Empresa
- `z11_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z11_codigo`: Código

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z11_codigo` -> `protocolo.cgmcorreto` (z10_codigo) [cgmerrado_codigo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmerradolog`

### Identidade

- Nome humano: Log do cgm errado.
- O que representa: Log do cgm errado
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z12_codigo`
  - `z12_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z12_codigo, z12_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z12_codigo`: Código
- `z12_log`: Log do que foi feito durante o processamento
- `z12_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z12_codigo`: Código

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z12_codigo, z12_codigo, z12_numcgm, z12_numcgm` -> `protocolo.cgmerrado` (z11_codigo, z11_numcgm, z11_numcgm, z11_codigo) [cgmerradolog_codigo_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmestrangeiro`

### Identidade

- Nome humano: Informações para um CGM estrangeiro.
- O que representa: Informações para um CGM estrangeiro
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z09_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z09_cidade, z09_numcgm, z09_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z09_cidade`: Cidade estrangeira
- `z09_documento`: Documento
- `z09_numcgm`: Código do CGM
- `z09_pais`: País estrangeiro
- `z09_sequencial`: Código

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z09_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmestrangeiro_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmfamilia`

### Identidade

- Nome humano: Familia do CGM.
- O que representa: Familia do CGM
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z13_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z13_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z13_sequencial`: Sequencial da Família

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmfisico`

### Identidade

- Nome humano: Cgm Físico.
- O que representa: Cgm Físico
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z04_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z04_numcgm, z04_paisnacionalidade, z04_rhcbo, z04_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z04_nomesocial`: Nome Social para atender legislação
- `z04_numcgm`: Código CGM
- `z04_paisnacionalidade`: País Nacionalidade
- `z04_paisnascimento`: País onde a pessoa nasceu
- `z04_rhcbo`: Código sequencial da CBO
- `z04_sequencial`: Código Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z04_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmfisico_numcgm_fk]
- `z04_paisnacionalidade` -> `configuracoes.cadenderpais` (db70_sequencial) [cgmfisico_paisnacionalidade_fk]
- `z04_paisnascimento` -> `configuracoes.cadenderpais` (db70_sequencial) [cgmfisico_paisnascimento_fk]
- `z04_rhcbo` -> `pessoal.rhcbo` (rh70_sequencial) [cgmfisico_z04_cbo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmfoto`

### Identidade

- Nome humano: Fotos do Cadastro Geral do Município.
- O que representa: Fotos do Cadastro Geral do Município
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z16_sequencial`
- Coluna temporal: `z16_data`
- Candidatas a chave de negocio: z16_id_usuario, z16_numcgm, z16_sequencial
- Candidatas a coluna temporal: z16_data

### Colunas principais

- `z16_arquivofoto`: Arquivo da Foto
- `z16_data`: Data de Inclusão
- `z16_fotoativa`: Foto Ativa
- `z16_hora`: Hora da Incluisão
- `z16_id_usuario`: usuário
- `z16_numcgm`: Número de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `z16_principal`: Foto Principal - Foto que será mostrada no cadastro do cgm, e em relatórios.
- `z16_sequencial`: Código da Foto

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z16_data`: Data de Inclusão

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z16_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmfoto_numcgm_fk]
- `z16_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [cgmfoto_usuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmjuridico`

### Identidade

- Nome humano: Cgm Jurídico.
- O que representa: Cgm Jurídico
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z08_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z08_numcgm, z08_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z08_nire`: Nire
- `z08_numcgm`: Código CGM
- `z08_sequencial`: Código Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z08_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmjuridico_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmsaude`

### Identidade

- Nome humano: Informações inerentes ao Módulo Saúde.
- O que representa: Informações inerentes ao Módulo Saúde
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z01_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z01_cartaosus`: Cartão SUS
- `z01_fatorrh`: Fator RH
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município
- `z01_tiposangue`: Tipo Sanguineo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z01_tiposangue`: Tipo Sanguineo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z01_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmsaude_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.cgmtipoempresa`

### Identidade

- Nome humano: Ligação entre cgm e tipoempresa.
- O que representa: Ligação entre cgm e tipoempresa
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z03_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z03_numcgm, z03_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z03_numcgm`: Codigo do CGM
- `z03_sequencial`: Código Sequencial
- `z03_tipoempresa`: Código Tipo Empresa

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z03_numcgm`: Codigo do CGM
- `z03_tipoempresa`: Código Tipo Empresa

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z03_numcgm` -> `protocolo.cgm` (z01_numcgm) [cgmtipoempresa_numcgm_fk]
- `z03_tipoempresa` -> `configuracoes.tipoempresa` (db98_sequencial) [cgmtipoempresa_tipoempresa_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_ceplog`

### Identidade

- Nome humano: tabela de Cep por logradouro.
- O que representa: tabela de Cep por logradouro
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `db11_codlog`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: db11_codigo
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `db11_bairro`: bairro
- `db11_cep`: Cep
- `db11_codigo`: Código do Município
- `db11_codlog`: Código do Logradouro
- `db11_logradouro`: Logradouro
- `db11_logsemacento`: Logradouro sem Acento
- `db11_tipo`: Tipo de Logradouro

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `db11_bairro`: bairro
- `db11_codigo`: Código do Município
- `db11_tipo`: Tipo de Logradouro

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `db11_codigo` -> `protocolo.db_cepmunic` (db10_codigo) [db_ceplog_codigo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_cepmunic`

### Identidade

- Nome humano: tabela de cep do municipio.
- O que representa: tabela de cep do municipio
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `db10_codigo`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: db10_codigo
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `db10_cep`: Cep
- `db10_codibge`: Código do município no cadastro do IBGE
- `db10_codigo`: Código do cep
- `db10_munic`: Município
- `db10_uf`: UF

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `db10_codigo`: Código do cep

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `db10_uf` -> `protocolo.db_uf` (db12_codigo) [db_cepmunic_uf_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_cgmbairro`

### Identidade

- Nome humano: Tabela com o bairro dos contribuinte que morram no município..
- O que representa: Tabela com o bairro dos contribuinte que morram no município.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z01_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `j13_codi`: Código do bairro
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `j13_codi`: Código do bairro

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `j13_codi` -> `cadastro.bairro` (j13_codi) [db_cgmbairro_codi_fk]
- `z01_numcgm` -> `protocolo.cgm` (z01_numcgm) [db_cgmbairro_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_cgmcgc`

### Identidade

- Nome humano: Cadastro do CNPj do cgm.
- O que representa: Cadastro do CNPj do cgm
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z01_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z01_cgc`: CNPJ para empresas
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z01_numcgm` -> `protocolo.cgm` (z01_numcgm) [db_cgmcgc_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_cgmcpf`

### Identidade

- Nome humano: cadastro do CPF do cgm.
- O que representa: cadastro do CPF do cgm
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z01_cpf, z01_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z01_cpf`: Codigo do CPF do contribuinte
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `z01_cpf`: Codigo do CPF do contribuinte

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `z01_numcgm` -> `protocolo.cgm` (z01_numcgm) [db_cgmcpf_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_cgmruas`

### Identidade

- Nome humano: Indica o codigo do logradourodo cgm quando este é do municipio.
- O que representa: Indica o codigo do logradourodo cgm quando este é do municipio
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z01_numcgm`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: j14_codigo, z01_numcgm
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `j14_codigo`: código do logradouro cadastrado no sistema
- `z01_numcgm`: Numero de Identificação do Contribuinte ou Empresa no Cadastro geral do Município

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `j14_codigo`: código do logradouro cadastrado no sistema

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `j14_codigo` -> `cadastro.ruas` (j14_codigo) [db_cgmruas_codigo_fk]
- `z01_numcgm` -> `protocolo.cgm` (z01_numcgm) [db_cgmruas_numcgm_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.db_uf`

### Identidade

- Nome humano: tabela com os estados brasileiros.
- O que representa: tabela com os estados brasileiros
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `db12_codigo`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: db12_codigo
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `db12_codigo`: código do estado
- `db12_extenso`: Estado por extenso
- `db12_nome`: Nome
- `db12_uf`: descrição do estado

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `db12_codigo`: código do estado

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.gestaodepartamentoprocesso`

### Identidade

- Nome humano: Armazena o usuário responsável pela gestão de processos em um departamento e que pode visualizar o relatório de processos vencidos com somente dados do departamento em que é responsável..
- O que representa: Armazena o usuário responsável pela gestão de processos em um departamento e que pode visualizar o relatório de processos vencidos com somente dados do departamento em que é responsável.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p103_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p103_db_depart, p103_db_usuarios, p103_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p103_db_depart`: Código do departamento que será administrado os processos vencidos.
- `p103_db_usuarios`: Código do usuário responsável pelos processos vencidos em um departamento.
- `p103_sequencial`: Código sequencial.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p103_db_depart` -> `configuracoes.db_depart` (coddepto) [gestaodepartamentoprocesso_depart_fk]
- `p103_db_usuarios` -> `configuracoes.db_usuarios` (id_usuario) [gestaodepartamentoprocesso_usuarios_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.gestaoprocessovencido`

### Identidade

- Nome humano: Armazena o usuário responsável pela gestão de processos e que pode visualizar no relatório de processos vencidos de todos os departamentos..
- O que representa: Armazena o usuário responsável pela gestão de processos e que pode visualizar no relatório de processos vencidos de todos os departamentos.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p102_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p102_db_usuarios, p102_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p102_db_usuarios`: Código do usuário responsável pelos processos vencidos.
- `p102_sequencial`: Código sequencial.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p102_db_usuarios` -> `configuracoes.db_usuarios` (id_usuario) [gestaoprocessovencido_usuarios_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.historico_tipo_processo`

### Identidade

- Nome humano: Registra as alterações no tipo do processo manual,eletrônico e ouvidoria..
- O que representa: Registra as alterações no tipo do processo manual,eletrônico e ouvidoria.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p112_sequencial`
- Coluna temporal: `p112_data_registro`
- Candidatas a chave de negocio: p112_codigoprocesso, p112_sequencial, p112_usuario
- Candidatas a coluna temporal: p112_data_registro

### Colunas principais

- `p112_codigoprocesso`: Código do Processo
- `p112_data_registro`: Data em qual foi efetuado a mudança no tipo de processo
- `p112_departamento`: Departamento referente ao usuário que solicitou mudança no tipo de processo.
- `p112_instituicao`: Instituição referente ao usuário que efetuou mudança no tipo do processo.
- `p112_sequencial`: Sequencial
- `p112_tipoprocesso`: Tipo de processo
- `p112_usuario`: Identificação do usuário

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p112_codigoprocesso`: Código do Processo
- `p112_data_registro`: Data em qual foi efetuado a mudança no tipo de processo
- `p112_departamento`: Departamento referente ao usuário que solicitou mudança no tipo de processo.
- `p112_instituicao`: Instituição referente ao usuário que efetuou mudança no tipo do processo.
- `p112_tipoprocesso`: Tipo de processo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p112_codigoprocesso` -> `protocolo.protprocesso` (p58_codproc) [historico_tipo_processo_p112_codigoprocesso_fkey]
- `p112_instituicao` -> `configuracoes.db_config` (codigo) [historico_tipo_processo_p112_instituicao_fkey]
- `p112_tipoprocesso` -> `protocolo.tipoprocesso` (p109_sequencial) [historico_tipo_processo_p112_tipoprocesso_fkey]
- `p112_usuario` -> `configuracoes.db_usuarios` (id_usuario) [historico_tipo_processo_p112_usuario_fkey]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.historicovisualizacaoprocandam`

### Identidade

- Nome humano: Histórico de visualização de mensagens referente ao andamento do processo.
- O que representa: Histórico de visualização de mensagens referente ao andamento do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p113_sequencial`
- Coluna temporal: `p113_data_registro`
- Candidatas a chave de negocio: p113_departamento_id, p113_instituicao_id, p113_procandamint_id, p113_sequencial, p113_usuario_id
- Candidatas a coluna temporal: p113_data_registro

### Colunas principais

- `p113_data_registro`: Data de Registro
- `p113_departamento_id`: Identificação do departamento
- `p113_instituicao_id`: Identificação da instituição
- `p113_procandamint_id`: procandamint
- `p113_sequencial`: Identificação da visualização
- `p113_usuario_id`: Identificação do usuário

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p113_data_registro`: Data de Registro

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p113_departamento_id` -> `configuracoes.db_depart` (coddepto) [fk_p113_departamento_id]
- `p113_instituicao_id` -> `configuracoes.db_config` (codigo) [fk_p113_instituicao_id]
- `p113_usuario_id` -> `configuracoes.db_usuarios` (id_usuario) [fk_p113_usuario_id]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.mensageriaprocesso`

### Identidade

- Nome humano: Armazena a configuração da mensagem de notificação do vencimento dos processos..
- O que representa: Armazena a configuração da mensagem de notificação do vencimento dos processos.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p101_sequencial`
- Coluna temporal: `p101_notificardatavencimento`
- Candidatas a chave de negocio: p101_diasprazo, p101_mensagem, p101_notificardatavencimento, p101_notificarreceberprocesso, p101_sequencial
- Candidatas a coluna temporal: p101_notificardatavencimento

### Colunas principais

- `p101_assunto`: Assunto da mensagem de notificação.
- `p101_diasprazo`: Quantidade de dias que o servidor tem para movimentar um processo a partir de seu recebimento.
- `p101_mensagem`: Mensagem de notificação de processo vencido.
- `p101_notificardatavencimento`: Notifica o servidor quando o processo atingiu seu prazo limite para movimentação.
- `p101_notificarreceberprocesso`: Notifica um servidor quando um processo é transferido ou tramitado para ele.
- `p101_permitirnotificardepartamento`: Habilita as notificações do mensageria por departamento.
- `p101_sequencial`: Código sequencial.
- `p101_tipoprazo`: Tipo de Prazo para definir de onde pegar o prazo de envio de notificação
- `p101_usuarioremetente`: Usuário Remetente, do envio da notificação

### Metricas atomicas

- `p101_diasprazo`: Quantidade de dias que o servidor tem para movimentar um processo a partir de seu recebimento.

### Dimensoes

- `p101_notificardatavencimento`: Notifica o servidor quando o processo atingiu seu prazo limite para movimentação.
- `p101_tipoprazo`: Tipo de Prazo para definir de onde pegar o prazo de envio de notificação

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procandam`

### Identidade

- Nome humano: Andamento do processo.
- O que representa: Andamento do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p61_codandam`
- Coluna temporal: `p61_dtandam`
- Candidatas a chave de negocio: p61_id_usuario
- Candidatas a coluna temporal: p61_dtandam

### Colunas principais

- `p61_codandam`: Código andamento
- `p61_coddepto`: Código do departamento
- `p61_codproc`: Código do processo
- `p61_despacho`: parecer do processo
- `p61_dtandam`: Data do andamento
- `p61_hora`: Hora do Andamento
- `p61_id_usuario`: id do usuario que efetvou o registro
- `p61_publico`: Despacho Publico

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p61_dtandam`: Data do andamento

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p61_coddepto` -> `configuracoes.db_depart` (coddepto) [procandam_coddepto_fk]
- `p61_codproc` -> `protocolo.protprocesso` (p58_codproc) [procandam_codproc_fk]
- `p61_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [procandam_id_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procandamint`

### Identidade

- Nome humano: Andamento Interno.
- O que representa: Andamento Interno
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p78_sequencial`
- Coluna temporal: `p78_data`
- Candidatas a chave de negocio: p78_sequencial, p78_usuario
- Candidatas a coluna temporal: p78_data

### Colunas principais

- `p78_codandam`: Código andamento
- `p78_data`: Data do andamento interno
- `p78_despacho`: Despacho Interno do andamento
- `p78_hora`: Hora do andamento
- `p78_publico`: Despacho Publico
- `p78_sequencial`: Codigo sequencial da tabela
- `p78_tipodespacho`: Tipo de Despacho
- `p78_transint`: diz se despacho interno com transferência ou não Tranferencia Interna
- `p78_usuario`: codigo do usuario

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p78_data`: Data do andamento interno
- `p78_sequencial`: Codigo sequencial da tabela
- `p78_tipodespacho`: Tipo de Despacho
- `p78_usuario`: codigo do usuario

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p78_codandam` -> `protocolo.procandam` (p61_codandam) [procandamint_codandam_fk]
- `p78_tipodespacho` -> `protocolo.tipodespacho` (p100_sequencial) [procandamint_tipodespacho_fk]
- `p78_usuario` -> `configuracoes.db_usuarios` (id_usuario) [procandamint_usuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procandamintand`

### Identidade

- Nome humano: Andamento e Tranferência.
- O que representa: Andamento e Tranferência
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: `p86_codtrans`
- Candidatas a chave de negocio: p86_codtrans
- Candidatas a coluna temporal: p86_codtrans

### Colunas principais

- `p86_codandam`: Código andamento
- `p86_codtrans`: codigo da tranferência

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p86_codtrans`: codigo da tranferência

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p86_codandam` -> `protocolo.procandam` (p61_codandam) [procandamintand_codandam_fk]
- `p86_codtrans` -> `protocolo.proctransferint` (p88_codigo) [procandamintand_codtrans_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procandamintusu`

### Identidade

- Nome humano: usuario atual do andamento interno dos processos.
- O que representa: usuario atual do andamento interno dos processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p79_codandamint`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p79_codandamint, p79_usuario
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p79_codandamint`: Codigo sequencial da tabela procandamint
- `p79_usuario`: codigo do usuario de destino

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p79_codandamint`: Codigo sequencial da tabela procandamint
- `p79_usuario`: codigo do usuario de destino

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p79_codandamint` -> `protocolo.procandamint` (p78_sequencial) [procandamintusu_codandamint_fk]
- `p79_usuario` -> `configuracoes.db_usuarios` (id_usuario) [procandamintusu_usuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procarquiv`

### Identidade

- Nome humano: Arquivamento dos Processos.
- O que representa: Arquivamento dos Processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p67_codarquiv`
- Coluna temporal: `p67_dtarq`
- Candidatas a chave de negocio: p67_id_usuario
- Candidatas a coluna temporal: p67_dtarq

### Colunas principais

- `p67_codarquiv`: Código do Arquivamento
- `p67_coddepto`: Código do departamento
- `p67_codproc`: Código do processo
- `p67_dtarq`: Data do Arquivamento
- `p67_historico`: Histórico do Arquivamento
- `p67_id_usuario`: Código do Usuário

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p67_dtarq`: Data do Arquivamento

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procdoc`

### Identidade

- Nome humano: Documentos necessários para encaminhamento do processo.
- O que representa: Documentos necessários para encaminhamento do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p56_coddoc`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p56_ouvidoriatipodado
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p56_coddoc`: Código do documento
- `p56_descr`: Descrição do documento
- `p56_ouvidoriatipodado`: Tipo de dado do documento, válido para ouvidoria externa: Texto Livre; Numérico; Valor; Endereço; Arquivo.

### Metricas atomicas

- `p56_ouvidoriatipodado`: Tipo de dado do documento, válido para ouvidoria externa: Texto Livre; Numérico; Valor; Endereço; Arquivo.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procdoctipo`

### Identidade

- Nome humano: Indica o tipo do documento.
- O que representa: Indica o tipo do documento
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p57_codigo`
  - `p57_coddoc`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p57_codigo, p57_ouvidoriaobrigatorio
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p57_coddoc`: Código de documentos
- `p57_codigo`: Código do tipo de documento do processo
- `p57_ouvidoriaobrigatorio`: Controla se o documento, vinculado ao tipo de processo, é obrigatório para sistemas externos.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p57_codigo`: Código do tipo de documento do processo
- `p57_ouvidoriaobrigatorio`: Controla se o documento, vinculado ao tipo de processo, é obrigatório para sistemas externos.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p57_coddoc` -> `protocolo.procdoc` (p56_coddoc) [procdoctipo_coddoc_fk]
- `p57_codigo` -> `protocolo.tipoproc` (p51_codigo) [procdoctipo_codigo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.processoinscr`

### Identidade

- Nome humano: Processo de inscrição.
- O que representa: Processo de inscrição
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p82_codigo, p82_inscr
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p82_codigo`: código
- `p82_inscr`: inscrição

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p82_codigo`: código

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.processomatric`

### Identidade

- Nome humano: processo de matrícula.
- O que representa: processo de matrícula
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p81_codigo, p81_matric
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p81_codigo`: código
- `p81_matric`: matrícula

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p81_codigo`: código
- `p81_matric`: matrícula

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.processosapensados`

### Identidade

- Nome humano: Apensar Processos.
- O que representa: Apensar Processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p30_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p30_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p30_procapensado`: Processo Apensado
- `p30_procprincipal`: Processo Principal
- `p30_sequencial`: Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p30_procapensado` -> `protocolo.protprocesso` (p58_codproc) [processosapensados_procapensado_fk]
- `p30_procprincipal` -> `protocolo.protprocesso` (p58_codproc) [processosapensados_procprincipal_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.processosvinculados`

### Identidade

- Nome humano: Armazena vínculo entre processo do e-cidade e processo da Ouvidoria..
- O que representa: Armazena vínculo entre processo do e-cidade e processo da Ouvidoria.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p92_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p92_processofilho, p92_processopai, p92_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p92_processofilho`: Processo referente a uma mensagem enviada do e-cidade para a ouvidoria ou da ouvidoria para o e-cidade.
- `p92_processopai`: Processo do e-cidade que é pai de um processo filho. Esse processo filho pode ser processo aberto para enviar uma mensagem para a Ouvidoria ou uma mensagem enviada da Ouvidoria para o e-cidade.
- `p92_sequencial`: PK da tabela processosvinculados.
- `p92_tipo`: Tipo de Documento do Processo.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p92_tipo`: Tipo de Documento do Processo.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p92_processofilho` -> `protocolo.protprocesso` (p58_codproc) [processosvinculados_p92_sequencial_seq_processofilho_fk]
- `p92_processopai` -> `protocolo.protprocesso` (p58_codproc) [processosvinculados_p92_sequencial_seq_processopai_fk]
- `p92_tipo` -> `protocolo.prottipodocumentoprocesso` (p91_sequencial) [processosvinculados_p92_sequencial_seq_tipo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procimag`

### Identidade

- Nome humano: imagens do processo.
- O que representa: imagens do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p64_codproc`: Código do processo
- `p64_imagem`: Imagem

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p64_codproc` -> `protocolo.protprocesso` (p58_codproc) [procimag_codproc_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procinscr`

### Identidade

- Nome humano: controle da inscrição.
- O que representa: controle da inscrição
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p60_inscr
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p60_codproc`: Código do processo
- `p60_inscr`: inscrição do iss

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p60_codproc` -> `protocolo.protprocesso` (p58_codproc) [procinscr_codproc_fk]
- `p60_inscr` -> `issqn.issbase` (q02_inscr) [procinscr_inscr_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procmatric`

### Identidade

- Nome humano: Relacionamentos.
- O que representa: Relacionamentos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p59_matric
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p59_codproc`: código do processo
- `p59_matric`: Código da matricula do iptu

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p59_matric`: Código da matricula do iptu

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p59_codproc` -> `protocolo.protprocesso` (p58_codproc) [procmatric_codproc_fk]
- `p59_matric` -> `cadastro.iptubase` (j01_matric) [procmatric_matric_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procprocessodesp`

### Identidade

- Nome humano: Inclusão dos despachos dos processos incluídos pelos usuários.
- O que representa: Inclusão dos despachos dos processos incluídos pelos usuários
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p80_coddesp`
- Coluna temporal: `p80_data`
- Candidatas a chave de negocio: p80_codigo, p80_id_usuario
- Candidatas a coluna temporal: p80_data

### Colunas principais

- `p80_coddesp`: Código Despacho
- `p80_codigo`: código
- `p80_data`: Data da inclusão do despacho
- `p80_despacho`: Despacho digitado pelo usuário
- `p80_hora`: Hora da inclusão
- `p80_id_usuario`: Usuário que digitou o despacho

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p80_codigo`: código
- `p80_data`: Data da inclusão do despacho

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p80_codigo` -> `protocolo.protprocesso` (p58_codproc) [procprocessodesp_codigo_fk]
- `p80_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [procprocessodesp_id_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procprocessodoc`

### Identidade

- Nome humano: documentos utilizados no processo.
- O que representa: documentos utilizados no processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p81_codproc`
  - `p81_coddoc`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p81_doc
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p81_coddoc`: Código do documento
- `p81_codproc`: Código do processo
- `p81_doc`: indica quais os documentos foram trazidos para o processo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p81_coddoc` -> `protocolo.procdoc` (p56_coddoc) [procprocessodoc_coddoc_fk]
- `p81_codproc` -> `protocolo.protprocesso` (p58_codproc) [procprocessodoc_codproc_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procrec`

### Identidade

- Nome humano: Cadastros das receitas para os tipos de processos.
- O que representa: Cadastros das receitas para os tipos de processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p52_codigo`
  - `p52_codrec`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p52_codigo
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p52_codigo`: Código do Tipo de Processo
- `p52_codrec`: Código da Receita de Processos
- `p52_valor`: Valor da Taxa a ser cobrada pelo Processo

### Metricas atomicas

- `p52_valor`: Valor da Taxa a ser cobrada pelo Processo

### Dimensoes

- `p52_codigo`: Código do Tipo de Processo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p52_codigo` -> `protocolo.tipoproc` (p51_codigo) [procrec_codigo_fk]
- `p52_codrec` -> `caixa.tabrec` (k02_codigo) [procrec_codrec_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctipovar`

### Identidade

- Nome humano: Controla o tipo do processo.
- O que representa: Controla o tipo do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p55_codproc`
  - `p55_codvar`
  - `p55_codcam`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p55_codcam, p55_codproc
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p55_codcam`: Código do campo para identificar na tabela
- `p55_codproc`: codigo do processo
- `p55_codvar`: código da variável
- `p55_conteudo`: conteúdo do tipo de variável por processo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p55_codproc`: codigo do processo
- `p55_conteudo`: conteúdo do tipo de variável por processo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p55_codproc` -> `protocolo.protprocesso` (p58_codproc) [proctipovar_codproc_fk]
- `p55_codvar, p55_codvar, p55_codcam, p55_codcam` -> `protocolo.procvar` (p54_codigo, p54_codcam, p54_codigo, p54_codcam) [proctipovar_codvar_codcam_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransand`

### Identidade

- Nome humano: Controle da transferência dos processos.
- O que representa: Controle da transferência dos processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: `p64_codtran`
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: p64_codtran

### Colunas principais

- `p64_codandam`: Código do andamento
- `p64_codtran`: Código da Transferência

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransfer`

### Identidade

- Nome humano: Controle da transferência dos departamentos.
- O que representa: Controle da transferência dos departamentos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p62_codtran`
- Coluna temporal: `p62_codtran`
- Candidatas a chave de negocio: p62_id_usorec, p62_id_usuario
- Candidatas a coluna temporal: p62_codtran, p62_dttran

### Colunas principais

- `p62_coddepto`: Código do departamento
- `p62_coddeptorec`: Código do departamento que recebeu o processo
- `p62_codtran`: Código da transferência
- `p62_dttran`: Data da transferencia
- `p62_hora`: Hora da transferencia
- `p62_id_usorec`: Id do usuario que recebeu o processo
- `p62_id_usuario`: is usuario

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p62_dttran`: Data da transferencia

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p62_coddepto` -> `configuracoes.db_depart` (coddepto) [proctransfer_coddepto_fk]
- `p62_coddeptorec` -> `configuracoes.db_depart` (coddepto) [proctransfer_p62_coddeptorec_fkey]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransferint`

### Identidade

- Nome humano: tranferencia interna de processos.
- O que representa: tranferencia interna de processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p88_codigo`
- Coluna temporal: `p88_data`
- Candidatas a chave de negocio: p88_codigo
- Candidatas a coluna temporal: p88_data

### Colunas principais

- `p88_codigo`: codigo sequencial do registro
- `p88_data`: Data da Transfêrencia Interna
- `p88_despacho`: Despacho Interno
- `p88_hora`: Hora da Transfêrencia Interna
- `p88_publico`: Despacho Publico
- `p88_usuario`: Usuário atual

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p88_codigo`: codigo sequencial do registro
- `p88_data`: Data da Transfêrencia Interna

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p88_usuario` -> `configuracoes.db_usuarios` (id_usuario) [proctransferint_usuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransferintand`

### Identidade

- Nome humano: andamento da tranferencia do processo.
- O que representa: andamento da tranferencia do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: `p87_codtransferint`
- Candidatas a chave de negocio: p87_codtransferint
- Candidatas a coluna temporal: p87_codtransferint

### Colunas principais

- `p87_codandam`: Código andamento
- `p87_codtransferint`: codigo da transferência interna

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p87_codtransferint`: codigo da transferência interna

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p87_codandam` -> `protocolo.procandam` (p61_codandam) [proctransferintand_codandam_fk]
- `p87_codtransferint` -> `protocolo.proctransferint` (p88_codigo) [proctransferintand_codtransferint_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransferintusu`

### Identidade

- Nome humano: usuario de destino.
- O que representa: usuario de destino
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: `p89_codtransferint`
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: p89_codtransferint

### Colunas principais

- `p89_codtransferint`: Codígo da Tranferência Interna
- `p89_usuario`: Usuário Destino

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p89_codtransferint` -> `protocolo.proctransferint` (p88_codigo) [proctransferintusu_codtransferint_fk]
- `p89_usuario` -> `configuracoes.db_usuarios` (id_usuario) [proctransferintusu_usuario_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransferproc`

### Identidade

- Nome humano: controla a transferencia por processo.
- O que representa: controla a transferencia por processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p63_codtran`
  - `p63_codproc`
- Coluna temporal: `p63_codtran`
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: p63_codtran

### Colunas principais

- `p63_codproc`: Código do processo
- `p63_codtran`: Código da transferencia

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p63_codproc` -> `protocolo.protprocesso` (p58_codproc) [proctransferproc_codproc_fk]
- `p63_codtran` -> `protocolo.proctransfer` (p62_codtran) [proctransferproc_codtran_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.proctransferworkflowativexec`

### Identidade

- Nome humano: proctransferworkflowativexec.
- O que representa: proctransferworkflowativexec
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p46_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p46_sequencial, p46_workflowativexec
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p46_proctransfer`: Código Processo Transferência
- `p46_sequencial`: Código Sequencial
- `p46_workflowativexec`: Código Work Flow Atividade Execução

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p46_proctransfer` -> `protocolo.proctransfer` (p62_codtran) [proctransferworkflowativexec_proctransfer_fk]
- `p46_workflowativexec` -> `configuracoes.workflowativexec` (db113_sequencial) [proctransferworkflowativexec_workflowativexec_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.procvar`

### Identidade

- Nome humano: Variáveis do processo.
- O que representa: Variáveis do processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p54_codigo`
  - `p54_codcam`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p54_codcam, p54_codigo
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p54_codcam`: Código do campo para identificar na tabela
- `p54_codigo`: código do tipo de processo
- `p54_obrigatorio`: Variável Obrigatória ao Tipo de Processo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p54_codigo`: código do tipo de processo
- `p54_obrigatorio`: Variável Obrigatória ao Tipo de Processo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p54_codcam` -> `configuracoes.db_syscampo` (codcam) [procvar_codcam_fk]
- `p54_codigo` -> `protocolo.tipoproc` (p51_codigo) [procvar_codigo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protdoc`

### Identidade

- Nome humano: Documentos entregues.
- O que representa: Documentos entregues
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p65_coddoc`: Código do documento
- `p65_codproc`: Código do processo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protparam`

### Identidade

- Nome humano: Tabela de Manutenção de Parametros do Modulo Protocolo.
- O que representa: Tabela de Manutenção de Parametros do Modulo Protocolo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p90_histpadcert, p90_valcpfcnpj
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p90_alteracgmprot`: Se obriga usuario a atualizar o cgm durante a inclusao do processo de protocolo
- `p90_andatual`: Mostra andamento atual na consulta processos
- `p90_db_documentotemplate`: Documento Template
- `p90_debiaber`: Verifica se o contribuinte tem debitos em aberto na inclusão do processo
- `p90_depandamentopadrao`: Departamento para inclusão automática do andamento padrão. Ao incluir um tipo de processo, será gerado um andamento padrão automaticamente, baseado no departamento informado nos parâmetros institucionais. Este, será vinculado ao tipo de processo.
- `p90_despachoob`: Despacho Obrigatório.Se quando for transferir o processo é obrigatorio incluir um despacho para os processos.
- `p90_emiterecib`: Emite recibo na inclusão do processo
- `p90_histpadcert`: Historico padrão para certidões
- `p90_impdepto`: Imprime Departamento
- `p90_imprimevar`: Configura a impressão ou não de variáveis da capa de processo.
- `p90_impusuproc`: Imprime o usuário q criou o processo na capa do processo
- `p90_instit`: Código da Instituição
- `p90_minchardesp`: Minímo de Caracteres p/ o despacho.
- `p90_modelcapaproc`: Modelo da Capa do Processo
- `p90_taxagrupo`: Código do grupo de taxas
- `p90_traminic`: 1. permitir escolher departamentos diferentes; 2. nào permitir escolher departamentos diferentes; 3. permitir escolher departamentos diferentes, mas avisar o usuário;
- `p90_valcpfcnpj`: Valida CPF/CNPJ na inclusão de Processo de Protocolo,ou seja ,permite incluir processo para um CPF/CNPJ em branco

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p90_depandamentopadrao`: Departamento para inclusão automática do andamento padrão. Ao incluir um tipo de processo, será gerado um andamento padrão automaticamente, baseado no departamento informado nos parâmetros institucionais. Este, será vinculado ao tipo de processo.
- `p90_taxagrupo`: Código do grupo de taxas

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p90_taxagrupo` -> `caixa.taxagrupo` (k06_taxagrupo) [protparam_taxagrupo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protparamglobal`

### Identidade

- Nome humano: Armazena as configurações globais da rotina de processo..
- O que representa: Armazena as configurações globais da rotina de processo.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p06_sequencial`
- Coluna temporal: `p06_tipo`
- Candidatas a chave de negocio: p06_sequencial, p06_tipo
- Candidatas a coluna temporal: p06_tipo

### Colunas principais

- `p06_instituicao`: Código da Instituição ao qual a configuração está atrelada.
- `p06_sequencial`: Sequencial
- `p06_tipo`: Tipo de controle. 1 = controle pelo campo sequencial 2 = controle pelo sequencial do ano

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p06_tipo`: Tipo de controle. 1 = controle pelo campo sequencial 2 = controle pelo sequencial do ano

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protprocesso`

### Identidade

- Nome humano: Controla os processos.
- O que representa: Controla os processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p58_codproc`
- Coluna temporal: `p58_ano`
- Candidatas a chave de negocio: p58_codigo, p58_codproc, p58_id_usuario, p58_numcgm, p58_volume
- Candidatas a coluna temporal: p58_ano, p58_dtproc, p58_numero

### Colunas principais

- `p58_ano`: Ano do Processo
- `p58_codandam`: Código do andamento
- `p58_coddepto`: Código do departamento incial do processo
- `p58_codigo`: Código do tipo do processo
- `p58_codproc`: Número do código do Processo (Sequencial)
- `p58_despacho`: Despacho
- `p58_dtproc`: Data de entrada do processo no departamento
- `p58_hora`: Hora da inclusão do processo
- `p58_id_usuario`: número do id do usuário
- `p58_instit`: Código da Instituição
- `p58_interno`: Interno ou não
- `p58_numcgm`: Número do CGM - Código Geral do Município.Titular do Processo
- `p58_numero`: Número do Processo acompanhado do ano.
- `p58_numero2`: Preencher significado.
- `p58_obs`: Observações do processo.
- `p58_orgao`: Órgão no qual processo foi cadastrado.
- `p58_processopai`: Indica qual o processo pai caso o processo em questão seja um volume.
- `p58_publico`: Despacho Publico
- `p58_requer`: Descrição do requerimento
- `p58_tipoprocesso`: Vínculo com o tabela tipoprocesso.
- `p58_volume`: Campo que identifica volume.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p58_ano`: Ano do Processo
- `p58_codigo`: Código do tipo do processo
- `p58_dtproc`: Data de entrada do processo no departamento
- `p58_numero`: Número do Processo acompanhado do ano.
- `p58_tipoprocesso`: Vínculo com o tabela tipoprocesso.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p58_coddepto` -> `configuracoes.db_depart` (coddepto) [protprocesso_coddepto_fk]
- `p58_codigo` -> `protocolo.tipoproc` (p51_codigo) [protprocesso_codigo_fk]
- `p58_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [protprocesso_id_fk]
- `p58_numcgm` -> `protocolo.cgm` (z01_numcgm) [protprocesso_numcgm_fk]
- `p58_tipoprocesso` -> `protocolo.tipoprocesso` (p109_sequencial) [protprocesso_p58_tipoprocesso_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protprocessodocumento`

### Identidade

- Nome humano: ligação entre processos e seus arquivos.
- O que representa: ligação entre processos e seus arquivos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p01_sequencial`
- Coluna temporal: `p01_data`
- Candidatas a chave de negocio: p01_estorage, p01_protprocesso, p01_sequencial
- Candidatas a coluna temporal: p01_data

### Colunas principais

- `p01_data`: Data de cadastro do documento
- `p01_descricao`: Descrição do arquivo
- `p01_documento`: Documento
- `p01_estorage`: Informa se o documento está no e-Storage ou não, caso esse campo seja verdadeiro então o campo p01_nomedocumento contem a referência do documento no e-Storage, o valor default do campo é false para retrocompatibilidade
- `p01_nomedocumento`: Nome do documento(arquivo) do processo do protocolo.
- `p01_ordem`: Ordenação dos documentos do processo.
- `p01_procandamint`: Código do andamento do documento
- `p01_protprocesso`: Número do código do Processo (Sequencial)
- `p01_sequencial`: Sequencial de Documentos
- `p01_usuario`: Usuário que adicionou o documento

### Metricas atomicas

- `p01_estorage`: Informa se o documento está no e-Storage ou não, caso esse campo seja verdadeiro então o campo p01_nomedocumento contem a referência do documento no e-Storage, o valor default do campo é false para retrocompatibilidade

### Dimensoes

- `p01_data`: Data de cadastro do documento

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p01_protprocesso` -> `protocolo.protprocesso` (p58_codproc) [protprocessodocumento_protprocesso_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protprocessonumeracao`

### Identidade

- Nome humano: Guarda o próximo número do processo a ser gerado no ano..
- O que representa: Guarda o próximo número do processo a ser gerado no ano.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p07_sequencial`
- Coluna temporal: `p07_ano`
- Candidatas a chave de negocio: p07_sequencial
- Candidatas a coluna temporal: p07_ano

### Colunas principais

- `p07_ano`: Ano do Processo
- `p07_instit`: Instituição que o processo está relacionado.
- `p07_orgao`: órgão
- `p07_prottipodocumentoprocesso`: Tipo de documento do processo.
- `p07_proximonumero`: Próximo número do processo a ser gerado.
- `p07_sequencial`: Sequencial de controle da númeração do ùltimo processo.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p07_ano`: Ano do Processo
- `p07_prottipodocumentoprocesso`: Tipo de documento do processo.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p07_instit` -> `configuracoes.db_config` (codigo) [protprocessonumeracao_instit_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.protprocessonumeracaoorgao`

### Identidade

- Nome humano: protocolo.protprocessonumeracaoorgao.
- O que representa: Preencher em linguagem de negocio.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p07_sequencial`
- Coluna temporal: `p07_ano`
- Candidatas a chave de negocio: p07_sequencial
- Candidatas a coluna temporal: p07_ano

### Colunas principais

- `p07_ano`: Preencher significado.
- `p07_instit`: Preencher significado.
- `p07_orgao`: Preencher significado.
- `p07_proximonumero`: Preencher significado.
- `p07_sequencial`: Preencher significado.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p07_ano`

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p07_instit` -> `configuracoes.db_config` (codigo) [protprocessonumeracaoorgao_instit_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.prottipodocumentoprocesso`

### Identidade

- Nome humano: Tipo de Documento do Processo..
- O que representa: Tipo de Documento do Processo.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p91_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p91_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p91_descricao`: Tipo de Documento do Processo
- `p91_sequencial`: PK da tabela.
- `p91_sigla`: Sigla do tipo de documento.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p91_descricao`: Tipo de Documento do Processo
- `p91_sigla`: Sigla do tipo de documento.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.recibocanc`

### Identidade

- Nome humano: recibo.
- O que representa: recibo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: `p99_dtoper`
- Candidatas a chave de negocio: p99_numcgm
- Candidatas a coluna temporal: p99_dtoper, p99_dtvenc

### Colunas principais

- `p99_codsubrec`: codsubrec
- `p99_dtoper`: Data
- `p99_dtvenc`: Vencimento
- `p99_hist`: Historico
- `p99_numcgm`: Numcgm
- `p99_numdig`: Numdig
- `p99_numnov`: Numnov
- `p99_numpar`: Parcela
- `p99_numpre`: Numpre
- `p99_numtot`: Total
- `p99_receit`: Receita
- `p99_tipo`: Tipo
- `p99_tipojm`: Tipojm
- `p99_valor`: Valor

### Metricas atomicas

- `p99_numtot`: Total
- `p99_valor`: Valor

### Dimensoes

- `p99_dtoper`: Data
- `p99_tipo`: Tipo
- `p99_tipojm`: Tipojm

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipoarq`

### Identidade

- Nome humano: Tipo de Arquivamentos de processos.
- O que representa: Tipo de Arquivamentos de processos
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - Preencher.
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p66_codarq`: Código do Arquivamento
- `p66_descr`: Descrição do tipo do Arquivo.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p66_descr`: Descrição do tipo do Arquivo.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipodespacho`

### Identidade

- Nome humano: tipodespacho.
- O que representa: tipodespacho
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p100_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p100_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p100_descricao`: Descrição
- `p100_sequencial`: Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipofamiliar`

### Identidade

- Nome humano: Tipo de Familiar do CGM.
- O que representa: Tipo de Familiar do CGM
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `z14_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: z14_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `z14_descricao`: Descrição
- `z14_sequencial`: Sequencial

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- Preencher dimensoes de agrupamento/filtro.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipoproc`

### Identidade

- Nome humano: Tipos dos processos incluidos no protocolo.
- O que representa: Tipos dos processos incluidos no protocolo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p51_codigo`
- Coluna temporal: `p51_dtlimite`
- Candidatas a chave de negocio: p51_codigo, p51_identificado, p51_itemmenu, p51_linksaibamais
- Candidatas a coluna temporal: p51_dtlimite

### Colunas principais

- `p51_codigo`: Código do Tipo de Processo.
- `p51_descr`: Descrição do Tipo de Processo.
- `p51_dtlimite`: Data limite
- `p51_identificado`: Identificado
- `p51_instit`: Código da Instituição
- `p51_itemmenu`: Menu exibido no ambiente processo eletrônico
- `p51_linksaibamais`: link exibido no frontend processo eletrônico
- `p51_mensagem`: Mensagem padrão enviada para atendimento do processo eletrônico
- `p51_prottipodocumentoprocesso`: Tipo de documento do processo.
- `p51_tipoprocgrupo`: Tipo Processo Grupo

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p51_codigo`: Código do Tipo de Processo.
- `p51_descr`: Descrição do Tipo de Processo.
- `p51_dtlimite`: Data limite
- `p51_prottipodocumentoprocesso`: Tipo de documento do processo.
- `p51_tipoprocgrupo`: Tipo Processo Grupo

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p51_prottipodocumentoprocesso` -> `protocolo.prottipodocumentoprocesso` (p91_sequencial) [tipoproc_prottipodocumentoprocesso_fk]
- `p51_tipoprocgrupo` -> `ouvidoria.tipoprocgrupo` (p40_sequencial) [tipoproc_tipoprocgrupo_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipoprocesso`

### Identidade

- Nome humano: Tipos de processos. Inicialmente Manual, eletrônico e ouvidoria..
- O que representa: Tipos de processos. Inicialmente Manual, eletrônico e ouvidoria.
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p109_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p109_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p109_nome`: Nome do tipo de processo.
- `p109_sequencial`: Código sequencial da tabela.

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p109_nome`: Nome do tipo de processo.

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- Nenhum relacionamento catalogado.

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tipoprocessoformulario`

### Identidade

- Nome humano: tabela que guarda o json contendo a estrutura do atendimento para esse tipo de processo.
- O que representa: tabela que guarda o json contendo a estrutura do atendimento para esse tipo de processo
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p108_sequencial`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p108_sequencial
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p108_formulario`: formulario do tipo de processo
- `p108_rota`: A rota quer deve ser redirecionado ao clicar no link do card no processo eletrônico.
- `p108_sequencial`: sequencial da tabela
- `p108_tipoproc`: tipo do processo do formulario

### Metricas atomicas

- Preencher apenas se houver coluna numerica com significado de negocio.

### Dimensoes

- `p108_formulario`: formulario do tipo de processo
- `p108_tipoproc`: tipo do processo do formulario

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p108_tipoproc` -> `protocolo.tipoproc` (p51_codigo) [tipoprocessoformulario_tipoproc_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.

## Tabela de negocio: `protocolo.tiporece`

### Identidade

- Nome humano: Tipos de Receitas.
- O que representa: Tipos de Receitas
- Quando usar:
  - Preencher com perguntas/casos de negocio.
- Quando evitar:
  - Preencher com tabelas ou cenarios mais adequados.

### Grao e chaves

- Grao: Preencher.
- Entidade principal: Preencher.
- Chave de negocio:
  - `p08_tipo`
  - `p08_receit`
- Coluna temporal: Preencher.
- Candidatas a chave de negocio: p08_qtufir
- Candidatas a coluna temporal: Nenhuma inferida automaticamente.

### Colunas principais

- `p08_descr`: Descrição
- `p08_qtufir`: Quantidade de UFIR
- `p08_receit`: Receita
- `p08_tipo`: Tipo de Receita
- `p08_valor`: Valor

### Metricas atomicas

- `p08_qtufir`: Quantidade de UFIR
- `p08_valor`: Valor

### Dimensoes

- `p08_tipo`: Tipo de Receita

### Filtros de negocio

- Preencher filtros obrigatorios ou comuns.

### Regra de contagem

- Definir o que uma linha representa antes de contar.
- Se houver join que multiplique o grao, usar contagem distinta pela chave de negocio.

### Regra de agregacao

- Preencher como somar, contar ou agrupar sem mudar o grao.

### Relacionamentos importantes

- `p08_receit` -> `caixa.tabrec` (k02_codigo) [tiporece_receit_fk]

### Regras de negocio existentes no catalogo

- Preencher regras validadas por pessoa de negocio.

### Riscos de duplicidade

- Preencher onde joins podem multiplicar linhas ou valores.

### O que nao inferir

- Nao inferir regra de negocio apenas pelo nome tecnico.

### Cuidados

- Preencher ambiguidades, excecoes e limites conhecidos.
