## cadastro.caracter



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.caracter`



### Resumo tecnico

- Descricao: Cadastro das características usadas para lotes, construções, faces de quadra e outros contextos configurados no sistema. A classificação do tipo da característica é definida pelo grupo vinculado em `cadastro.cargrup`, onde `j32_tipo` pode indicar, por exemplo, `L` para lote, `C` para construção e `F` para face de quadra.
- Chave primaria: j31_codigo
- Chave de negocio: j31_codigo
- Coluna de tempo: Nao informada.
- Grao: Uma linha por característica cadastrada.
- Recomendada: sim
- Significado da contagem: Conta características cadastradas. Não conta lotes, construções, faces ou imóveis que usam essas características. Para contar uso real das características, cruzar com tabelas de vínculo como `carlote`, `carconstr` ou `carface`.
- Candidatas a chave de negocio: j31_codigo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j31_grupo` -> `cadastro.cargrup` (j32_grupo) [caracter_grupo_fk]

### Relacionamentos

- `j31_grupo` -> `cadastro.cargrup` (j32_grupo) [caracter_grupo_fk]

### Filtros padrao

- Característica específica `j31_codigo = :caracteristica`
- Busca por descrição `j31_descr ILIKE :descricao`
- Grupo específico `j31_grupo = :grupo`
- Características com pontuação positiva `COALESCE(j31_pontos, 0) > 0`
- Características sem pontuação `COALESCE(j31_pontos, 0) = 0`
- Características de lote, cruzando com `cargrup`: `j32_tipo = 'L'`
- Características de construção, cruzando com `cargrup`: `j32_tipo = 'C'`
- Características de face de quadra, cruzando com `cargrup`: `j32_tipo = 'F'`
- Características de ITBI, cruzando com `cargrup`: `j32_tipo = 'I'`
- Características de obras, cruzando com `cargrup`: `j32_tipo = 'O'`
- Características de água, cruzando com `cargrup`: `j32_tipo = 'A'`

### Semantica de filtros

- `j31_codigo` identifica de forma segura uma característica.
- `j31_descr` é descrição textual e pode variar conforme parametrização municipal, conversão de dados ou cadastro local.
- `j31_grupo` classifica a característica dentro de um grupo, mas o tipo de aplicação deve ser interpretado em `cadastro.cargrup`.
- `j31_pontos` representa pontuação atribuída à característica, mas não explica sozinho a regra completa de cálculo.
- Para saber se a característica é de lote, construção ou face de quadra, cruzar `j31_grupo` com `cargrup.j32_grupo` e avaliar `j32_tipo`.
- Para saber quais lotes usam uma característica, cruzar com `cadastro.carlote`.
- Para saber quais construções usam uma característica, cruzar com `cadastro.carconstr`.
- Para saber quais faces de quadra usam uma característica, cruzar com `cadastro.carface`.
- Para analisar impacto no valor venal territorial, cruzar características de lote com `carlote`, `lote`, `iptubase` e `iptucalc`.
- Para analisar impacto no valor venal da construção, cruzar características de construção com `carconstr`, `iptuconstr` e `iptucale`.
- Para analisar impacto no valor final calculado, cruzar com `iptucalv`.
- Como características são dinâmicas por município, o significado de cada código deve ser interpretado pela própria base analisada.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa o cadastro mestre das características utilizadas pelo município para qualificar lotes, construções, faces de quadra e outros objetos parametrizados no sistema.
  - Essas características ajudam a descrever condições físicas, cadastrais, construtivas, territoriais ou de infraestrutura.
  - Dependendo da parametrização municipal, podem influenciar pontuação, padrão, enquadramento, fator, valor de metro quadrado, valor venal e cálculo de IPTU ou taxas.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver descrição, código, grupo ou pontuação de uma característica.
  - Deve ser usada para interpretar códigos existentes em `carlote`, `carconstr` e `carface`.
  - Deve ser combinada com `cargrup` quando for necessário separar características de lote, construção, face de quadra, ITBI, obras ou água.
  - Deve ser combinada com `carlote` quando for necessário saber quais lotes possuem determinada característica.
  - Deve ser combinada com `carconstr` quando for necessário saber quais construções possuem determinada característica.
  - Deve ser combinada com `carface` quando for necessário saber quais faces de quadra possuem determinada característica.
  - Não deve substituir `cargrup`, pois `caracter` guarda a característica individual, não a classificação superior do grupo.
  - Não deve substituir tabelas de vínculo, pois não informa onde a característica foi aplicada.
  - Não deve substituir tabelas de cálculo, pois não guarda valor venal, valor de IPTU, débito ou lançamento.

### Cuidados / riscos

- `caracter` é tabela de cadastro mestre de características, não tabela de ocorrência.
- Contar linhas da `caracter` conta características cadastradas, não lotes, construções, faces ou imóveis.
- As características são dinâmicas e podem variar por município/cliente.
- O código da característica deve ser interpretado dentro da base analisada.
- A descrição da característica pode ser genérica, abreviada, duplicada ou específica da parametrização municipal.
- O grupo da característica deve ser interpretado por `cargrup`.
- Para separar características de lote, construção e face, usar `cargrup.j32_tipo`.
- `j31_pontos` pode influenciar cálculo ou classificação, mas seu efeito depende da fórmula, exercício e parametrização municipal.
- Características cadastradas podem não estar em uso.
- Características usadas em vínculos podem estar mal classificadas se o grupo foi parametrizado incorretamente.
- Para análise de características predominantes, não usar `caracter` isoladamente; cruzar com `carlote`, `carconstr` ou `carface`.
- Para análise de impacto no IPTU, cruzar com tabelas de vínculo e tabelas de cálculo, como `iptucalc`, `iptucale` e `iptucalv`.
- Para consultas assistidas por IA, nunca assumir significado pelo código numérico; buscar descrição e grupo.
