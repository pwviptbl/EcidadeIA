## orcamento.orctiporec

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_orctiporec_classe.php`

Cadastro dos tipos de recurso do orcamento. A classe representa o eixo legado que liga recurso, estrutura, complemento, campos LOA e, nas consultas derivadas, conecta o recurso a dotacoes, receitas, convenios, conta corrente e ao modelo novo de `fonterecurso`.

### Estrutura e interpretacao

- **Classe:** `cl_orctiporec`
- **Tabela principal:** `orctiporec`
- **Chave primaria:** `o15_codigo`
- **Grau basico:** uma linha por tipo de recurso

Campos de negocio confirmados:

- `o15_codigo`: codigo do recurso
- `o15_descr`: descricao do recurso
- `o15_codtri`: codigo do tribunal
- `o15_finali`: finalidade textual do recurso
- `o15_tipo`: tipo do recurso
- `o15_datalimite`: data limite, quando existir
- `o15_db_estruturavalor`: estrutura vinculada
- `o15_codigosiconfi`: codigo Siconfi legado
- `o15_loaidentificadoruso`: identificador de uso na LOA
- `o15_loatipo`: tipo da LOA
- `o15_loagrupo`: grupo da LOA
- `o15_loaespecificacao`: especificacao da LOA
- `o15_complemento`: complemento da fonte de recurso
- `o15_recurso`: representacao textual do recurso

Interpretacao segura:

- `orctiporec` e o cadastro central legado do recurso usado em dotacao e receita.
- `o15_complemento` conecta o tipo de recurso ao detalhamento de `complementofonterecurso`.
- Parte dos campos LOA e Siconfi coexistem aqui mesmo no modelo antigo, mas varias instalacoes tambem usam `fonterecurso` como camada nova.

### Consulta: `sql_query`

- **Objetivo:** recuperar o tipo de recurso com enriquecimento da estrutura de cadastro.
- **Tabelas:** `orctiporec`, `db_estruturavalor`, `db_estrutura`

```sql
select /* campos dinamicos */
  from orctiporec
       left join db_estruturavalor
         on db_estruturavalor.db121_sequencial = orctiporec.o15_db_estruturavalor
       left join db_estrutura
         on db_estrutura.db77_codestrut = db_estruturavalor.db121_db_estrutura
 where orctiporec.o15_codigo = :codigo
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta base para entender o recurso no modelo legado.
- O join com estrutura ajuda a resolver a hierarquia/cadastro estrutural do recurso.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `orctiporec`.

