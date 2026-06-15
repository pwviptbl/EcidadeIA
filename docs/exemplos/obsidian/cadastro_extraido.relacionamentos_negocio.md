---
titulo: Relacionamentos de negocio - Cadastro
dominio: cadastro
schema_principal: cadastro
fonte_json: cadastro_extraido.json
tags:
  - conhecimento-negocio
  - relacionamentos
  - curadoria
  - obsidian
---

# Relacionamentos de negocio - Cadastro

Este arquivo e um esqueleto para curadoria humana. Priorize validar caminhos que a FK isolada nao explica.

Quando uma receita estiver validada, copie ou adapte a secao para `knowledge/manual/<schema>/relacionamentos_negocio.md` e regenere o RAG.

## Receita de relacionamento: modelo

- Quando usar: Preencher.
- Origem de negocio: Preencher.
- Destino de negocio: Preencher.
- Tabelas no caminho:
  - Preencher.
- Caminho de negocio:
  - Preencher.
- Join logico:
  - Preencher.
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher.
- Cuidados:
  - Preencher.

## Receitas candidatas extraidas do catalogo

## Receita de relacionamento: arquivocdn_para_iptubase_via_arquivocdniptubase

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.arquivocdn` com `cadastro.iptubase` usando `cadastro.arquivocdniptubase`.
- Origem de negocio: `configuracoes.arquivocdn`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `configuracoes.arquivocdn`
  - `cadastro.arquivocdniptubase`
  - `cadastro.iptubase`
- Caminho de negocio:
  - arquivocdn -> arquivocdniptubase -> iptubase
- Join logico:
  - `cadastro.arquivocdniptubase.j151_arquivocdn = configuracoes.arquivocdn.db59_sequencial`
  - `cadastro.arquivocdniptubase.j151_iptubase = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_cgm_via_averba

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `protocolo.cgm` usando `cadastro.averba`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.averba`
  - `protocolo.cgm`
- Caminho de negocio:
  - iptubase -> averba -> cgm
- Join logico:
  - `cadastro.averba.j55_matric = cadastro.iptubase.j01_matric`
  - `cadastro.averba.j55_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_averbatipo_via_averbacao

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.averbatipo` usando `cadastro.averbacao`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.averbatipo`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.averbacao`
  - `cadastro.averbatipo`
- Caminho de negocio:
  - iptubase -> averbacao -> averbatipo
- Join logico:
  - `cadastro.averbacao.j75_matric = cadastro.iptubase.j01_matric`
  - `cadastro.averbacao.j75_tipo = cadastro.averbatipo.j93_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbacao_para_cgm_via_averbacgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbacao` com `protocolo.cgm` usando `cadastro.averbacgm`.
- Origem de negocio: `cadastro.averbacao`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.averbacao`
  - `cadastro.averbacgm`
  - `protocolo.cgm`
- Caminho de negocio:
  - averbacao -> averbacgm -> cgm
- Join logico:
  - `cadastro.averbacgm.j76_averbacao = cadastro.averbacao.j75_codigo`
  - `cadastro.averbacgm.j76_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbacao_para_tipocontribuinte_via_averbacgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbacao` com `cadastro.tipocontribuinte` usando `cadastro.averbacgm`.
- Origem de negocio: `cadastro.averbacao`.
- Destino de negocio: `cadastro.tipocontribuinte`.
- Tabelas no caminho:
  - `cadastro.averbacao`
  - `cadastro.averbacgm`
  - `cadastro.tipocontribuinte`
- Caminho de negocio:
  - averbacao -> averbacgm -> tipocontribuinte
- Join logico:
  - `cadastro.averbacgm.j76_averbacao = cadastro.averbacao.j75_codigo`
  - `cadastro.averbacgm.j76_tipo_contribuinte = cadastro.tipocontribuinte.j147_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: cgm_para_tipocontribuinte_via_averbacgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `protocolo.cgm` com `cadastro.tipocontribuinte` usando `cadastro.averbacgm`.
- Origem de negocio: `protocolo.cgm`.
- Destino de negocio: `cadastro.tipocontribuinte`.
- Tabelas no caminho:
  - `protocolo.cgm`
  - `cadastro.averbacgm`
  - `cadastro.tipocontribuinte`
- Caminho de negocio:
  - cgm -> averbacgm -> tipocontribuinte
- Join logico:
  - `cadastro.averbacgm.j76_numcgm = protocolo.cgm.z01_numcgm`
  - `cadastro.averbacgm.j76_tipo_contribuinte = cadastro.tipocontribuinte.j147_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbacao_para_cgm_via_averbacgmold

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbacao` com `protocolo.cgm` usando `cadastro.averbacgmold`.
- Origem de negocio: `cadastro.averbacao`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.averbacao`
  - `cadastro.averbacgmold`
  - `protocolo.cgm`
- Caminho de negocio:
  - averbacao -> averbacgmold -> cgm
- Join logico:
  - `cadastro.averbacgmold.j79_averbacao = cadastro.averbacao.j75_codigo`
  - `cadastro.averbacgmold.j79_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbaformalpartilha_para_cgm_via_averbaformalpartilhacgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbaformalpartilha` com `protocolo.cgm` usando `cadastro.averbaformalpartilhacgm`.
- Origem de negocio: `cadastro.averbaformalpartilha`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.averbaformalpartilha`
  - `cadastro.averbaformalpartilhacgm`
  - `protocolo.cgm`
- Caminho de negocio:
  - averbaformalpartilha -> averbaformalpartilhacgm -> cgm
- Join logico:
  - `cadastro.averbaformalpartilhacgm.j102_averbaformalpartilha = cadastro.averbaformalpartilha.j100_sequencial`
  - `cadastro.averbaformalpartilhacgm.j102_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbaguia_para_itbi_via_averbaguiaitbi

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbaguia` com `itbi.itbi` usando `cadastro.averbaguiaitbi`.
- Origem de negocio: `cadastro.averbaguia`.
- Destino de negocio: `itbi.itbi`.
- Tabelas no caminho:
  - `cadastro.averbaguia`
  - `cadastro.averbaguiaitbi`
  - `itbi.itbi`
- Caminho de negocio:
  - averbaguia -> averbaguiaitbi -> itbi
- Join logico:
  - `cadastro.averbaguiaitbi.j103_averbaguia = cadastro.averbaguia.j104_sequencial`
  - `cadastro.averbaguiaitbi.j103_itbi = itbi.itbi.it01_guia`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: averbacao_para_protprocesso_via_averbaprocesso

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.averbacao` com `protocolo.protprocesso` usando `cadastro.averbaprocesso`.
- Origem de negocio: `cadastro.averbacao`.
- Destino de negocio: `protocolo.protprocesso`.
- Tabelas no caminho:
  - `cadastro.averbacao`
  - `cadastro.averbaprocesso`
  - `protocolo.protprocesso`
