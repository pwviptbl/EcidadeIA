## cadastro.iptucale



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucale`



### Resumo tecnico

- Descricao: Registra os valores venais calculados para as construções vinculadas a uma matrícula em determinado exercício. Guarda a área edificada processada, pontos, valor do metro quadrado da construção e valor venal calculado por edificação.
- Chave primaria: j22_anousu, j22_matric, j22_idcons
- Chave de negocio: j22_anousu, j22_matric, j22_idcons
- Coluna de tempo: j22_anousu
- Grao: Uma linha por exercício, matrícula e construção calculada.
- Recomendada: sim
- Significado da contagem: Conta construções calculadas por exercício. Não conta imóveis diretamente. Para contar imóveis com construção calculada, usar `COUNT(DISTINCT j22_matric)` filtrando por exercício.
- Candidatas a chave de negocio: j22_anousu, j22_matric, j22_idcons
- Candidatas a coluna de tempo: j22_anousu

### Relacionamentos

- `j22_matric, j22_matric, j22_idcons, j22_idcons` -> `cadastro.iptuconstr` (j39_matric, j39_idcons, j39_matric, j39_idcons) [iptucale_matric_idcons_fk]

### Filtros padrao

- Exercício específico `j22_anousu = :exercicio`
- Matrícula específica `j22_matric = :matricula`
- Construção específica `j22_matric = :matricula AND j22_idcons = :idcons`
- Comparação entre exercícios `j22_anousu IN (:exercicio_anterior, :exercicio_atual)`
- Valor venal positivo `COALESCE(j22_valor, 0) > 0`
- Valor venal zerado `COALESCE(j22_valor, 0) = 0`
- Área edificada positiva `COALESCE(j22_areaed, 0) > 0`
- Sem área edificada calculada `COALESCE(j22_areaed, 0) = 0`
- Valor de m² positivo `COALESCE(j22_vm2, 0) > 0`
- Pontuação positiva `COALESCE(j22_pontos, 0) > 0`

### Semantica de filtros

- `j22_anousu` representa o exercício do cálculo e deve ser usado em qualquer análise temporal.
- `j22_matric, j22_idcons` identificam a construção calculada dentro de uma matrícula.
- `j22_anousu, j22_matric, j22_idcons` identificam de forma segura o cálculo de uma construção em um exercício.
- `j22_areaed` é a área edificada processada no cálculo, não necessariamente a área atual cadastrada em `iptuconstr`.
- `j22_valor` é o valor venal calculado da edificação, não o valor final do IPTU.
- `j22_vm2` é o valor do metro quadrado da construção usado no cálculo, não valor de mercado.
- `j22_pontos` representa a pontuação processada para a construção, normalmente relacionada às características e padrão construtivo.
- Para totalizar valor venal de edificações por matrícula, somar `j22_valor` agrupando por `j22_anousu, j22_matric`.
- Para totalizar área edificada calculada por matrícula, somar `j22_areaed` agrupando por `j22_anousu, j22_matric`.
- Para comparar exercícios, comparar a mesma combinação `j22_matric, j22_idcons` em anos diferentes.
- Para validar existência física ou situação da construção, cruzar com `iptuconstr`.
- Para explicar pontuação, padrão ou características da construção, cruzar com tabelas de características, como `carconstr` e `caracter`.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa o resultado do cálculo venal das edificações de uma matrícula em cada exercício. Ela mostra quanto cada construção contribuiu, em valor venal, para a composição cadastral/tributária do imóvel.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver valor venal da construção, área edificada usada no cálculo, valor do metro quadrado da construção, pontuação calculada ou comparação do valor das edificações entre exercícios.
  - Deve ser usada quando for necessário explicar o impacto das construções no cálculo do IPTU.
  - Deve ser preferida sobre `iptuconstr` quando a pergunta for sobre valores calculados da edificação.
  - Deve ser combinada com `iptuconstr` quando for necessário comparar cadastro físico atual com cálculo processado.
  - Deve ser combinada com `iptucalc` quando for necessário entender o cálculo consolidado da matrícula.
  - Deve ser combinada com `iptucalv` quando for necessário relacionar valor venal da edificação com valor monetário de IPTU ou taxas.
  - Não deve substituir `iptucalv` para apurar valor final calculado por receita.
  - Não deve substituir `iptunump` para analisar débito gerado, parcelas ou integração com arrecadação.

- Que perguntas ela responde bem?

  - Qual foi o valor venal calculado de cada construção?
  - Qual foi o valor venal total das construções de uma matrícula?

### Cuidados / riscos

- A chave correta para análise é `j22_anousu, j22_matric, j22_idcons`. Usar apenas `j22_matric` mistura construções e exercícios.
- Uma matrícula pode possuir várias construções calculadas no mesmo exercício.
- Contar linhas da `iptucale` conta construções calculadas, não imóveis.
- Para contar imóveis com edificação calculada, usar `COUNT(DISTINCT j22_matric)`.
- Para obter valor venal edificado total da matrícula, somar `j22_valor` por `j22_anousu, j22_matric`.
- Para obter área edificada calculada total da matrícula, somar `j22_areaed` por `j22_anousu, j22_matric`.
- `j22_areaed` pode divergir de `iptuconstr.j39_area`, pois representa a área usada no cálculo do exercício.
- `j22_valor` é valor venal da edificação, não valor do IPTU lançado.
- `j22_vm2` é parâmetro de cálculo, não valor comercial de mercado.
- `j22_pontos` deve ser interpretado junto com características e regras de cálculo.
- Construções demolidas, alteradas ou incluídas entre exercícios podem afetar comparações 2026 x 2027.
- Construções cadastradas em `iptuconstr` podem não existir em `iptucale` para determinado exercício se não foram calculadas.
- Para explicar aumento do IPTU, cruzar com `iptucalc`, `iptucalv`, `iptuconstr`, `carconstr` e `caracter`.
- Para análise cadastral atual, não usar apenas `iptucale`; validar com `iptuconstr`.
