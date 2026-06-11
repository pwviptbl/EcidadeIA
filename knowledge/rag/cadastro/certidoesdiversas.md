## cadastro.certidoesdiversas



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.certidoesdiversas`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j183_id
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j183_id, j183_id_usuario, j183_inscr_iss, j183_matric_iptu, j183_numcgm
- Candidatas a coluna de tempo: j183_data, j183_dtprocesso

### Relacionamentos

- `j183_id_usuario` -> `configuracoes.db_usuarios` (id_usuario) [certidoesdiversas_j183_id_usuario_fk]
- `j183_inscr_iss` -> `issqn.issbase` (q02_inscr) [certidoesdiversas_j183_inscr_iss_fk]
- `j183_matric_iptu` -> `cadastro.iptubase` (j01_matric) [certidoesdiversas_j183_matric_iptu_fk]
- `j183_numcgm` -> `protocolo.cgm` (z01_numcgm) [certidoesdiversas_j183_numcgm_fk]

### Filtros padrao

- Nenhum filtro padrao catalogado.

### Semantica de filtros

- Nenhuma semantica de filtro catalogada.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?
- Quando ela deve ser preferida sobre outras tabelas parecidas?
- Que perguntas ela responde bem?
- Que filtros de negocio sao seguros?
- O que nao pode ser inferido a partir dela?

### Cuidados / riscos

- Preencher com ambiguidades, excecoes e limites conhecidos.