- Caminho de negocio:
  - averbacao -> averbaprocesso -> protprocesso
- Join logico:
  - `cadastro.averbaprocesso.j77_averbacao = cadastro.averbacao.j75_codigo`
  - `cadastro.averbaprocesso.j77_codproc = protocolo.protprocesso.p58_codproc`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_caracter_via_caractercaracter

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.caracter` usando `cadastro.caractercaracter`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.caracter`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.caractercaracter`
  - `cadastro.caracter`
- Caminho de negocio:
  - caracter -> caractercaracter -> caracter
- Join logico:
  - `cadastro.caractercaracter.j138_caracterdestino = cadastro.caracter.j31_codigo`
  - `cadastro.caractercaracter.j138_caracterorigem = cadastro.caracter.j31_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_caracteristica_via_caractercaracteristica

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `configuracoes.caracteristica` usando `cadastro.caractercaracteristica`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `configuracoes.caracteristica`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.caractercaracteristica`
  - `configuracoes.caracteristica`
- Caminho de negocio:
  - caracter -> caractercaracteristica -> caracteristica
- Join logico:
  - `cadastro.caractercaracteristica.db143_caracter = cadastro.caracter.j31_codigo`
  - `cadastro.caractercaracteristica.db143_caracteristica = configuracoes.caracteristica.db140_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: bairro_para_caracter_via_carbairro

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.bairro` com `cadastro.caracter` usando `cadastro.carbairro`.
- Origem de negocio: `cadastro.bairro`.
- Destino de negocio: `cadastro.caracter`.
- Tabelas no caminho:
  - `cadastro.bairro`
  - `cadastro.carbairro`
  - `cadastro.caracter`
- Caminho de negocio:
  - bairro -> carbairro -> caracter
- Join logico:
  - `cadastro.carbairro.j114_bairro = cadastro.bairro.j13_codi`
  - `cadastro.carbairro.j114_caracter = cadastro.caracter.j31_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_caracter_via_carcaractervalor

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.caracter` usando `cadastro.carcaractervalor`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.caracter`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carcaractervalor`
  - `cadastro.caracter`
- Caminho de negocio:
  - caracter -> carcaractervalor -> caracter
- Join logico:
  - `cadastro.carcaractervalor.j119_caracteristica1 = cadastro.caracter.j31_codigo`
  - `cadastro.carcaractervalor.j119_caracteristica2 = cadastro.caracter.j31_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_face_via_carface

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.face` usando `cadastro.carface`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.face`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carface`
  - `cadastro.face`
- Caminho de negocio:
  - caracter -> carface -> face
- Join logico:
  - `cadastro.carface.j38_caract = cadastro.caracter.j31_codigo`
  - `cadastro.carface.j38_face = cadastro.face.j37_face`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_lote_via_carlote

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.lote` usando `cadastro.carlote`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.lote`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carlote`
  - `cadastro.lote`
- Caminho de negocio:
  - caracter -> carlote -> lote
- Join logico:
  - `cadastro.carlote.j35_caract = cadastro.caracter.j31_codigo`
  - `cadastro.carlote.j35_idbql = cadastro.lote.j34_idbql`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_cargrup_via_carpadrao

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.cargrup` usando `cadastro.carpadrao`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.cargrup`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carpadrao`
  - `cadastro.cargrup`
- Caminho de negocio:
  - caracter -> carpadrao -> cargrup
- Join logico:
  - `cadastro.carpadrao.j33_codcaracter = cadastro.caracter.j31_codigo`
  - `cadastro.carpadrao.j33_codgrupo = cadastro.cargrup.j32_grupo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_zonas_via_carzonafator

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.zonas` usando `cadastro.carzonafator`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.zonas`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carzonafator`
  - `cadastro.zonas`
- Caminho de negocio:
  - caracter -> carzonafator -> zonas
- Join logico:
  - `cadastro.carzonafator.j96_caracter = cadastro.caracter.j31_codigo`
  - `cadastro.carzonafator.j96_zona = cadastro.zonas.j50_zona`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_zonas_via_carzonavalor

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.zonas` usando `cadastro.carzonavalor`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.zonas`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.carzonavalor`
  - `cadastro.zonas`
- Caminho de negocio:
  - caracter -> carzonavalor -> zonas
- Join logico:
  - `cadastro.carzonavalor.j72_caract = cadastro.caracter.j31_codigo`
  - `cadastro.carzonavalor.j72_zona = cadastro.zonas.j50_zona`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptuconstr_para_db_usuarios_via_certidaoexistencia

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptuconstr` com `configuracoes.db_usuarios` usando `cadastro.certidaoexistencia`.
- Origem de negocio: `cadastro.iptuconstr`.
- Destino de negocio: `configuracoes.db_usuarios`.
- Tabelas no caminho:
  - `cadastro.iptuconstr`
  - `cadastro.certidaoexistencia`
  - `configuracoes.db_usuarios`
- Caminho de negocio:
  - iptuconstr -> certidaoexistencia -> db_usuarios
- Join logico:
  - `cadastro.certidaoexistencia.j133_matric = cadastro.iptuconstr.j39_matric` e `cadastro.certidaoexistencia.j133_matric = cadastro.iptuconstr.j39_idcons` e `cadastro.certidaoexistencia.j133_iptuconstr = cadastro.iptuconstr.j39_matric` e `cadastro.certidaoexistencia.j133_iptuconstr = cadastro.iptuconstr.j39_idcons`
  - `cadastro.certidaoexistencia.j133_db_usuarios = configuracoes.db_usuarios.id_usuario`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: certidaoexistencia_para_protprocesso_via_certidaoexistenciaprotprocesso

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.certidaoexistencia` com `protocolo.protprocesso` usando `cadastro.certidaoexistenciaprotprocesso`.
- Origem de negocio: `cadastro.certidaoexistencia`.
- Destino de negocio: `protocolo.protprocesso`.
- Tabelas no caminho:
  - `cadastro.certidaoexistencia`
  - `cadastro.certidaoexistenciaprotprocesso`
  - `protocolo.protprocesso`
