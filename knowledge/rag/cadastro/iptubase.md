## cadastro.iptubase



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptubase`



### Resumo tecnico

- Descricao: Cadastro principal das matrículas imobiliárias do IPTU. Cada registro representa uma matrícula do imóvel, vinculada a um lote e a um contribuinte principal.
- Chave primaria: j01_matric
- Chave de negocio: j01_matric
- Coluna de tempo: j01_baixa
- Grao: Uma linha por matrícula imobiliária.
- Recomendada: sim
- Significado da contagem: Conta matrículas imobiliárias cadastradas. Para contar imóveis ativos, aplicar j01_baixa IS NULL. Para análise territorial por lote, avaliar duplicidade de matrículas por j01_idbql.
- Candidatas a chave de negocio: j01_matric
- Candidatas a coluna de tempo: j01_baixa

### Relacionamentos

- `j01_idbql` -> `cadastro.lote` (j34_idbql) [iptubase_idbql_fk]
- `j01_numcgm` -> `protocolo.cgm` (z01_numcgm) [iptubase_numcgm_fk]
- `j01_tipo_contribuinte, j01_tipo_contribuinte, j01_tipo_contribuinte` -> `cadastro.tipocontribuinte` (j147_sequencial, j147_sequencial, j147_sequencial) [tipocontribuinte_sequencial_fk]

### Filtros padrao

- Matrícula específica `j01_matric = :matricula`
- Matrículas ativas `j01_baixa IS NULL` Usado para excluir baixadas |
- Proprietário principal `j01_numcgm = :numcgm`

### Regra de negocio para enriquecer

- A iptubase é a tabela central do cadastro imobiliário para localizar a matrícula e conectá-la ao lote, ao contribuinte principal e às demais informações cadastrais.
- Para análises de IPTU, normalmente a iptubase deve ser combinada com tabelas financeiras, como iptucalc, iptucalv, iptunump ou equivalentes, usando a matrícula e o exercício.
- Para análises físicas do imóvel, combinar com lote, iptuconstr, testada, testpri, bairro, setor, zonas e características.
- Para análise de titularidade completa, não usar apenas j01_numcgm; combinar com tabelas de proprietários, promitentes e averbações.
- Para análises de imóveis ativos, sempre aplicar j01_baixa IS NULL, salvo quando a pergunta envolver histórico, baixas ou comparação cadastral ampla.
- Para contagem de imóveis, definir antes se “imóvel” significa matrícula, lote ou unidade tributável. A iptubase conta melhor matrículas.
