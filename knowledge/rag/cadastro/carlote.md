## cadastro.carlote



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carlote`



### Resumo tecnico

- Descricao: Cadastro das características dos lotes/terrenos. Cada registro associa um lote a uma característica cadastrada em `cadastro.caracter`. Essas características são dinâmicas e podem variar conforme o município, podendo impactar regras cadastrais, avaliação territorial, valor venal, fatores de cálculo e enquadramentos usados no IPTU.
- Chave primaria: j35_idbql, j35_caract
- Chave de negocio: j35_idbql, j35_caract
- Coluna de tempo: j35_dtlanc
- Grao: Uma linha por lote e característica.
- Recomendada: sim
- Significado da contagem: Conta vínculos de características em lotes. Não conta lotes diretamente quando um mesmo lote possui várias características. Para contar lotes com determinada característica, usar `COUNT(DISTINCT j35_idbql)`.
- Candidatas a chave de negocio: j35_idbql, j35_caract
- Candidatas a coluna de tempo: j35_dtlanc

### Relacionamentos

- `j35_caract` -> `cadastro.caracter` (j31_codigo) [carlote_caract_fk]
- `j35_idbql` -> `cadastro.lote` (j34_idbql) [carlote_idbql_fk]

### Filtros padrao

- Lote específico `j35_idbql = :idbql`
- Característica específica `j35_caract = :caracteristica`
- Lotes com lista de características `j35_caract IN (:lista_caracteristicas)`
- Características lançadas em período `j35_dtlanc BETWEEN :data_inicio AND :data_fim`
- Características lançadas a partir de uma data `j35_dtlanc >= :data_inicio`
- Características sem data de lançamento `j35_dtlanc IS NULL`
- Contagem de uso por característica `GROUP BY j35_caract`
- Contagem de características por lote `GROUP BY j35_idbql`
- Contagem de lotes por característica `GROUP BY j35_caract` usando `COUNT(DISTINCT j35_idbql)`

### Semantica de filtros

- `j35_idbql, j35_caract` identificam de forma segura uma característica vinculada a um lote.
- `j35_idbql` identifica o lote, não a matrícula. Para chegar à matrícula/imóvel, cruzar com `cadastro.iptubase` por `j01_idbql`.
- `j35_caract` identifica a característica, mas sua descrição e significado devem ser obtidos em `cadastro.caracter`.
- `j35_dtlanc` indica a data de lançamento da característica no lote, não necessariamente a data em que a condição física passou a existir.
- Para interpretar grupo, descrição, pontos ou natureza da característica, cruzar com `cadastro.caracter`.
- Para saber se a característica é de lote, validar o grupo da característica em `caracter`/`cargrup`, quando disponível.
- Para analisar imóveis ativos vinculados ao lote, cruzar com `cadastro.iptubase` e aplicar `j01_baixa IS NULL`.
- Para análise por bairro, setor, quadra ou zona, cruzar com `cadastro.lote`.
- Para análise de impacto no valor venal territorial, cruzar com `cadastro.iptucalc`.
- Para análise de impacto no valor final do IPTU, cruzar com `cadastro.iptucalv`.
- Para encontrar padrões de lote, agrupar as características por `j35_idbql` e comparar conjuntos de `j35_caract`.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa o vínculo entre lotes/terrenos e suas características cadastrais. Essas características descrevem condições ou atributos do lote, como situação, topografia, pedologia, infraestrutura, localização, uso, condição territorial ou outros critérios configurados pelo município.
  - Essas características podem impactar o cálculo do IPTU, pois podem influenciar valor venal territorial, fatores de valorização ou desvalorização, pontuação, enquadramento e aplicação de regras específicas da fórmula de cálculo.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver características do lote/terreno.
  - Deve ser usada para analisar predominância de características territoriais.
  - Deve ser usada para montar padrões de lote com base no conjunto de características vinculadas.
  - Deve ser combinada com `caracter` quando for necessário obter descrição, grupo ou pontuação da característica.
  - Deve ser combinada com `lote` quando for necessário obter setor, quadra, bairro, zona, área ou demais dados territoriais.
  - Deve ser combinada com `iptubase` quando for necessário chegar às matrículas/imóveis vinculados ao lote.
  - Deve ser combinada com `iptucalc` quando for necessário avaliar impacto das características no valor venal territorial.
  - Não deve substituir `lote`, pois `carlote` não guarda os dados físicos principais do lote.
  - Não deve substituir `caracter`, pois `carlote` não descreve a característica; apenas referencia o código.
  - Não deve substituir `iptucalc` ou `iptucalv`, pois não guarda valores calculados ou valores de receita.

### Cuidados / riscos

- As características são dinâmicas e podem variar por município. Não tratar a lista de características como domínio fixo universal.
- Contar linhas da `carlote` conta vínculos de características, não lotes nem imóveis.
- Um lote pode possuir várias características.
- Um mesmo lote pode estar vinculado a uma ou mais matrículas em `iptubase`.
- Para contar lotes com característica, usar `COUNT(DISTINCT j35_idbql)`.
- Para contar imóveis/matrículas com característica de lote, cruzar com `iptubase` e usar `COUNT(DISTINCT j01_matric)`.
- `j35_dtlanc` indica lançamento cadastral da característica, não necessariamente início real da condição física.
- Características podem estar incompletas, ausentes ou mal cadastradas, especialmente em bases antigas ou migradas.
- Para análise de imóveis ativos, cruzar com `iptubase` e filtrar `j01_baixa IS NULL`.
- Para análise territorial, cruzar com `lote`.
- Para análise por bairro, setor ou zona, não usar `carlote` isoladamente; buscar essas dimensões no lote.
- Características podem afetar cálculo, mas o efeito exato depende da fórmula, do exercício, do grupo da característica e da parametrização municipal.
- Para explicar impacto financeiro, cruzar com `iptucalc` e `iptucalv`.
- Para explicar impacto territorial, cruzar com `lote`, `zonas`, `bairro`, `setor`, `testada` e tabelas de valor/fator quando aplicável.