- Caminho de negocio:
  - certidaoexistencia -> certidaoexistenciaprotprocesso -> protprocesso
- Join logico:
  - `cadastro.certidaoexistenciaprotprocesso.j134_certidaoexistencia = cadastro.certidaoexistencia.j133_sequencial`
  - `cadastro.certidaoexistenciaprotprocesso.j134_protprocesso = protocolo.protprocesso.p58_codproc`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_usuarios_para_issbase_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_usuarios` com `issqn.issbase` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `configuracoes.db_usuarios`.
- Destino de negocio: `issqn.issbase`.
- Tabelas no caminho:
  - `configuracoes.db_usuarios`
  - `cadastro.certidoesdiversas`
  - `issqn.issbase`
- Caminho de negocio:
  - db_usuarios -> certidoesdiversas -> issbase
- Join logico:
  - `cadastro.certidoesdiversas.j183_id_usuario = configuracoes.db_usuarios.id_usuario`
  - `cadastro.certidoesdiversas.j183_inscr_iss = issqn.issbase.q02_inscr`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_usuarios_para_iptubase_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_usuarios` com `cadastro.iptubase` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `configuracoes.db_usuarios`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `configuracoes.db_usuarios`
  - `cadastro.certidoesdiversas`
  - `cadastro.iptubase`
- Caminho de negocio:
  - db_usuarios -> certidoesdiversas -> iptubase
- Join logico:
  - `cadastro.certidoesdiversas.j183_id_usuario = configuracoes.db_usuarios.id_usuario`
  - `cadastro.certidoesdiversas.j183_matric_iptu = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_usuarios_para_cgm_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_usuarios` com `protocolo.cgm` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `configuracoes.db_usuarios`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `configuracoes.db_usuarios`
  - `cadastro.certidoesdiversas`
  - `protocolo.cgm`
- Caminho de negocio:
  - db_usuarios -> certidoesdiversas -> cgm
- Join logico:
  - `cadastro.certidoesdiversas.j183_id_usuario = configuracoes.db_usuarios.id_usuario`
  - `cadastro.certidoesdiversas.j183_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: issbase_para_iptubase_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `issqn.issbase` com `cadastro.iptubase` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `issqn.issbase`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `issqn.issbase`
  - `cadastro.certidoesdiversas`
  - `cadastro.iptubase`
- Caminho de negocio:
  - issbase -> certidoesdiversas -> iptubase
- Join logico:
  - `cadastro.certidoesdiversas.j183_inscr_iss = issqn.issbase.q02_inscr`
  - `cadastro.certidoesdiversas.j183_matric_iptu = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: issbase_para_cgm_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `issqn.issbase` com `protocolo.cgm` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `issqn.issbase`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `issqn.issbase`
  - `cadastro.certidoesdiversas`
  - `protocolo.cgm`
- Caminho de negocio:
  - issbase -> certidoesdiversas -> cgm
- Join logico:
  - `cadastro.certidoesdiversas.j183_inscr_iss = issqn.issbase.q02_inscr`
  - `cadastro.certidoesdiversas.j183_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_cgm_via_certidoesdiversas

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `protocolo.cgm` usando `cadastro.certidoesdiversas`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.certidoesdiversas`
  - `protocolo.cgm`
- Caminho de negocio:
  - iptubase -> certidoesdiversas -> cgm
- Join logico:
  - `cadastro.certidoesdiversas.j183_matric_iptu = cadastro.iptubase.j01_matric`
  - `cadastro.certidoesdiversas.j183_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: certidoesdiversas_para_protprocesso_via_certidoesdiversasprotprocesso

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.certidoesdiversas` com `protocolo.protprocesso` usando `cadastro.certidoesdiversasprotprocesso`.
- Origem de negocio: `cadastro.certidoesdiversas`.
- Destino de negocio: `protocolo.protprocesso`.
- Tabelas no caminho:
  - `cadastro.certidoesdiversas`
  - `cadastro.certidoesdiversasprotprocesso`
  - `protocolo.protprocesso`
- Caminho de negocio:
  - certidoesdiversas -> certidoesdiversasprotprocesso -> protprocesso
- Join logico:
  - `cadastro.certidoesdiversasprotprocesso.j184_id_certidoesdiversas = cadastro.certidoesdiversas.j183_id`
  - `cadastro.certidoesdiversasprotprocesso.j184_protprocesso = protocolo.protprocesso.p58_codproc`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: inflan_para_iptucalh_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `inflatores.inflan` com `cadastro.iptucalh` usando `cadastro.cfiptu`.
- Origem de negocio: `inflatores.inflan`.
- Destino de negocio: `cadastro.iptucalh`.
- Tabelas no caminho:
  - `inflatores.inflan`
  - `cadastro.cfiptu`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - inflan -> cfiptu -> iptucalh
- Join logico:
  - `cadastro.cfiptu.j18_infla = inflatores.inflan.i01_codigo`
  - `cadastro.cfiptu.j18_iptuhistisen = cadastro.iptucalh.j17_codhis`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: inflan_para_db_documentotemplate_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `inflatores.inflan` com `configuracoes.db_documentotemplate` usando `cadastro.cfiptu`.
- Origem de negocio: `inflatores.inflan`.
- Destino de negocio: `configuracoes.db_documentotemplate`.
- Tabelas no caminho:
  - `inflatores.inflan`
  - `cadastro.cfiptu`
  - `configuracoes.db_documentotemplate`
- Caminho de negocio:
  - inflan -> cfiptu -> db_documentotemplate
- Join logico:
  - `cadastro.cfiptu.j18_infla = inflatores.inflan.i01_codigo`
  - `cadastro.cfiptu.j18_templatecertidaoexitencia = configuracoes.db_documentotemplate.db82_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: inflan_para_tabrec_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `inflatores.inflan` com `caixa.tabrec` usando `cadastro.cfiptu`.
- Origem de negocio: `inflatores.inflan`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `inflatores.inflan`
  - `cadastro.cfiptu`
  - `caixa.tabrec`
- Caminho de negocio:
  - inflan -> cfiptu -> tabrec
- Join logico:
  - `cadastro.cfiptu.j18_infla = inflatores.inflan.i01_codigo`
  - `cadastro.cfiptu.j18_receitacreditorecalculo = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: inflan_para_arretipo_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `inflatores.inflan` com `caixa.arretipo` usando `cadastro.cfiptu`.
