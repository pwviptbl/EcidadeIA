## orcamento.orcreceita

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_orcreceita_classe.php`

Registra a receita orcamentaria prevista por exercicio, codigo reduzido, fonte e instituicao. A classe liga a receita a tipo de recurso, fonte, instituicao, caracteristica peculiar e, em consultas especificas, ao plano orcamentario, alteracoes de previsao e lancamentos contabeis da receita.

### Estrutura e interpretacao

- **Classe:** `cl_orcreceita`
- **Tabela principal:** `orcreceita`
- **Chave primaria composta:** `o70_anousu`, `o70_codrec`
- **Grau basico:** uma linha por receita orcamentaria reduzida em um exercicio

Campos de negocio confirmados:

- `o70_codfon`: fonte da receita no exercicio
- `o70_codigo`: tipo de recurso em `orctiporec`
- `o70_valor`: valor previsto da receita
- `o70_reclan`: indicador de receita lancada
- `o70_instit`: instituicao dona da receita
- `o70_concarpeculiar`: caracteristica peculiar
- `o70_orcorgao`, `o70_orcunidade`: orgao e unidade, quando informados
- `o70_esferaorcamentaria`: esfera orcamentaria, quando informada

Interpretacao segura:

- `o70_codrec` e o identificador reduzido da receita, nao o codigo estrutural da fonte nem do plano.
- A mesma fonte (`o70_codfon`) pode aparecer em mais de uma receita.
- O valor previsto (`o70_valor`) e a previsao base da receita, nao a arrecadacao realizada.

### Consulta: `sql_query`

- **Objetivo:** Recuperar a receita prevista com enriquecimento institucional, tipo de recurso, complemento de fonte, fonte, caracteristica peculiar e unidade.
- **Status do metodo:** marcado como `@deprecated` para uso de `fonterecurso`.
- **Tabelas:** `orcreceita`, `db_config`, `orctiporec`, `complementofonterecurso`, `orcfontes`, `concarpeculiar`, `cgm`, `db_tipoinstit`, `orcunidade`

```sql
select /* campos dinamicos */
  from orcreceita
       inner join db_config
          on db_config.codigo = orcreceita.o70_instit
       inner join orctiporec
          on orctiporec.o15_codigo = orcreceita.o70_codigo
       inner join complementofonterecurso
          on complementofonterecurso.o200_sequencial = orctiporec.o15_complemento
       inner join orcfontes
          on orcfontes.o57_codfon = orcreceita.o70_codfon
         and orcfontes.o57_anousu = orcreceita.o70_anousu
       inner join concarpeculiar
          on concarpeculiar.c58_sequencial = orcreceita.o70_concarpeculiar
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
       inner join db_tipoinstit
          on db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit
       left join orcunidade
          on orcunidade.o41_unidade = orcreceita.o70_orcunidade
         and orcunidade.o41_orgao = orcreceita.o70_orcorgao
         and orcunidade.o41_anousu = orcreceita.o70_anousu
 where orcreceita.o70_anousu = :exercicio
   and orcreceita.o70_codrec = :codrec
 order by /* ordenacao dinamica */
```

Regras observadas:

- A receita precisa ter instituicao, tipo de recurso, fonte e caracteristica peculiar validos.
- A unidade orcamentaria e opcional.
- O caminho do complemento de fonte vem via `orctiporec.o15_complemento`.

### Consulta: `sql_query2`

- **Objetivo:** Versao atualizada da consulta base, substituindo o caminho antigo pelo cadastro `fonterecurso`.
- **Tabelas adicionais relevantes:** `fonterecurso`

```sql
select /* campos dinamicos */
  from orcreceita
       join db_config on db_config.codigo = orcreceita.o70_instit
       join orctiporec on orctiporec.o15_codigo = orcreceita.o70_codigo
       join fonterecurso
         on fonterecurso.orctiporec_id = orctiporec.o15_codigo
        and fonterecurso.exercicio = orcreceita.o70_anousu
       join complementofonterecurso
         on complementofonterecurso.o200_sequencial = orctiporec.o15_complemento
       join orcfontes
         on orcfontes.o57_codfon = orcreceita.o70_codfon
        and orcfontes.o57_anousu = orcreceita.o70_anousu
       join concarpeculiar
         on concarpeculiar.c58_sequencial = orcreceita.o70_concarpeculiar
       join cgm
         on cgm.z01_numcgm = db_config.numcgm
       join db_tipoinstit
         on db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit
       left join orcunidade
         on o41_unidade = o70_orcunidade
        and o41_orgao = o70_orcorgao
        and o41_anousu = o70_anousu
 where orcreceita.o70_anousu = :exercicio
   and orcreceita.o70_codrec = :codrec