```sql
select /* campos dinamicos */
  from orctiporec
 where orctiporec.o15_codigo = :codigo
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia do recurso;
- ler somente os campos gravados na tabela.

### Consulta: `sql_queryComplemento`

- **Objetivo:** enriquecer o tipo de recurso com estrutura e complemento de fonte.
- **Tabelas:** `orctiporec`, `db_estruturavalor`, `db_estrutura`, `complementofonterecurso`

Interpretacao segura:

- Use quando a pergunta depender do complemento legado da fonte.
- O metodo expõe o caminho antigo de detalhamento do recurso.

### Consulta: `sql_query_convenios`

- **Objetivo:** localizar recursos vinculados a convenios em uma data ou intervalo.
- **Tabelas:** `orctiporec`, `orctiporecconvenio`

Regras observadas:

- considera vigencia normal e prorrogacao;
- quando so `sDataini` e informado, verifica se a data cai dentro da vigencia ou prorrogacao;
- quando ha intervalo, verifica cobertura completa do periodo.

### Consulta: `sql_query_conveniosGestao`

- **Objetivo:** localizar recursos de convenio já cruzados com a fonte de gestao atual.
- **Tabelas:** `orctiporec`, `orctiporecconvenio`, `fonterecurso`, `complementofonterecurso`

Regras observadas:

- usa a mesma logica de vigencia/prorrogacao dos convenios;
- ainda filtra `fonterecurso.exercicio = DB_anousu`.

Interpretacao segura:

- Este e o ponto de transicao entre o recurso legado e a camada nova de fonte por exercicio.

### Consulta: `sql_query_emp`

- **Objetivo:** ligar o recurso a dotacoes e empenhos que o utilizam.
- **Tabelas:** `orctiporec`, `orcdotacao`, `empempenho`

Interpretacao segura:

- Serve para responder sobre empenhos associados a um recurso especifico.
- O caminho passa por `orcdotacao.o58_codigo = o15_codigo`.

### Consulta: `sql_query_orcamento`

- **Objetivo:** listar recursos usados no orcamento corrente da sessao, tanto na despesa quanto na receita.
- **Tabelas:** `orctiporec`, `orcdotacao`, `orcreceita`

Regras observadas:

- faz `union` entre recursos presentes em `orcdotacao` e em `orcreceita`;
- usa `DB_anousu` e `DB_instit` da sessao para ambos os lados.

Interpretacao segura:

- E um atalho para "recursos ativos no orçamento do exercício/instituição corrente".

### Consultas tematicas adicionais

Metodos principais:

- `sql_recurso_despesa`
- `sql_query_contacorrentedetalhe`
- `sql_query_complemento`
- `sql_query_especificacao_sem_complemento`
- `sql_recurso_receita`
- `sql_query_fonte_recurso`
- `sqlNovaFonteRecurso`

Leituras de negocio confirmadas:

- `sql_recurso_despesa` liga recurso a `orcdotacao`;
- `sql_query_contacorrentedetalhe` liga recurso a `contacorrentedetalhe`;
- `sql_query_complemento` e `sql_query_especificacao_sem_complemento` tentam filtrar por LOA/especificacao e contexto de dotacao;
- `sql_recurso_receita` liga recurso a `orcreceita`;
- `sql_query_fonte_recurso` usa `complementofonterecurso`;
- `sqlNovaFonteRecurso` cruza `orctiporec` com `fonterecurso` e `complementofonterecurso`.

Cuidados observados no codigo:

- `sql_recurso_despesa` monta `where = {$sWhere}`, o que sugere defeito sintatico se usado literalmente.
- `sql_query_complemento` e `sql_query_especificacao_sem_complemento` referenciam `o15_loaspecificacao`, enquanto o campo da classe e `o15_loaespecificacao`; trate isso como ponto de atencao.
- `sql_query_fonte_recurso` e `sqlNovaFonteRecurso` checam a variavel `$ed161_codigo` em vez de `$o15_codigo`, entao o filtro por codigo pode nao entrar como esperado.

### Regras de manutencao observadas

1. `incluir()` exige `o15_descr`, `o15_codtri`, `o15_finali`, `o15_tipo` e `o15_db_estruturavalor`.
2. `o15_datalimite` pode ser nulo.
3. Campos LOA podem ser normalizados para `null`.
4. Quando `o15_codigo` nao e informado, a classe usa a sequence `orctiporec_o15_codigo_seq`.
5. Se o codigo informado for maior que o ultimo valor da sequence, a inclusao e bloqueada.

### Relacionamentos de negocio confirmados no ecossistema

- `orctiporec -> orcdotacao` via `o58_codigo`
- `orctiporec -> orcreceita` via `o70_codigo`
- `orctiporec -> fonterecurso` via `fonterecurso.orctiporec_id`
- `orctiporec -> complementofonterecurso` via `o15_complemento`

Interpretacao segura:

- `orctiporec` e a ponte entre orçamento legado e o modelo mais novo de fonte de recurso.
- Em perguntas sobre despesa/receita por recurso, este costuma ser o ponto de entrada correto.

### Cuidados para consultas do agente

- Nao confundir `orctiporec` com `fonterecurso`: o primeiro e o cadastro legado central; o segundo e o versionamento novo por exercicio.
- Para perguntas sobre complemento antigo, use os métodos com `complementofonterecurso`.
- Para perguntas sobre fonte atual/gestao, prefira cruzar com `fonterecurso`.
- Para filtros por especificacao LOA, revise o SQL gerado pela classe porque ha sinais de typo no nome do campo.
