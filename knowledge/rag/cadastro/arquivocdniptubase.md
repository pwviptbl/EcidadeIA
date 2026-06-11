## cadastro.arquivocdniptubase



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.arquivocdniptubase`



### Resumo tecnico

- Descricao: Guarda as informações do vinculo dos arquivos gerados com as matrículas dos imóveis.
- Chave primaria: j151_iptubase, j151_arquivocdn
- Chave de negocio: Nao informada.
- Coluna de tempo: Nao informada.
- Grao: Nao informado.
- Recomendada: nao
- Significado da contagem: Preencher se esta tabela for usada para contagem.
- Candidatas a chave de negocio: Nenhuma inferida automaticamente.
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j151_arquivocdn` -> `configuracoes.arquivocdn` (db59_sequencial) [arquivocdniptubase_j151_arquivocdn_fkey]
- `j151_iptubase` -> `cadastro.iptubase` (j01_matric) [arquivocdniptubase_j151_iptubase_fkey]

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
