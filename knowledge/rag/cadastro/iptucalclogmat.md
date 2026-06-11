## cadastro.iptucalclogmat



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalclogmat`



### Resumo tecnico

- Descricao: Matriculas do log do calculo do iptu
- Chave primaria: j28_codigo, j28_matric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j28_codigo, j28_matric, j28_tipologcalc
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j28_codigo` -> `cadastro.iptucalclog` (j27_codigo) [iptucalclogmat_codigo_fk]
- `j28_matric` -> `cadastro.iptubase` (j01_matric) [iptucalclogmat_matric_fk]
- `j28_tipologcalc` -> `cadastro.iptucadlogcalc` (j62_codigo) [iptucalclogmat_tipologcalc_fk]

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