- Origem de negocio: `inflatores.inflan`.
- Destino de negocio: `caixa.arretipo`.
- Tabelas no caminho:
  - `inflatores.inflan`
  - `cadastro.cfiptu`
  - `caixa.arretipo`
- Caminho de negocio:
  - inflan -> cfiptu -> arretipo
- Join logico:
  - `cadastro.cfiptu.j18_infla = inflatores.inflan.i01_codigo`
  - `cadastro.cfiptu.j18_tipodebitorecalculo = caixa.arretipo.k00_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: inflan_para_tipoisen_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `inflatores.inflan` com `cadastro.tipoisen` usando `cadastro.cfiptu`.
- Origem de negocio: `inflatores.inflan`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `inflatores.inflan`
  - `cadastro.cfiptu`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - inflan -> cfiptu -> tipoisen
- Join logico:
  - `cadastro.cfiptu.j18_infla = inflatores.inflan.i01_codigo`
  - `cadastro.cfiptu.j18_tipoisen = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_db_documentotemplate_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `configuracoes.db_documentotemplate` usando `cadastro.cfiptu`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `configuracoes.db_documentotemplate`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.cfiptu`
  - `configuracoes.db_documentotemplate`
- Caminho de negocio:
  - iptucalh -> cfiptu -> db_documentotemplate
- Join logico:
  - `cadastro.cfiptu.j18_iptuhistisen = cadastro.iptucalh.j17_codhis`
  - `cadastro.cfiptu.j18_templatecertidaoexitencia = configuracoes.db_documentotemplate.db82_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_tabrec_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `caixa.tabrec` usando `cadastro.cfiptu`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.cfiptu`
  - `caixa.tabrec`
- Caminho de negocio:
  - iptucalh -> cfiptu -> tabrec
- Join logico:
  - `cadastro.cfiptu.j18_iptuhistisen = cadastro.iptucalh.j17_codhis`
  - `cadastro.cfiptu.j18_receitacreditorecalculo = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_arretipo_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `caixa.arretipo` usando `cadastro.cfiptu`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `caixa.arretipo`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.cfiptu`
  - `caixa.arretipo`
- Caminho de negocio:
  - iptucalh -> cfiptu -> arretipo
- Join logico:
  - `cadastro.cfiptu.j18_iptuhistisen = cadastro.iptucalh.j17_codhis`
  - `cadastro.cfiptu.j18_tipodebitorecalculo = caixa.arretipo.k00_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_tipoisen_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `cadastro.tipoisen` usando `cadastro.cfiptu`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.cfiptu`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - iptucalh -> cfiptu -> tipoisen
- Join logico:
  - `cadastro.cfiptu.j18_iptuhistisen = cadastro.iptucalh.j17_codhis`
  - `cadastro.cfiptu.j18_tipoisen = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_documentotemplate_para_tabrec_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_documentotemplate` com `caixa.tabrec` usando `cadastro.cfiptu`.
- Origem de negocio: `configuracoes.db_documentotemplate`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `configuracoes.db_documentotemplate`
  - `cadastro.cfiptu`
  - `caixa.tabrec`
- Caminho de negocio:
  - db_documentotemplate -> cfiptu -> tabrec
- Join logico:
  - `cadastro.cfiptu.j18_templatecertidaoexitencia = configuracoes.db_documentotemplate.db82_sequencial`
  - `cadastro.cfiptu.j18_receitacreditorecalculo = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_documentotemplate_para_arretipo_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_documentotemplate` com `caixa.arretipo` usando `cadastro.cfiptu`.
- Origem de negocio: `configuracoes.db_documentotemplate`.
- Destino de negocio: `caixa.arretipo`.
- Tabelas no caminho:
  - `configuracoes.db_documentotemplate`
  - `cadastro.cfiptu`
  - `caixa.arretipo`
- Caminho de negocio:
  - db_documentotemplate -> cfiptu -> arretipo
- Join logico:
  - `cadastro.cfiptu.j18_templatecertidaoexitencia = configuracoes.db_documentotemplate.db82_sequencial`
  - `cadastro.cfiptu.j18_tipodebitorecalculo = caixa.arretipo.k00_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: db_documentotemplate_para_tipoisen_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `configuracoes.db_documentotemplate` com `cadastro.tipoisen` usando `cadastro.cfiptu`.
- Origem de negocio: `configuracoes.db_documentotemplate`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `configuracoes.db_documentotemplate`
  - `cadastro.cfiptu`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - db_documentotemplate -> cfiptu -> tipoisen
- Join logico:
  - `cadastro.cfiptu.j18_templatecertidaoexitencia = configuracoes.db_documentotemplate.db82_sequencial`
  - `cadastro.cfiptu.j18_tipoisen = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: tabrec_para_arretipo_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `caixa.tabrec` com `caixa.arretipo` usando `cadastro.cfiptu`.
- Origem de negocio: `caixa.tabrec`.
- Destino de negocio: `caixa.arretipo`.
- Tabelas no caminho:
  - `caixa.tabrec`
  - `cadastro.cfiptu`
  - `caixa.arretipo`
- Caminho de negocio:
  - tabrec -> cfiptu -> arretipo
- Join logico:
  - `cadastro.cfiptu.j18_receitacreditorecalculo = caixa.tabrec.k02_codigo`
  - `cadastro.cfiptu.j18_tipodebitorecalculo = caixa.arretipo.k00_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: tabrec_para_tipoisen_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `caixa.tabrec` com `cadastro.tipoisen` usando `cadastro.cfiptu`.
- Origem de negocio: `caixa.tabrec`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `caixa.tabrec`
  - `cadastro.cfiptu`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - tabrec -> cfiptu -> tipoisen