```

Interpretacao segura:

- Quando a pergunta exigir a relacao atual entre receita e fonte de recurso, prefira `sql_query2` em vez de `sql_query`.

### Consulta: `sql_query_file`

- **Objetivo:** Ler apenas a tabela fisica `orcreceita`.

```sql
select /* campos dinamicos */
  from orcreceita
 where orcreceita.o70_anousu = :exercicio
   and orcreceita.o70_codrec = :codrec
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia da receita;
- listar receitas de um exercicio;
- ler o valor previsto sem multiplicacao de joins.

### Consulta: `sql_query_migra`

- **Objetivo:** Consolidar a previsao da receita e os movimentos mensais de `orcreceitaval` para migracao.
- **Tabelas:** `orcreceita`, `orcreceitaval`, `orcfontes`
- **Grau final:** uma linha por exercicio, receita reduzida e fonte

Regras comprovadas:

- Para cada mes, a consulta soma `o71_valor`.
- Quando `o71_coddoc = 100`, o valor entra positivo.
- Para outros documentos, o valor entra negativo.

Interpretacao segura:

- O metodo trata `o71_coddoc = 100` como movimento base e os demais como reversao/ajuste de sinal oposto.
- O resultado separa colunas mensais `jan` a `dez`, alem de `o70_valor` previsto.

### Consulta: `sql_query_plano`

- **Objetivo:** Relacionar a receita orcamentaria ao plano reduzido associado pela fonte.
- **Tabelas:** `orcreceita`, `db_config`, `orctiporec`, `orcfontes`, `conplanoreduz`, `concarpeculiar`

```sql
select /* campos dinamicos */
  from orcreceita
       inner join db_config on db_config.codigo = orcreceita.o70_instit
       inner join orctiporec on orctiporec.o15_codigo = orcreceita.o70_codigo
       inner join orcfontes
          on orcfontes.o57_codfon = orcreceita.o70_codfon
         and orcfontes.o57_anousu = orcreceita.o70_anousu
       inner join conplanoreduz
          on conplanoreduz.c61_codcon = orcfontes.o57_codfon
         and conplanoreduz.c61_anousu = orcfontes.o57_anousu
         and conplanoreduz.c61_instit = orcreceita.o70_instit
       inner join concarpeculiar
          on concarpeculiar.c58_sequencial = orcreceita.o70_concarpeculiar
 where /* filtro dinamico */
```

Cuidados:

- O retorno passa por `analiseQueryPlanoOrcamento($sql)`, entao a SQL final consumida pode ser transformada fora da classe.
- O join usa `orcfontes.o57_codfon = conplanoreduz.c61_codcon`, portanto nao confundir fonte com codigo reduzido da receita.

### Consulta: `sql_query_razao`

- **Objetivo aparente:** listar receitas para o razao da instituicao corrente.
- **Defeito observado:** o metodo monta `$sql2` com os filtros, mas retorna apenas `$sql`.

Impacto:

- filtros por exercicio, receita e `$dbwhere` nao entram na SQL final;
- nao reutilizar esse metodo como receita confiavel sem corrigir o codigo.

### Consulta: `sql_query_atualizacoesprevisao`

- **Objetivo:** recuperar as alteracoes de previsao da receita por suplementacao.
- **Tabelas:** `orcreceita`, `db_config`, `orcfontes`, `orcsuplemrec`, `orcsuplem`, `orcsuplemlan`
- **Regra comprovada:** so retorna receitas que possuem vinculo em `orcsuplemrec`.

Interpretacao segura:

- a receita precisa ter passado por uma atualizacao de previsao ligada a um suplemento (`o46_codsup`).
- o grao pode multiplicar a receita por lancamentos de suplementacao associados ao mesmo suplemento.

### Consulta: `sql_query_dados_receita`

- **Objetivo:** recuperar a receita da instituicao corrente junto do plano orcamentario correspondente a fonte.
- **Tabelas:** `orcreceita`, `db_config`, `orcfontes`, `conplanoorcamento`

Regra comprovada:

- a consulta sempre filtra `db_config.codigo = DB_instit`.
- o vinculo com `conplanoorcamento` usa `orcfontes.o57_codfon = conplanoorcamento.c60_codcon`.

Defeito observado:

- quando `ordem` e informado, o metodo adiciona `order by` antes de concatenar o `where`.
- isso gera SQL invalida se houver filtro montado em `$sql2`.

### Consulta: `sql_queryEstornoReceitaFatoGerador`

