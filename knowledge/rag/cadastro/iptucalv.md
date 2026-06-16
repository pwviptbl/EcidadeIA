## cadastro.iptucalv



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalv`



### Resumo tecnico

- Descricao: Valores gerados no cálculo do IPTU para o imóvel/matrícula por exercício, histórico de cálculo e receita. Registra valores calculados para IPTU, taxas e outros componentes vinculados à matrícula.
- Chave primaria: Nao informada.
- Chave de negocio: j21_anousu, j21_matric, j21_codhis, j21_receit
- Coluna de tempo: j21_anousu
- Grao: Uma linha por exercício, matrícula, histórico de cálculo e receita.
- Recomendada: sim
- Significado da contagem: Conta itens de valor calculado por matrícula, exercício, histórico e receita. Não conta imóveis diretamente. Para contar imóveis com valor gerado, usar `COUNT(DISTINCT j21_matric)` filtrando por exercício e, se necessário, por receita.
- Candidatas a chave de negocio: j21_anousu, j21_matric, j21_codhis, j21_receit
- Candidatas a coluna de tempo: j21_anousu

### Relacionamentos

- `j21_codhis` -> `cadastro.iptucalh` (j17_codhis) [iptucalv_codhis_fk]
- `j21_matric` -> `cadastro.iptubase` (j01_matric) [iptucalv_matric_fk]
- `j21_receit` -> `caixa.tabrec` (k02_codigo) [iptucalv_receit_fk]

### Filtros padrao

- Exercício `j21_anousu = :exercicio`
- Matrícula `j21_matric = :matricula`
- Receita `j21_receit = :receita`
- Histórico `j21_codhis = :codhis`
- Comparação entre exercícios `j21_anousu IN (:exercicio_anterior, :exercicio_atual)`

### Semantica de filtros

- Para total por matrícula, somar `j21_valor` agrupando por `j21_anousu, j21_matric`.
- Para total por receita, somar `j21_valor` agrupando por `j21_anousu, j21_receit`.
- Para comparar anos, comparar a mesma `j21_matric` e, quando necessário, a mesma `j21_receit`.
- Para análise de IPTU puro, é obrigatório identificar quais códigos de `j21_receit` correspondem ao IPTU.
- Para análise de taxas, é obrigatório identificar quais códigos de `j21_receit` correspondem a cada taxa.

### Regra de negocio para enriquecer

- O que esta tabela representa no negocio?

  - Representa os valores detalhados gerados no cálculo do IPTU e de receitas associadas ao imóvel/matrícula, como IPTU, taxa de lixo e outros itens tributários vinculados ao exercício.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

  - Deve ser preferida quando a pergunta envolver valor calculado por receita, soma de IPTU, soma de taxas, composição do valor por matrícula ou comparação financeira entre exercícios.
  - Deve ser usada quando for necessário separar IPTU de taxa de lixo ou de outras receitas.
  - Deve ser preferida sobre `iptucalc` quando o objetivo for analisar valores finais/componentes monetários por receita.
  - Não deve substituir `iptucalc` quando a pergunta for sobre parâmetros do cálculo, como área, testada, alíquota ou valor venal territorial.
  - Não deve substituir `iptunump` quando a pergunta for sobre débito gerado, número do débito, parcelas ou integração com arrecadação.

- Que perguntas ela responde bem?

  - Qual foi o valor calculado de IPTU em determinado exercício?
  - Qual foi o valor calculado de taxa de lixo em determinado exercício?
  - Qual foi o total calculado por matrícula?
  - Qual foi o total calculado por receita?
  - Qual foi o total calculado por histórico?

### Cuidados / riscos

- A tabela pode ter mais de uma linha por matrícula e exercício, pois os valores são detalhados por receita e histórico.
- Contar linhas da `iptucalv` não conta imóveis; conta itens de valor calculado.
- Para contar imóveis com valor gerado, usar `COUNT(DISTINCT j21_matric)`.
- Para somar IPTU corretamente, é necessário filtrar os códigos de receita que representam IPTU.
- Para somar taxa de lixo corretamente, é necessário filtrar os códigos de receita correspondentes à taxa.
- Sem filtro por `j21_receit`, a soma de `j21_valor` pode misturar IPTU, taxas e outros componentes.
- Sem filtro por `j21_anousu`, a soma mistura exercícios diferentes.
- Sem agrupamento correto, uma matrícula pode ser duplicada por possuir várias receitas ou históricos.
- `j21_valor` representa valor calculado, não valor lançado definitivamente, pago ou arrecadado.
- `j21_quant` pode ter significado diferente conforme a receita/histórico. Validar antes de usar como métrica de negócio.
- Para comparação 2026 x 2027, comparar por matrícula e por receita para identificar qual componente causou a variação.
- Matrículas existentes em um ano e ausentes em outro podem representar imóveis novos, baixados, não calculados ou mudanças cadastrais.
- Valores zerados ou negativos devem ser investigados antes de agregações finais.
- Para explicar aumento do IPTU, combinar `iptucalv` com `iptucalc`, pois `iptucalv` mostra o valor, mas `iptucalc` ajuda a explicar os parâmetros do cálculo.