- Join logico:
  - `cadastro.cfiptu.j18_receitacreditorecalculo = caixa.tabrec.k02_codigo`
  - `cadastro.cfiptu.j18_tipoisen = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: arretipo_para_tipoisen_via_cfiptu

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `caixa.arretipo` com `cadastro.tipoisen` usando `cadastro.cfiptu`.
- Origem de negocio: `caixa.arretipo`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `caixa.arretipo`
  - `cadastro.cfiptu`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - arretipo -> cfiptu -> tipoisen
- Join logico:
  - `cadastro.cfiptu.j18_tipodebitorecalculo = caixa.arretipo.k00_tipo`
  - `cadastro.cfiptu.j18_tipoisen = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: condominio_para_cgm_via_condominiocgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.condominio` com `protocolo.cgm` usando `cadastro.condominiocgm`.
- Origem de negocio: `cadastro.condominio`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.condominio`
  - `cadastro.condominiocgm`
  - `protocolo.cgm`
- Caminho de negocio:
  - condominio -> condominiocgm -> cgm
- Join logico:
  - `cadastro.condominiocgm.j106_condominio = cadastro.condominio.j107_sequencial`
  - `cadastro.condominiocgm.j106_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: condominio_para_protprocesso_via_condominioprocesso

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.condominio` com `protocolo.protprocesso` usando `cadastro.condominioprocesso`.
- Origem de negocio: `cadastro.condominio`.
- Destino de negocio: `protocolo.protprocesso`.
- Tabelas no caminho:
  - `cadastro.condominio`
  - `cadastro.condominioprocesso`
  - `protocolo.protprocesso`
- Caminho de negocio:
  - condominio -> condominioprocesso -> protprocesso
- Join logico:
  - `cadastro.condominioprocesso.j179_condominio = cadastro.condominio.j107_sequencial`
  - `cadastro.condominioprocesso.j179_processo = protocolo.protprocesso.p58_codproc`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: ruas_para_iptubase_via_constrescr

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.ruas` com `cadastro.iptubase` usando `cadastro.constrescr`.
- Origem de negocio: `cadastro.ruas`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.ruas`
  - `cadastro.constrescr`
  - `cadastro.iptubase`
- Caminho de negocio:
  - ruas -> constrescr -> iptubase
- Join logico:
  - `cadastro.constrescr.j52_codigo = cadastro.ruas.j14_codigo`
  - `cadastro.constrescr.j52_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: setorregimovel_para_db_usuarios_via_doi

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.setorregimovel` com `configuracoes.db_usuarios` usando `cadastro.doi`.
- Origem de negocio: `cadastro.setorregimovel`.
- Destino de negocio: `configuracoes.db_usuarios`.
- Tabelas no caminho:
  - `cadastro.setorregimovel`
  - `cadastro.doi`
  - `configuracoes.db_usuarios`
- Caminho de negocio:
  - setorregimovel -> doi -> db_usuarios
- Join logico:
  - `cadastro.doi.j180_id_registro_imoveis = cadastro.setorregimovel.j69_sequencial`
  - `cadastro.doi.j180_id_usuario = configuracoes.db_usuarios.id_usuario`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: doi_para_cgm_via_doi_importacao

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.doi` com `protocolo.cgm` usando `cadastro.doi_importacao`.
- Origem de negocio: `cadastro.doi`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.doi`
  - `cadastro.doi_importacao`
  - `protocolo.cgm`
- Caminho de negocio:
  - doi -> doi_importacao -> cgm
- Join logico:
  - `cadastro.doi_importacao.j181_id_doi = cadastro.doi.j180_id`
  - `cadastro.doi_importacao.j181_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: ruas_para_setor_via_face

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.ruas` com `cadastro.setor` usando `cadastro.face`.
- Origem de negocio: `cadastro.ruas`.
- Destino de negocio: `cadastro.setor`.
- Tabelas no caminho:
  - `cadastro.ruas`
  - `cadastro.face`
  - `cadastro.setor`
- Caminho de negocio:
  - ruas -> face -> setor
- Join logico:
  - `cadastro.face.j37_codigo = cadastro.ruas.j14_codigo`
  - `cadastro.face.j37_setor = cadastro.setor.j30_codi`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_cgm_via_imobil

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `protocolo.cgm` usando `cadastro.imobil`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.imobil`
  - `protocolo.cgm`
- Caminho de negocio:
  - iptubase -> imobil -> cgm
- Join logico:
  - `cadastro.imobil.j44_matric = cadastro.iptubase.j01_matric`
  - `cadastro.imobil.j44_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_db_usuarios_via_iptubaixa

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `configuracoes.db_usuarios` usando `cadastro.iptubaixa`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `configuracoes.db_usuarios`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptubaixa`
  - `configuracoes.db_usuarios`
- Caminho de negocio:
  - iptubase -> iptubaixa -> db_usuarios
- Join logico:
  - `cadastro.iptubaixa.j02_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptubaixa.j02_usuario = configuracoes.db_usuarios.id_usuario`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: protprocesso_para_iptubaixa_via_iptubaixaproc

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `protocolo.protprocesso` com `cadastro.iptubaixa` usando `cadastro.iptubaixaproc`.
- Origem de negocio: `protocolo.protprocesso`.
- Destino de negocio: `cadastro.iptubaixa`.
- Tabelas no caminho:
  - `protocolo.protprocesso`
  - `cadastro.iptubaixaproc`
  - `cadastro.iptubaixa`
- Caminho de negocio:
  - protprocesso -> iptubaixaproc -> iptubaixa
- Join logico:
  - `cadastro.iptubaixaproc.j03_codproc = protocolo.protprocesso.p58_codproc`
  - `cadastro.iptubaixaproc.j03_matric = cadastro.iptubaixa.j02_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: lote_para_cgm_via_iptubase

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.lote` com `protocolo.cgm` usando `cadastro.iptubase`.
- Origem de negocio: `cadastro.lote`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.lote`
  - `cadastro.iptubase`
  - `protocolo.cgm`
- Caminho de negocio:
  - lote -> iptubase -> cgm
- Join logico:
  - `cadastro.iptubase.j01_idbql = cadastro.lote.j34_idbql`
  - `cadastro.iptubase.j01_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: lote_para_tipocontribuinte_via_iptubase

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.lote` com `cadastro.tipocontribuinte` usando `cadastro.iptubase`.
- Origem de negocio: `cadastro.lote`.
- Destino de negocio: `cadastro.tipocontribuinte`.
- Tabelas no caminho:
  - `cadastro.lote`
  - `cadastro.iptubase`
  - `cadastro.tipocontribuinte`
