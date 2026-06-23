## issqn.issplan

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_issplan_classe.php`

Planilha de retenção na fonte do modulo ISSQN. A classe representa o cabecalho da planilha e serve de base para vincular inscrições, itens da planilha e numeros de arrecadacao gerados no fluxo de retencao.

### Resumo tecnico

- **Classe:** `cl_issplan`
- **Tabela principal:** `issplan`
- **Chave primaria:** `q20_planilha`
- **CGM do contribuinte:** `q20_numcgm`
- **Inscricao vinculada:** `q20_inscr`
- **Ano:** `q20_ano`
- **Mes:** `q20_mes`
- **Nome do contribuinte:** `q20_nomecontri`
- **Telefone do contribuinte:** `q20_fonecontri`
- **Numpre:** `q20_numpre`
- **Numero do banco:** `q20_numbco`
- **Situacao:** `q20_situacao`
- **Grau:** uma linha por planilha.

Interpretacao segura:

- Esta entidade nao e o lancamento tributario em si; ela organiza a planilha que agrupa os lancamentos de retenção.
- O registro funciona como cabecalho e ponto de ancoragem para os itens da planilha e para a relacao com arrecadacao.
- Para contar planilhas, use `COUNT(DISTINCT q20_planilha)`.

### Relacionamentos

- `q20_numcgm -> cgm.z01_numcgm`
- `q20_inscr -> issbase.q02_inscr`
- `q20_planilha -> issplaninscr.q24_planilha`
- `q20_planilha -> issplannumpre.q32_planilha`
- `q20_planilha -> issplanit.q21_planilha`

### Cuidados de schema

- A classe usa `q20_inscr` em consultas e nos relatórios do sistema, mas o atributo nao aparece na lista de propriedades do cabecalho da classe.
- O campo e tratado como parte da visao `issplan` pelos consumidores e por `funcoes/db_func_issplan.php`.
- Se a tarefa envolver escrita ou validacao de schema, confirme essa coluna diretamente no banco ou nas visoes de DDL antes de assumir que o objeto PHP a expõe explicitamente.

### Consultas da classe

#### `sql_query`

- **Objetivo:** ler a planilha com enriquecimento da inscricao e dos CGMs envolvidos.
- **Tabelas:** `issplan`, `issbase`, `cgm` e `cgm as a`
- **Grau do resultado:** uma linha por planilha, desde que a inscricao e os CGMs existam nos cadastros relacionados
- **Juncoes:**
  - `issbase.q02_inscr = issplan.q20_inscr` `inner join`
  - `cgm.z01_numcgm = issplan.q20_numcgm` `inner join`
  - `a.z01_numcgm = issbase.q02_numcgm` `inner join`
- **Filtro padrao:** `issplan.q20_planilha = :planilha`
- **Uso seguro:** consultar cabecalho com contexto do contribuinte e da inscricao.

```sql
select /* campos dinamicos */
  from issplan
 inner join issbase on issbase.q02_inscr = issplan.q20_inscr
 inner join cgm on cgm.z01_numcgm = issplan.q20_numcgm
 inner join cgm as a on a.z01_numcgm = issbase.q02_numcgm
 where issplan.q20_planilha = :planilha;
```

#### `sql_query_file`

- **Objetivo:** leitura fisica direta da tabela `issplan`.
- **Tabelas:** `issplan`
- **Grau do resultado:** uma linha por planilha
- **Juncoes:** nenhuma
- **Uso seguro:** validar o cabecalho da planilha sem depender do cadastro de inscrição.

#### `sql_query_arrecad`

- **Objetivo:** enxergar a planilha junto de seus vínculos e da situacao financeira do `numpre`.
- **Tabelas:** `issplan`, `issplaninscr`, `arrecad`, `arrepaga`
- **Grau do resultado:** uma linha por planilha, podendo multiplicar conforme as linhas associadas em `issplaninscr` ou arrecadacao
- **Juncoes:**
  - `issplaninscr.q24_planilha = issplan.q20_planilha` `left join`
  - `arrecad.k00_numpre = issplan.q20_numpre` `left outer join`
  - `arrepaga.k00_numpre = issplan.q20_numpre` `left outer join`
- **Uso seguro:** conferir a planilha com visao de arrecadacao e o status associado ao numero de arrecadacao.

```sql
select /* campos dinamicos */
  from issplan
  left join issplaninscr on q20_planilha = q24_planilha
  left outer join arrecad on issplan.q20_numpre = arrecad.k00_numpre
  left outer join arrepaga on issplan.q20_numpre = arrepaga.k00_numpre
 where issplan.q20_planilha = :planilha;
```

#### `sql_query_issplaninscr`

- **Objetivo:** listar a planilha com os itens de inscricao e os numeros de arrecadacao vinculados.
- **Tabelas:** `issplan`, `issplaninscr`, `issplannumpre`
- **Grau do resultado:** uma linha por planilha, ampliada pelos vinculos de inscricao e numpre
- **Juncoes:**
  - `q24_planilha = q20_planilha` `left join`
  - `q32_planilha = q20_planilha` `left join`
- **Uso seguro:** montar a visao operacional da planilha com suas inscricoes e numeros de arrecadacao.

### Regras de manutencao observadas

1. `incluir()` exige `q20_numcgm`, `q20_ano`, `q20_mes` e monta `q20_planilha` por sequence quando o valor nao e informado.
2. `q20_numpre`, `q20_numbco` e `q20_situacao` sao normalizados para `0` quando nulos.
3. A classe grava auditoria em `db_acount` para insert, update e delete.
4. `sql_query_file()` e a leitura mais direta quando a visao relacionada estiver inconsistente.

### Perguntas que ela responde bem

- Qual planilha de retencao foi gerada?
- Qual CGM e qual inscricao estao ligados a uma planilha?
- Qual numpre foi associado a uma planilha?
- Qual a situacao financeira da planilha em relacao ao numpre?
- Quais inscricoes e numeros de arrecadacao estao vinculados a uma planilha?

### Cuidados

- Nao confundir `issplan` com o lancamento individual `issplanit`.
- Nao confundir o cabecalho da planilha com o conjunto de itens da planilha ou com a arrecadacao gerada.
- `q20_situacao` e um estado operacional da planilha, nao uma prova isolada de pagamento.
- Se o consumidor depender de `q20_inscr`, valide a origem dessa coluna no schema ou na visao que expõe `issplan`.
