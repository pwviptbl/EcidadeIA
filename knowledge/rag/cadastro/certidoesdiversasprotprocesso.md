## cadastro.certidoesdiversasprotprocesso



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.certidoesdiversasprotprocesso`



### Resumo tecnico

- Descricao: Preencher.
- Chave primaria: j184_id
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j184_id, j184_id_certidoesdiversas
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j184_id_certidoesdiversas` -> `cadastro.certidoesdiversas` (j183_id) [certidoesdiversasprotprocesso_j184_id_certidao_fk]
- `j184_protprocesso` -> `protocolo.protprocesso` (p58_codproc) [certidoesdiversasprotprocesso_j184_protprocesso_fk]

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
