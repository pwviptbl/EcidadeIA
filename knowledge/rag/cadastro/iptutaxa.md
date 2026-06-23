## cadastro.iptutaxa

> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptutaxa`
> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptutaxa_classe.php`

### Resumo tecnico

- Descricao: cadastro das taxas cobradas junto com o IPTU por exercicio e receita.
- Chave primaria: `j19_anousu`, `j19_receit`
- Chave de negocio: `j19_anousu`, `j19_receit`
- Coluna de tempo: `j19_anousu`
- Grao: uma linha por exercicio e receita de taxa
- Recomendada: sim
- Significado da contagem: conta combinacoes de exercicio e receita cadastradas como taxa de IPTU, nao lancamentos por matricula.
- Candidatas a chave de negocio: `j19_receit`, `j19_valor`
- Candidatas a coluna de tempo: `j19_anousu`

### Relacionamentos

- `j19_receit` -> `caixa.tabrec` (`k02_codigo`) [iptutaxa_receit_fk]
- `tabrec.k02_codjm` -> `tabrecjm.k02_codjm` [observado na consulta da classe]

### Perguntas que esta tabela ajuda a responder

- Quais taxas serao cobradas no exercicio?
- Qual o valor cadastrado para uma receita de taxa em determinado ano?
- Quais receitas do IPTU devem ser tratadas como taxa no calculo?
- Qual a descricao financeira da receita vinculada a uma taxa?

### Filtros e regras reaproveitaveis

#### Filtros padrao

- Exercício: `j19_anousu = :anousu`
- Receita: `j19_receit = :receita`

#### Semantica de filtros

- `j19_anousu` delimita o ano em que a taxa vale.
- `j19_receit` identifica a receita orcamentaria cadastrada em `tabrec`.
- `j19_valor` e o valor da taxa para o exercicio.

### Consulta: `sql_query`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptutaxa_classe.php`
- **Objetivo:** ler a taxa com descricao financeira da receita.
- **Tabelas:** `iptutaxa`, `tabrec`, `tabrecjm`
- **Grau do resultado:** uma linha por exercicio e receita de taxa
- **Parametros:** `j19_anousu`, `j19_receit`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - `tabrec.k02_codigo = iptutaxa.j19_receit` `inner join`
  - `tabrecjm.k02_codjm = tabrec.k02_codjm` `inner join`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio, filtra por exercicio e/ou receita.
  - A consulta exige a receita cadastrada em `tabrec`; sem isso a linha nao aparece.
  - O `tabrecjm` entra como suporte para a classificacao/jm da receita.
- **Campos relevantes:**
  - `j19_anousu`, `j19_receit`, `j19_valor`
  - `k02_codigo`, `k02_drecei`, `k02_codjm`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptutaxa
    inner join tabrec on tabrec.k02_codigo = iptutaxa.j19_receit
    inner join tabrecjm on tabrecjm.k02_codjm = tabrec.k02_codjm
   where /* j19_anousu, j19_receit ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - A consulta e cadastral, nao financeira de arrecadacao efetiva.
  - Como usa `inner join`, taxas sem receita valida em `tabrec` nao entram no resultado.
  - Nao confundir a descricao da receita com o valor da taxa.
- **Evidencia adicional:** usada pelo cadastro de taxas e por consultas que cruzam a tabela com `iptucalv` para separar valores de IPTU e de taxas.

### Consulta: `sql_query_file`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptutaxa_classe.php`
- **Objetivo:** leitura direta da tabela `iptutaxa`.
- **Tabelas:** `iptutaxa`
- **Grau do resultado:** uma linha por exercicio e receita
- **Parametros:** `j19_anousu`, `j19_receit`, `campos`, `ordem`, `dbwhere`
- **Juncoes:** nenhuma
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio, aplica os filtros de exercicio e/ou receita.
  - Nao enriquece com descricao da receita.
- **Campos relevantes:**
  - `j19_anousu`, `j19_receit`, `j19_valor`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptutaxa
   where /* j19_anousu, j19_receit ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Use quando a pergunta for apenas sobre o valor cadastrado da taxa.
  - Para saber a descricao da receita, combine com `tabrec`.

### Regras de manutencao observadas

1. `j19_anousu` e `j19_receit` formam a chave composta da tabela.
2. `j19_valor` e obrigatorio na inclusao.
3. A classe e usada em telas de manutencao de taxa (`func_iptutaxa.php`, `cad1_iptutaxa001.php`, `cad1_iptutaxa002.php`, `cad1_iptutaxa003.php`).
4. O cruzamento com `iptucalv` permite separar valores de IPTU e de taxas no calculo anual.

### Cuidados / riscos

- Nao tratar `iptutaxa` como valor por matricula; a granularidade e por exercicio e receita.
- Nao assumir que toda receita de `tabrec` e taxa de IPTU; ela precisa estar cadastrada nesta tabela.
- `sql_query()` depende de `tabrec` e `tabrecjm`; se a receita estiver inconsistente, o registro some do enriquecimento.
- Em relatórios de cálculo, use `iptutaxa` para identificar quais receitas sao taxa e `iptucalv` para buscar os valores calculados correspondentes.
