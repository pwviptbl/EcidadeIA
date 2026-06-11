## cadastro.iptutaxamatric



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptutaxamatric`



### Resumo tecnico

- Descricao: Tabela que ligação com a iptucadtaxa por matricula
- Chave primaria: j09_iptutaxamatric
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j09_iptutaxamatric, j09_matric
- Candidatas a coluna de tempo: j09_iptucadtaxaexe

### Relacionamentos

- `j09_matric` -> `cadastro.iptubase` (j01_matric) [iptutaxamatric_matric_fk]
- `j09_iptucadtaxaexe` -> `cadastro.iptucadtaxaexe` (j08_iptucadtaxaexe) [iptutaxamatric_taxaexe_fk]

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