- Caminho de negocio:
  - lote -> iptubase -> tipocontribuinte
- Join logico:
  - `cadastro.iptubase.j01_idbql = cadastro.lote.j34_idbql`
  - `cadastro.iptubase.j01_tipo_contribuinte = cadastro.tipocontribuinte.j147_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: cgm_para_tipocontribuinte_via_iptubase

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `protocolo.cgm` com `cadastro.tipocontribuinte` usando `cadastro.iptubase`.
- Origem de negocio: `protocolo.cgm`.
- Destino de negocio: `cadastro.tipocontribuinte`.
- Tabelas no caminho:
  - `protocolo.cgm`
  - `cadastro.iptubase`
  - `cadastro.tipocontribuinte`
- Caminho de negocio:
  - cgm -> iptubase -> tipocontribuinte
- Join logico:
  - `cadastro.iptubase.j01_numcgm = protocolo.cgm.z01_numcgm`
  - `cadastro.iptubase.j01_tipo_contribuinte = cadastro.tipocontribuinte.j147_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: condominio_para_iptubase_via_iptubasecondominio

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.condominio` com `cadastro.iptubase` usando `cadastro.iptubasecondominio`.
- Origem de negocio: `cadastro.condominio`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.condominio`
  - `cadastro.iptubasecondominio`
  - `cadastro.iptubase`
- Caminho de negocio:
  - condominio -> iptubasecondominio -> iptubase
- Join logico:
  - `cadastro.iptubasecondominio.j108_condominio = cadastro.condominio.j107_sequencial`
  - `cadastro.iptubasecondominio.j108_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_predio_via_iptubasepredio

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.predio` usando `cadastro.iptubasepredio`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.predio`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptubasepredio`
  - `cadastro.predio`
- Caminho de negocio:
  - iptubase -> iptubasepredio -> predio
- Join logico:
  - `cadastro.iptubasepredio.j109_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptubasepredio.j109_predio = cadastro.predio.j111_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_setorregimovel_via_iptubaseregimovel

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.setorregimovel` usando `cadastro.iptubaseregimovel`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.setorregimovel`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptubaseregimovel`
  - `cadastro.setorregimovel`
- Caminho de negocio:
  - iptubase -> iptubaseregimovel -> setorregimovel
- Join logico:
  - `cadastro.iptubaseregimovel.j04_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptubaseregimovel.j04_setorregimovel = cadastro.setorregimovel.j69_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucadtaxa_para_iptucalh_via_iptucadtaxaexe

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucadtaxa` com `cadastro.iptucalh` usando `cadastro.iptucadtaxaexe`.
- Origem de negocio: `cadastro.iptucadtaxa`.
- Destino de negocio: `cadastro.iptucalh`.
- Tabelas no caminho:
  - `cadastro.iptucadtaxa`
  - `cadastro.iptucadtaxaexe`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - iptucadtaxa -> iptucadtaxaexe -> iptucalh
- Join logico:
  - `cadastro.iptucadtaxaexe.j08_iptucadtaxa = cadastro.iptucadtaxa.j07_iptucadtaxa`
  - `cadastro.iptucadtaxaexe.j08_iptucalh = cadastro.iptucalh.j17_codhis`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucadtaxa_para_tabrec_via_iptucadtaxaexe

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucadtaxa` com `caixa.tabrec` usando `cadastro.iptucadtaxaexe`.
- Origem de negocio: `cadastro.iptucadtaxa`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `cadastro.iptucadtaxa`
  - `cadastro.iptucadtaxaexe`
  - `caixa.tabrec`
- Caminho de negocio:
  - iptucadtaxa -> iptucadtaxaexe -> tabrec
- Join logico:
  - `cadastro.iptucadtaxaexe.j08_iptucadtaxa = cadastro.iptucadtaxa.j07_iptucadtaxa`
  - `cadastro.iptucadtaxaexe.j08_tabrec = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_tabrec_via_iptucadtaxaexe

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `caixa.tabrec` usando `cadastro.iptucadtaxaexe`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.iptucadtaxaexe`
  - `caixa.tabrec`
- Caminho de negocio:
  - iptucalh -> iptucadtaxaexe -> tabrec
- Join logico:
  - `cadastro.iptucadtaxaexe.j08_iptucalh = cadastro.iptucalh.j17_codhis`
  - `cadastro.iptucadtaxaexe.j08_tabrec = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucadzonaentrega_para_ruas_via_iptucadzonaentregaend

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucadzonaentrega` com `cadastro.ruas` usando `cadastro.iptucadzonaentregaend`.
- Origem de negocio: `cadastro.iptucadzonaentrega`.
- Destino de negocio: `cadastro.ruas`.
- Tabelas no caminho:
  - `cadastro.iptucadzonaentrega`
  - `cadastro.iptucadzonaentregaend`
  - `cadastro.ruas`
- Caminho de negocio:
  - iptucadzonaentrega -> iptucadzonaentregaend -> ruas
- Join logico:
  - `cadastro.iptucadzonaentregaend.j87_iptucadzonaentrega = cadastro.iptucadzonaentrega.j85_codigo`
  - `cadastro.iptucadzonaentregaend.j87_lograd = cadastro.ruas.j14_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: tabrec_para_tabrec_via_iptucalcconfrec

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `caixa.tabrec` com `caixa.tabrec` usando `cadastro.iptucalcconfrec`.
- Origem de negocio: `caixa.tabrec`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `caixa.tabrec`
  - `cadastro.iptucalcconfrec`
  - `caixa.tabrec`
- Caminho de negocio:
  - tabrec -> iptucalcconfrec -> tabrec
