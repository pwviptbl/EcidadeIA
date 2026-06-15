## cadastro.carconstr



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.carconstr`



### Resumo tecnico

- Descricao: Cadastro das características das construções vinculadas aos imóveis. Cada registro associa uma construção de uma matrícula a uma característica cadastrada em `cadastro.caracter`. As características são dinâmicas e podem variar por município/cliente, portanto não devem ser tratadas como domínio fixo universal.
- Chave primaria: j48_matric, j48_idcons, j48_caract
- Chave de negocio: j48_matric, j48_idcons, j48_caract
- Coluna de tempo: Nao informada.
- Grao: Uma linha por matrícula, construção e característica.
- Recomendada: sim
- Significado da contagem: Conta vínculos de características em construções. Uma linha identifica uma característica aplicada a uma construção (`j48_matric, j48_idcons, j48_caract`). Para contar construções por característica partindo apenas de `carconstr`, agrupar por `j48_caract` e usar `COUNT(1)`. Use `COUNT(DISTINCT (j48_matric, j48_idcons))` somente se joins adicionais puderem multiplicar linhas. Para contar imóveis com determinada característica, usar `COUNT(DISTINCT j48_matric)`.
- Candidatas a chave de negocio: j48_matric, j48_idcons, j48_caract
- Candidatas a coluna de tempo: Nenhuma inferida automaticamente.

### Relacionamentos

- `j48_caract` -> `cadastro.caracter` (j31_codigo) [carconstr_caract_idcons_fk]

### Filtros padrao

- Matrícula específica `j48_matric = :matricula`
- Construção específica `j48_matric = :matricula AND j48_idcons = :idcons`
- Característica específica `j48_caract = :caracteristica`
- Construções com lista de características `j48_caract IN (:lista_caracteristicas)`
- Características de uma matrícula `j48_matric = :matricula`
- Características de uma construção `j48_matric = :matricula AND j48_idcons = :idcons`
- Contagem de uso por característica `GROUP BY j48_caract`
- Contagem de características por construção `GROUP BY j48_matric, j48_idcons`
- Contagem de imóveis por característica `GROUP BY j48_caract` usando `COUNT(DISTINCT j48_matric)`

### Semantica de filtros

- `j48_matric, j48_idcons, j48_caract` identificam de forma segura uma característica vinculada a uma construção.
- `j48_matric, j48_idcons` identificam a construção dentro da matrícula.
- `j48_caract` identifica a característica, mas sua descrição e significado devem ser obtidos em `cadastro.caracter`.
- A tabela representa presença/vínculo da característica. Ela não informa, sozinha, o valor monetário, o fator aplicado ou a regra completa de cálculo.
- Como as características são configuráveis por município, o mesmo código ou conjunto de características deve ser validado na base analisada.
- Para interpretar grupo, descrição e pontuação da característica, cruzar com `cadastro.caracter`.
- Para saber se a característica é de construção, validar o grupo da característica em `caracter`/`cargrup`, quando disponível.
- Para saber se a construção está ativa ou demolida, cruzar com `cadastro.iptuconstr`.
- Para analisar impacto no valor venal da edificação, cruzar com `cadastro.iptucale`.
- Para analisar impacto no valor final do IPTU ou taxas, cruzar com `cadastro.iptucalv`.
- Para análises por bairro, setor ou zona, cruzar com `iptuconstr`, `iptubase`, `lote` e tabelas de localização.
- Para encontrar padrões construtivos, agrupar as características por `j48_matric, j48_idcons` e comparar conjuntos de `j48_caract`.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa o vínculo entre construções e suas características cadastrais. Essas características descrevem aspectos da edificação, como padrão, tipo, uso, conservação, estrutura, acabamento ou outros atributos definidos pelo município.
  - Essas características podem impactar o cálculo do IPTU e taxas, pois podem influenciar pontuação, padrão construtivo, valor do metro quadrado, fatores de aumento, redução ou enquadramentos usados na fórmula de cálculo.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver quais características estão associadas a uma construção.
  - Deve ser usada para analisar predominância de características construtivas.
  - Deve ser usada para montar padrões de construção com base no conjunto de características vinculadas.
  - Deve ser combinada com `caracter` quando for necessário obter descrição, grupo ou pontuação da característica.
  - Deve ser combinada com `iptuconstr` quando for necessário validar área, construção principal, demolição, lançamento ou dados físicos da construção.
  - Deve ser combinada com `iptucale` quando for necessário avaliar impacto das características no valor venal calculado da edificação.
  - Não deve substituir `iptuconstr`, pois `carconstr` não guarda área, ano da construção, demolição ou endereço.
  - Não deve substituir `caracter`, pois `carconstr` não descreve a característica; apenas referencia o código.
  - Não deve substituir `iptucalc` ou `iptucalv`, pois não guarda valor final de cálculo ou valor de receita.

- Que perguntas ela responde bem?

### Cuidados / riscos

- As características são dinâmicas e podem variar por município. Nunca tratar a lista de características como domínio fixo universal.
- Contar linhas da `carconstr` conta vínculos de características, não construções nem imóveis.
- Uma construção pode ter várias características.
- Uma matrícula pode ter várias construções, e cada construção pode ter várias características.
- Para contar construções com característica, usar a combinação `j48_matric, j48_idcons`.
- Para contar imóveis com característica, usar `COUNT(DISTINCT j48_matric)`.
- A tabela não possui coluna de tempo; não permite análise histórica direta de quando uma característica foi incluída, alterada ou removida.
- Características podem estar incompletas, ausentes ou mal cadastradas, especialmente em bases antigas ou migradas.
- O relacionamento catalogado mostra apenas a característica; para ligação completa com construção, validar o vínculo lógico com `iptuconstr` por `j48_matric = j39_matric` e `j48_idcons = j39_idcons`.
- Para analisar construções ativas, sempre cruzar com `iptuconstr` e filtrar `j39_dtdemo IS NULL`.
- Para analisar matrículas ativas, cruzar com `iptubase` e filtrar `j01_baixa IS NULL`.
- Características podem afetar cálculo, mas o efeito exato depende da fórmula, do exercício, do grupo da característica e da parametrização municipal.
- Para explicar impacto financeiro, cruzar com `iptucale`, `iptucalc` e `iptucalv`.
- Para análise por localização, cruzar com `iptubase`, `lote`, bairro, setor e zona.