- **Objetivo:** localizar receitas com estorno vinculado a fato gerador via abertura de exercicio.
- **Tabelas principais:** `orcreceita`, `conlancamrec`, `conlancamaberturaexercicio`, `aberturaexercicio`, `conlancam`

```sql
select /* campos dinamicos */
  from orcreceita
       inner join conlancamrec
          on conlancamrec.c74_codrec = orcreceita.o70_codrec
         and conlancamrec.c74_anousu = orcreceita.o70_anousu
       inner join conlancamaberturaexercicio
          on conlancamaberturaexercicio.c80_conlancam = conlancamrec.c74_codlan
       inner join aberturaexercicio
          on aberturaexercicio.c81_sequencial =
             conlancamaberturaexercicio.c80_aberturaexercicio
         and aberturaexercicio.c81_estornado = false
       inner join conlancam
          on conlancam.c70_codlan = conlancamrec.c74_codlan
```

Regra comprovada:

- so considera aberturas de exercicio ainda nao estornadas (`c81_estornado = false`).

### Consulta: `sql_query_fonte_desdobramento`

- **Objetivo:** relacionar a receita a seus desdobramentos de fonte.
- **Tabelas:** `orcreceita`, `orcfontes`, `orcfontesdes`

```sql
select /* campos dinamicos */
  from orcreceita
       inner join orcfontes
          on orcfontes.o57_codfon = orcreceita.o70_codfon
         and orcfontes.o57_anousu = orcreceita.o70_anousu
       inner join orcfontesdes
          on orcfontesdes.o60_anousu = orcreceita.o70_anousu
         and orcfontesdes.o60_codfon = orcfontes.o57_codfon
```

### Consulta: `sql_query_validacao_receita`

- **Objetivo:** validar se a receita esta conectada ao plano orcamentario e ao plano contabil derivado.
- **Tabelas principais:** `orcreceita`, `orcfontes`, `conplanoorcamento`, `conplanoorcamentogrupo`, `conplanoconplanoorcamento`, `conplano`, `conplanoreduz`

Interpretacao segura:

- o caminho de validacao e:
  - `orcreceita -> orcfontes`
  - `orcfontes -> conplanoorcamento`
  - opcionalmente `conplanoorcamento -> conplanoorcamentogrupo`
  - opcionalmente `conplanoorcamento -> conplanoconplanoorcamento -> conplano -> conplanoreduz`
- como varios joins sao `left`, ausencia de parte desse encadeamento nao elimina a receita do resultado, apenas sinaliza lacuna de configuracao.

### Consulta: `sql_query_receita`

- **Objetivo:** recuperar a receita com os metadados da fonte.
- **Tabelas:** `orcreceita`, `orcfontes`

Uso seguro:

- listagens simples de receitas por exercicio, fonte, valor previsto e status de lancamento.

### Consulta: `sql_query_receita_planoreceita`

- **Objetivo:** ligar a receita ao cadastro `planoreceita` da uniao por meio do plano orcamentario e da fonte de recurso.
- **Tabelas:** `orcreceita`, `orcfontes`, `conplanoorcamento`, `planoreceitaconplanoorcamento`, `planoreceita`, `orctiporec`, `fonterecurso`

Regra comprovada:

- a consulta exige `planoreceita.uniao = 't'`.
- tambem exige `planoreceita.exercicio = o70_anousu`.

Defeito observado:

- a implementacao adiciona `order by` antes de `group by`.
- portanto, quando os dois parametros sao informados, a SQL montada fica em ordem sintaticamente invalida para Postgres.

### Regras de negocio confirmadas

1. `orcreceita` representa receita prevista, nao arrecadacao realizada.
2. A fonte (`o70_codfon`) e obrigatoria e conduz boa parte dos joins com plano e validacao.
3. O tipo de recurso (`o70_codigo`) pode ser resolvido pelo caminho antigo de complemento ou pelo caminho novo de `fonterecurso`.
4. Atualizacoes de previsao dependem de vinculo em `orcsuplemrec`.
5. Parte das validacoes de receita passa pelo plano orcamentario e, depois, pelo plano contabil derivado.

### Cuidados para consultas do agente

- Para valor arrecadado, nao use `o70_valor`; esse campo e previsao.
- Para receitas simples e atuais, prefira `sql_query2` a `sql_query`.
- Nao reutilize `sql_query_razao` sem corrigir o bug de perda do `where`.
- Nao reutilize `sql_query_dados_receita` com ordenacao e filtro ao mesmo tempo sem reordenar a montagem da SQL.
- Nao reutilize `sql_query_receita_planoreceita` com `order by` e `group by` simultaneos sem corrigir a ordem das clausulas.
