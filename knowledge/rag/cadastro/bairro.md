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
- Para alunos, contribuintes ou outros objetos por bairro, usar a tabela de endereço/localização específica do módulo.
- Em bases migradas, bairros antigos podem ter sido consolidados, renomeados ou mantidos por compatibilidade.
- Antes de comparar bairros entre municípios ou bases diferentes, validar se os códigos são locais e não padronizados nacionalmente.
- Para consultas assistidas por IA, não assumir relacionamento com uma tabela apenas porque existe campo com nome parecido; validar FK, documentação ou regra do módulo.

---

## Consultas extraídas de `db_bairro_classe.php`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_bairro_classe.php`
- **Classe:** `cl_bairro`
- **Tabela principal:** `cadastro.bairro`
- **Campos físicos:** `j13_codi`, `j13_descr`, `j13_codant`, `j13_rural`

### Leitura direta: `sql_query` e `sql_query_file`

- **Objetivo:** Consultar o cadastro físico de bairros.
- **Filtro padrão:** `bairro.j13_codi = :codigo_bairro`, quando o código é informado e não há `$dbwhere`.
- **Campos e ordenação:** São recebidos dinamicamente e separados por `#`.
- **Diferença entre métodos:** Nesta versão da classe, `sql_query` e `sql_query_file` montam a mesma estrutura.
- **Grão:** Uma linha por bairro cadastrado.

```sql
SELECT /* campos dinâmicos */
FROM bairro
WHERE bairro.j13_codi = :codigo_bairro
ORDER BY /* ordenação dinâmica */;
```

### Bairro vinculado ao logradouro: `sql_getBairroByCodRua`

- **Objetivo:** Retornar os bairros associados a um código de rua/logradouro.
- **Tabelas:** `ruasbairro`, `ruas`, `bairro`.
- **Junções:**
  - `ruas.j14_codigo = ruasbairro.j16_lograd`
  - `bairro.j13_codi = ruasbairro.j16_bairro`
- **Filtro:** `ruas.j14_codigo = :codigo_rua`.
- **Campos retornados:** Todos os campos de `bairro`.
- **Grão:** Uma linha por vínculo entre a rua e um bairro.
- **Regra comprovada:** O bairro do logradouro é obtido pela tabela associativa `ruasbairro`; não existe vínculo direto entre `ruas` e `bairro` nesta consulta.
- **Cuidados:**
  - Uma rua pode estar vinculada a mais de um bairro e gerar várias linhas.
  - Não usar o primeiro resultado como bairro único sem validar a quantidade retornada.
  - Para contar bairros de uma rua, usar `COUNT(DISTINCT bairro.j13_codi)`.

```sql
SELECT bairro.*
FROM ruasbairro
JOIN ruas
  ON ruas.j14_codigo = ruasbairro.j16_lograd
JOIN bairro
  ON bairro.j13_codi = ruasbairro.j16_bairro
WHERE ruas.j14_codigo = :codigo_rua;
```

### Código de bairro por faixa de CEP: `sql_buscaBairroPorCep`

- **Objetivo:** Localizar faixas de CEP que contenham o CEP informado.
- **Tabela:** `cepbairrosfaixa`.
- **Campos retornados:** `cp02_codbairro`, `cp02_faixa`, `cp02_cepinicial`, `cp02_cepfinal`.
- **Filtro de faixa:**
  - `cp02_cepinicial::int <= :cep::int`
  - `cp02_cepfinal::int >= :cep::int`
- **Grão:** Uma linha por faixa de CEP compatível.
- **Regra comprovada:** O CEP pertence à faixa quando está numericamente entre o CEP inicial e o CEP final, inclusive.
- **Uso observado:** O importador MEI tenta usar esta consulta antes de procurar o bairro por código informado ou por nome.
- **Cuidados:**
  - A consulta não faz `JOIN` com `bairro` e não retorna `j13_codi` ou `j13_descr`.
  - `cp02_codbairro` é o código indicado pela faixa, mas o vínculo com `bairro.j13_codi` não é validado neste método.
  - O consumidor em `model/meiArquivo.model.php` verifica posteriormente `j13_codi`, embora esta SQL retorne `cp02_codbairro`. Não depender desse campo sem alias ou conversão explícita.
  - Faixas sobrepostas podem retornar mais de uma linha para o mesmo CEP.
  - A consulta não possui `ORDER BY`; não há prioridade definida entre faixas coincidentes.
  - Os CEPs são convertidos de texto para inteiro. Formatação, caracteres não numéricos ou valores fora do intervalo aceito pelo tipo podem causar erro.
  - A conversão numérica elimina zeros à esquerda. Para comparações textuais ou preservação do formato, esta consulta não é adequada.

```sql
SELECT
  cp02_codbairro,
  cp02_faixa,
  cp02_cepinicial,
  cp02_cepfinal
FROM cepbairrosfaixa
WHERE cp02_cepinicial::int <= :cep::int
  AND cp02_cepfinal::int >= :cep::int;
```

### Estratégia segura para identificar bairro

1. Quando existir código de rua confiável, consultar `ruasbairro` por `sql_getBairroByCodRua`.
2. Se o resultado possuir exatamente um bairro, usar `bairro.j13_codi`.
3. Se houver múltiplos bairros para a rua, exigir outro critério de desambiguação.
4. Para CEP, tratar `cepbairrosfaixa.cp02_codbairro` como candidato e validar sua existência em `bairro`.
5. Se a faixa de CEP não for única, não escolher arbitrariamente a primeira linha.
6. Como fallback por nome, comparar `TRIM(j13_descr)` ou busca tolerante, mas validar duplicidades.
