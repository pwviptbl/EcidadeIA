## cadastro.iptucadtaxaexe



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucadtaxaexe`



### Resumo tecnico

- Descricao: Cadastro de dados da taxa por ano
- Chave primaria: j08_iptucadtaxaexe
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: j08_db_sysfuncoes, j08_iptucadtaxa, j08_iptucadtaxaexe
- Candidatas a coluna de tempo: j08_anousu, j08_iptucadtaxa, j08_iptucadtaxaexe

### Relacionamentos

- `j08_iptucadtaxa` -> `cadastro.iptucadtaxa` (j07_iptucadtaxa) [iptucadtaxaexe_iptucadtaxa_fk]
- `j08_iptucalh` -> `cadastro.iptucalh` (j17_codhis) [iptucadtaxaexe_iptucalh_fk]
- `j08_tabrec` -> `caixa.tabrec` (k02_codigo) [iptucadtaxaexe_tabrec_fk]

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