- Join logico:
  - `cadastro.iptucalcconfrec.j23_recdst = caixa.tabrec.k02_codigo`
  - `cadastro.iptucalcconfrec.j23_recorg = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalclog_para_iptubase_via_iptucalclogmat

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalclog` com `cadastro.iptubase` usando `cadastro.iptucalclogmat`.
- Origem de negocio: `cadastro.iptucalclog`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.iptucalclog`
  - `cadastro.iptucalclogmat`
  - `cadastro.iptubase`
- Caminho de negocio:
  - iptucalclog -> iptucalclogmat -> iptubase
- Join logico:
  - `cadastro.iptucalclogmat.j28_codigo = cadastro.iptucalclog.j27_codigo`
  - `cadastro.iptucalclogmat.j28_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalclog_para_iptucadlogcalc_via_iptucalclogmat

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalclog` com `cadastro.iptucadlogcalc` usando `cadastro.iptucalclogmat`.
- Origem de negocio: `cadastro.iptucalclog`.
- Destino de negocio: `cadastro.iptucadlogcalc`.
- Tabelas no caminho:
  - `cadastro.iptucalclog`
  - `cadastro.iptucalclogmat`
  - `cadastro.iptucadlogcalc`
- Caminho de negocio:
  - iptucalclog -> iptucalclogmat -> iptucadlogcalc
- Join logico:
  - `cadastro.iptucalclogmat.j28_codigo = cadastro.iptucalclog.j27_codigo`
  - `cadastro.iptucalclogmat.j28_tipologcalc = cadastro.iptucadlogcalc.j62_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_iptucadlogcalc_via_iptucalclogmat

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.iptucadlogcalc` usando `cadastro.iptucalclogmat`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.iptucadlogcalc`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptucalclogmat`
  - `cadastro.iptucadlogcalc`
- Caminho de negocio:
  - iptubase -> iptucalclogmat -> iptucadlogcalc
- Join logico:
  - `cadastro.iptucalclogmat.j28_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptucalclogmat.j28_tipologcalc = cadastro.iptucadlogcalc.j62_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalcpadrao_para_iptuconstr_via_iptucalcpadraoconstr

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalcpadrao` com `cadastro.iptuconstr` usando `cadastro.iptucalcpadraoconstr`.
- Origem de negocio: `cadastro.iptucalcpadrao`.
- Destino de negocio: `cadastro.iptuconstr`.
- Tabelas no caminho:
  - `cadastro.iptucalcpadrao`
  - `cadastro.iptucalcpadraoconstr`
  - `cadastro.iptuconstr`
- Caminho de negocio:
  - iptucalcpadrao -> iptucalcpadraoconstr -> iptuconstr
- Join logico:
  - `cadastro.iptucalcpadraoconstr.j11_iptucalcpadrao = cadastro.iptucalcpadrao.j10_sequencial`
  - `cadastro.iptucalcpadraoconstr.j11_matric = cadastro.iptuconstr.j39_matric` e `cadastro.iptucalcpadraoconstr.j11_matric = cadastro.iptuconstr.j39_idcons` e `cadastro.iptucalcpadraoconstr.j11_idcons = cadastro.iptuconstr.j39_idcons` e `cadastro.iptucalcpadraoconstr.j11_idcons = cadastro.iptuconstr.j39_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalcpadrao_para_db_usuarios_via_iptucalcpadraolog

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalcpadrao` com `configuracoes.db_usuarios` usando `cadastro.iptucalcpadraolog`.
- Origem de negocio: `cadastro.iptucalcpadrao`.
- Destino de negocio: `configuracoes.db_usuarios`.
- Tabelas no caminho:
  - `cadastro.iptucalcpadrao`
  - `cadastro.iptucalcpadraolog`
  - `configuracoes.db_usuarios`
- Caminho de negocio:
  - iptucalcpadrao -> iptucalcpadraolog -> db_usuarios
- Join logico:
  - `cadastro.iptucalcpadraolog.j19_iptucalcpadrao = cadastro.iptucalcpadrao.j10_sequencial`
  - `cadastro.iptucalcpadraolog.j19_usuario = configuracoes.db_usuarios.id_usuario`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalc_para_iptucalcpadrao_via_iptucalcpadraoorigem

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalc` com `cadastro.iptucalcpadrao` usando `cadastro.iptucalcpadraoorigem`.
- Origem de negocio: `cadastro.iptucalc`.
- Destino de negocio: `cadastro.iptucalcpadrao`.
- Tabelas no caminho:
  - `cadastro.iptucalc`
  - `cadastro.iptucalcpadraoorigem`
  - `cadastro.iptucalcpadrao`
- Caminho de negocio:
  - iptucalc -> iptucalcpadraoorigem -> iptucalcpadrao
- Join logico:
  - `cadastro.iptucalcpadraoorigem.j27_anousu = cadastro.iptucalc.j23_matric` e `cadastro.iptucalcpadraoorigem.j27_anousu = cadastro.iptucalc.j23_anousu` e `cadastro.iptucalcpadraoorigem.j27_matric = cadastro.iptucalc.j23_anousu` e `cadastro.iptucalcpadraoorigem.j27_matric = cadastro.iptucalc.j23_matric`
  - `cadastro.iptucalcpadraoorigem.j27_iptucalcpadrao = cadastro.iptucalcpadrao.j10_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_iptucalh_via_iptucalhconf

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `cadastro.iptucalh` usando `cadastro.iptucalhconf`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `cadastro.iptucalh`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.iptucalhconf`
  - `cadastro.iptucalh`
- Caminho de negocio:
  - iptucalh -> iptucalhconf -> iptucalh
- Join logico:
  - `cadastro.iptucalhconf.j89_codhis = cadastro.iptucalh.j17_codhis`
  - `cadastro.iptucalhconf.j89_codhispai = cadastro.iptucalh.j17_codhis`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_iptubase_via_iptucalv

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `cadastro.iptubase` usando `cadastro.iptucalv`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.iptucalv`
  - `cadastro.iptubase`
- Caminho de negocio:
  - iptucalh -> iptucalv -> iptubase
- Join logico:
  - `cadastro.iptucalv.j21_codhis = cadastro.iptucalh.j17_codhis`
  - `cadastro.iptucalv.j21_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucalh_para_tabrec_via_iptucalv

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucalh` com `caixa.tabrec` usando `cadastro.iptucalv`.
- Origem de negocio: `cadastro.iptucalh`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `cadastro.iptucalh`
  - `cadastro.iptucalv`
  - `caixa.tabrec`
- Caminho de negocio:
  - iptucalh -> iptucalv -> tabrec
- Join logico:
  - `cadastro.iptucalv.j21_codhis = cadastro.iptucalh.j17_codhis`
  - `cadastro.iptucalv.j21_receit = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_tabrec_via_iptucalv

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `caixa.tabrec` usando `cadastro.iptucalv`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `caixa.tabrec`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptucalv`
  - `caixa.tabrec`
- Caminho de negocio:
  - iptubase -> iptucalv -> tabrec
- Join logico:
  - `cadastro.iptucalv.j21_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptucalv.j21_receit = caixa.tabrec.k02_codigo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: ruas_para_iptubase_via_iptuconstr

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.ruas` com `cadastro.iptubase` usando `cadastro.iptuconstr`.
- Origem de negocio: `cadastro.ruas`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.ruas`
  - `cadastro.iptuconstr`
  - `cadastro.iptubase`
