## cadastro.bairro



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.bairro`



### Resumo tecnico

- Descricao: Cadastro dos bairros do município. Tabela de domínio/localização usada para padronizar a identificação de bairros em cadastros municipais, especialmente em objetos vinculados ao território do município.
- Chave primaria: j13_codi
- Chave de negocio: j13_codi
- Coluna de tempo: Nao informada.
- Grao: Uma linha por bairro cadastrado.
- Recomendada: sim
- Significado da contagem: Conta bairros cadastrados no sistema. Não conta imóveis, lotes, alunos, pessoas ou endereços. Para contar objetos por bairro, é necessário cruzar esta tabela com a tabela do objeto analisado.
- Candidatas a chave de negocio: j13_codi, j13_descr
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- Nenhum relacionamento catalogado.

### Perguntas que esta tabela ajuda a responder

- Quais bairros existem no município?
- Qual o código de determinado bairro?
- Quais bairros estão marcados como rurais?
- Quais bairros estão marcados como urbanos?
- Existem bairros duplicados ou com nomes semelhantes?
- Quais bairros possuem código anterior de conversão?
- Quantos bairros estão cadastrados no sistema?
- Quantos imóveis existem em cada bairro?
- Quantos lotes/terrenos existem em cada bairro?
- Quais bairros concentram mais matrículas imobiliárias?
- Quais bairros concentram mais alunos, contribuintes, processos, imóveis ou outros objetos, quando houver relacionamento com tabelas do respectivo módulo?
- Em quais tabelas ou módulos o bairro aparece como dimensão de localização?

### Filtros padrao

- Bairro específico por código `j13_codi = :bairro`
- Bairro específico por nome `j13_descr ILIKE :nome_bairro`
- Bairros rurais `j13_rural IS TRUE`
- Bairros urbanos `j13_rural IS FALSE`
- Bairros sem classificação rural/urbana `j13_rural IS NULL`
- Código anterior específico `j13_codant = :codigo_anterior`
- Bairros com código anterior `j13_codant IS NOT NULL`
- Bairros sem código anterior `j13_codant IS NULL`

### Semantica de filtros

- `j13_codi` é o identificador técnico seguro do bairro.
- `j13_descr` é o nome do bairro e pode sofrer variação de grafia, abreviação, acentuação ou duplicidade.
- `j13_rural IS TRUE` indica bairro classificado como rural.
- `j13_rural IS FALSE` indica bairro não rural, normalmente urbano, mas essa interpretação deve ser validada conforme regra local.
- `j13_rural IS NULL` indica ausência de classificação explícita, não devendo ser automaticamente tratado como urbano.
- `j13_codant` deve ser usado para rastrear códigos antigos em migrações ou conversões, não como chave principal atual.
- Para contar imóveis por bairro, não contar linhas da `bairro`; cruzar com `cadastro.lote` e, quando necessário, com `cadastro.iptubase`.
- Para contar matrículas por bairro, usar o bairro do lote vinculado à matrícula.
- Para contar objetos de outros módulos por bairro, usar sempre o campo de bairro da tabela do módulo específico, quando existir.
- Para análises oficiais, preferir agrupamento por `j13_codi` e exibir `j13_descr`, evitando agrupar apenas por nome.
- Para maior IPTU por bairro, usar a receita `bairro_para_ranking_iptu` e ordenar pela soma de `iptucalv.j21_valor`.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa o cadastro padronizado dos bairros do município. Como o sistema é integrado, essa tabela pode servir como referência de localização para várias tabelas e módulos sempre que o objeto analisado precisa ser associado a um bairro municipal.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta for sobre a lista oficial de bairros cadastrados, identificação do código do bairro, descrição do bairro ou classificação rural/urbana.
  - Deve ser usada como dimensão de apoio para análises por bairro.
  - Não deve ser usada sozinha para contar imóveis, lotes, alunos, contribuintes ou processos.
  - Para imóveis por bairro, deve ser combinada com `cadastro.lote` e `cadastro.iptubase`.
  - Para alunos por bairro, deve ser combinada com as tabelas do módulo de educação que armazenam endereço ou bairro do aluno.
  - Para contribuintes por bairro, deve ser combinada com tabelas de endereço ou cadastro que possuam vínculo com bairro.
  - Para análises tributárias, usar esta tabela apenas como dimensão de localização, não como fonte de valores de IPTU.

- Que perguntas ela responde bem?

  - Quais bairros estão cadastrados?
  - Qual é o código de um bairro?
  - Qual é o nome de um bairro pelo código?

### Cuidados / riscos

- Esta é uma tabela cadastral/dimensional. Contar linhas conta bairros, não objetos vinculados aos bairros.
- Pode haver bairros com nomes duplicados, abreviados, grafados de forma diferente ou com acentuação inconsistente.
- Agrupar apenas por `j13_descr` pode gerar erro se houver duplicidade ou variação textual. Preferir `j13_codi`.
- `j13_codant` é código legado e deve ser usado apenas em contexto de migração/conversão.
- `j13_rural` pode estar nulo ou mal preenchido. Validar antes de usar em relatório oficial.
- A ausência de relacionamento catalogado não significa que a tabela não seja usada por outros módulos; significa apenas que a FK não foi documentada ou inferida no catálogo.
- Para imóveis por bairro, o caminho mais seguro é localizar o bairro no lote e depois relacionar o lote com a matrícula.
- Para valores de IPTU por bairro, cruzar bairro com lote, iptubase e tabelas de cálculo/valores.
- Para ranking de IPTU por bairro, usar o caminho bairro -> lote -> iptubase -> iptucalv -> iptucalh e ordenar a soma final.
- Para alunos, contribuintes ou outros objetos por bairro, usar a tabela de endereço/localização específica do módulo.
- Em bases migradas, bairros antigos podem ter sido consolidados, renomeados ou mantidos por compatibilidade.
- Antes de comparar bairros entre municípios ou bases diferentes, validar se os códigos são locais e não padronizados nacionalmente.
- Para consultas assistidas por IA, não assumir relacionamento com uma tabela apenas porque existe campo com nome parecido; validar FK, documentação ou regra do módulo.
