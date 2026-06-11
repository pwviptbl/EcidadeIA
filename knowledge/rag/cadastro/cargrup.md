## cadastro.cargrup



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.cargrup`



### Resumo tecnico

- Descricao: Cadastro dos grupos usados para classificar características de lotes, construções, faces de quadra e outros contextos. O campo `j32_tipo` identifica o tipo de aplicação do grupo, como `L` para lote, `C` para construção, `F` para face de quadra, `I` para ITBI, `O` para obras e `A` para água.
- Chave primaria: j32_grupo
- Chave de negocio: j32_grupo
- Coluna de tempo: Nao informada.
- Grao: Uma linha por grupo de características.
- Recomendada: sim
- Significado da contagem: Conta grupos de características cadastrados. Não conta características individuais, lotes, construções ou faces. Para contar características por grupo, cruzar com `cadastro.caracter`.
- Candidatas a chave de negocio: j32_grupo
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- Nenhum relacionamento catalogado.

### Filtros padrao

- Grupo específico `j32_grupo = :grupo`
- Busca por descrição `j32_descr ILIKE :descricao`
- Grupos de lote `j32_tipo = 'L'`
- Grupos de construção `j32_tipo = 'C'`
- Grupos de face de quadra `j32_tipo = 'F'`
- Grupos de ITBI `j32_tipo = 'I'`
- Grupos de obras `j32_tipo = 'O'`
- Grupos de água `j32_tipo = 'A'`
- Grupos sem tipo informado `j32_tipo IS NULL`
- Grupos com tipo fora do domínio esperado `j32_tipo NOT IN ('L', 'C', 'F', 'I', 'O', 'A')`

### Semantica de filtros

- `j32_grupo` identifica de forma segura o grupo de características.
- `j32_descr` é descrição textual e pode variar conforme parametrização do município.
- `j32_tipo = 'L'` indica grupos aplicáveis a características de lote.
- `j32_tipo = 'C'` indica grupos aplicáveis a características de construção.
- `j32_tipo = 'F'` indica grupos aplicáveis a características de face de quadra.
- `j32_tipo = 'I'` indica grupos aplicáveis a contexto de ITBI.
- `j32_tipo = 'O'` indica grupos aplicáveis a contexto de obras.
- `j32_tipo = 'A'` indica grupos aplicáveis a contexto de água.
- Para listar características de um grupo, cruzar `cargrup.j32_grupo` com `caracter.j31_grupo`.
- Para analisar características aplicadas a lotes, filtrar grupos do tipo `L` e cruzar com `caracter` e `carlote`.
- Para analisar características aplicadas a construções, filtrar grupos do tipo `C` e cruzar com `caracter` e `carconstr`.
- Para analisar características aplicadas a faces de quadra, filtrar grupos do tipo `F` e cruzar com `caracter` e `carface`.
- O tipo do grupo ajuda a evitar misturar características de naturezas diferentes em análises e consultas.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa a classificação superior das características usadas pelo sistema. Ela define grupos de características e informa em qual contexto esses grupos devem ser aplicados: lote, construção, face de quadra, ITBI, obras, água ou outro uso parametrizado.
  - É uma tabela de organização semântica. Ela não descreve o imóvel diretamente, mas ajuda a interpretar corretamente as características cadastradas em `caracter` e aplicadas nas tabelas de vínculo.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver organização, classificação ou tipo das características.
  - Deve ser usada quando for necessário separar características de lote, construção e face de quadra.
  - Deve ser combinada com `caracter` para obter a lista de características pertencentes a cada grupo.
  - Deve ser combinada com `carlote` quando a análise envolver características aplicadas a lotes.
  - Deve ser combinada com `carconstr` quando a análise envolver características aplicadas a construções.
  - Deve ser combinada com `carface` quando a análise envolver características aplicadas a faces de quadra.
  - Não deve substituir `caracter`, pois `cargrup` guarda o grupo, não a característica individual.
  - Não deve substituir `carlote`, `carconstr` ou `carface`, pois não informa quais lotes, construções ou faces possuem determinada característica.
  - Não deve substituir tabelas de cálculo, pois não guarda valores, áreas, alíquotas ou lançamentos.

- Que perguntas ela responde bem?

### Cuidados / riscos

- `cargrup` é tabela de domínio/classificação, não tabela de ocorrência cadastral.
- Contar linhas da `cargrup` conta grupos, não características, lotes, construções ou faces.
- Para contar características por grupo, cruzar com `caracter`.
- Para contar lotes por grupo de características, cruzar com `caracter` e `carlote`.
- Para contar construções por grupo de características, cruzar com `caracter` e `carconstr`.
- Para contar faces de quadra por grupo de características, cruzar com `caracter` e `carface`.
- Os tipos `L`, `C`, `F`, `I`, `O` e `A` devem ser tratados como domínio local do sistema e podem depender da parametrização do município.
- Grupos podem existir sem características vinculadas.
- Características podem estar em grupo inadequado por erro cadastral ou parametrização antiga.
- A descrição do grupo pode ser genérica, abreviada ou específica do município.
- Como as características são dinâmicas, não assumir padronização nacional ou universal dos grupos.
- Para análise de impacto no IPTU, `cargrup` apenas ajuda a classificar; o efeito financeiro precisa ser verificado em `caracter`, tabelas de vínculo e tabelas de cálculo.
- Para consultas assistidas por IA, usar `j32_tipo` para evitar misturar características de lote, construção e face de quadra.