- Caminho de negocio:
  - ruas -> iptuconstr -> iptubase
- Join logico:
  - `cadastro.iptuconstr.j39_codigo = cadastro.ruas.j14_codigo`
  - `cadastro.iptuconstr.j39_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptuconstr_para_obrasconstr_via_iptuconstrobrasconstr

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptuconstr` com `projetos.obrasconstr` usando `cadastro.iptuconstrobrasconstr`.
- Origem de negocio: `cadastro.iptuconstr`.
- Destino de negocio: `projetos.obrasconstr`.
- Tabelas no caminho:
  - `cadastro.iptuconstr`
  - `cadastro.iptuconstrobrasconstr`
  - `projetos.obrasconstr`
- Caminho de negocio:
  - iptuconstr -> iptuconstrobrasconstr -> obrasconstr
- Join logico:
  - `cadastro.iptuconstrobrasconstr.j132_matric = cadastro.iptuconstr.j39_idcons` e `cadastro.iptuconstrobrasconstr.j132_matric = cadastro.iptuconstr.j39_matric` e `cadastro.iptuconstrobrasconstr.j132_idconstr = cadastro.iptuconstr.j39_matric` e `cadastro.iptuconstrobrasconstr.j132_idconstr = cadastro.iptuconstr.j39_idcons`
  - `cadastro.iptuconstrobrasconstr.j132_obrasconstr = projetos.obrasconstr.ob08_codconstr`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_tipoisen_via_iptuisen

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.tipoisen` usando `cadastro.iptuisen`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.tipoisen`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptuisen`
  - `cadastro.tipoisen`
- Caminho de negocio:
  - iptubase -> iptuisen -> tipoisen
- Join logico:
  - `cadastro.iptuisen.j46_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptuisen.j46_tipo = cadastro.tipoisen.j45_tipo`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptucadzonaentrega_para_iptubase_via_iptumatzonaentrega

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptucadzonaentrega` com `cadastro.iptubase` usando `cadastro.iptumatzonaentrega`.
- Origem de negocio: `cadastro.iptucadzonaentrega`.
- Destino de negocio: `cadastro.iptubase`.
- Tabelas no caminho:
  - `cadastro.iptucadzonaentrega`
  - `cadastro.iptumatzonaentrega`
  - `cadastro.iptubase`
- Caminho de negocio:
  - iptucadzonaentrega -> iptumatzonaentrega -> iptubase
- Join logico:
  - `cadastro.iptumatzonaentrega.j86_iptucadzonaentrega = cadastro.iptucadzonaentrega.j85_codigo`
  - `cadastro.iptumatzonaentrega.j86_matric = cadastro.iptubase.j01_matric`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptunaogeracarne_para_cgm_via_iptunaogeracarnecgm

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptunaogeracarne` com `protocolo.cgm` usando `cadastro.iptunaogeracarnecgm`.
- Origem de negocio: `cadastro.iptunaogeracarne`.
- Destino de negocio: `protocolo.cgm`.
- Tabelas no caminho:
  - `cadastro.iptunaogeracarne`
  - `cadastro.iptunaogeracarnecgm`
  - `protocolo.cgm`
- Caminho de negocio:
  - iptunaogeracarne -> iptunaogeracarnecgm -> cgm
- Join logico:
  - `cadastro.iptunaogeracarnecgm.j68_naogeracarne = cadastro.iptunaogeracarne.j66_sequencial`
  - `cadastro.iptunaogeracarnecgm.j68_numcgm = protocolo.cgm.z01_numcgm`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: iptubase_para_iptunaogeracarne_via_iptunaogeracarnematric

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.iptubase` com `cadastro.iptunaogeracarne` usando `cadastro.iptunaogeracarnematric`.
- Origem de negocio: `cadastro.iptubase`.
- Destino de negocio: `cadastro.iptunaogeracarne`.
- Tabelas no caminho:
  - `cadastro.iptubase`
  - `cadastro.iptunaogeracarnematric`
  - `cadastro.iptunaogeracarne`
- Caminho de negocio:
  - iptubase -> iptunaogeracarnematric -> iptunaogeracarne
- Join logico:
  - `cadastro.iptunaogeracarnematric.j131_matric = cadastro.iptubase.j01_matric`
  - `cadastro.iptunaogeracarnematric.j131_naogeracarne = cadastro.iptunaogeracarne.j66_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Receita de relacionamento: caracter_para_iptupadraoconstr_via_iptupadraoconstrarea

- Tipo: caminho candidato por tabela ponte.
- Quando usar: perguntas que precisem relacionar `cadastro.caracter` com `cadastro.iptupadraoconstr` usando `cadastro.iptupadraoconstrarea`.
- Origem de negocio: `cadastro.caracter`.
- Destino de negocio: `cadastro.iptupadraoconstr`.
- Tabelas no caminho:
  - `cadastro.caracter`
  - `cadastro.iptupadraoconstrarea`
  - `cadastro.iptupadraoconstr`
- Caminho de negocio:
  - caracter -> iptupadraoconstrarea -> iptupadraoconstr
- Join logico:
  - `cadastro.iptupadraoconstrarea.j116_caracter = cadastro.caracter.j31_codigo`
  - `cadastro.iptupadraoconstrarea.j116_iptupadraoconstr = cadastro.iptupadraoconstr.j115_sequencial`
- Cardinalidade: Preencher.
- Filtros recomendados:
  - Preencher filtros de negocio.
- Cuidados:
  - Receita gerada automaticamente por FK. Validar se a tabela ponte representa o relacionamento de negocio esperado.

## Observacao de limite

- O catalogo possui 227 FKs candidatas. Este arquivo gerou no maximo 80 receitas para revisao inicial.
- Aumente `--max-relationship-recipes` se precisar de mais caminhos brutos.
