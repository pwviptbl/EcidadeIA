## orcamento.orcfontes

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_orcfontes_classe.php`

Registra as fontes da receita por exercicio. A classe relaciona cada fonte ao plano orcamentario/contabil, aos desdobramentos de fonte e, em consultas especificas, a receitas previstas e filtros por instituicao.

### Estrutura e interpretacao

- **Classe:** `cl_orcfontes`
- **Tabela principal:** `orcfontes`
- **Chave primaria composta:** `o57_codfon`, `o57_anousu`
- **Grau basico:** uma linha por fonte em um exercicio

Campos de negocio confirmados:

- `o57_fonte`: codigo textual/hierarquico da fonte
- `o57_descr`: descricao da fonte
- `o57_finali`: finalidade da fonte

Interpretacao segura:

- `o57_codfon` e o identificador numerico da fonte no exercicio.
- `o57_fonte` e a representacao textual hierarquica usada nas validacoes de nivel.
- A fonte e reaproveitada por `orcreceita` via `o70_codfon`.

### Consulta: `sql_query`

- **Objetivo:** recuperar a fonte com enriquecimento do plano orcamentario/contabil correspondente.
- **Tabelas:** `orcfontes`, `conplano`, `conclass`, `consistema`
- **Grau do resultado:** uma linha por fonte, desde que o plano correspondente exista

```sql
select /* campos dinamicos */
  from orcfontes
       inner join conplano
          on conplano.c60_codcon = orcfontes.o57_codfon
         and conplano.c60_anousu = orcfontes.o57_anousu
       inner join conclass
          on conclass.c51_codcla = conplano.c60_codcla
       inner join consistema
          on consistema.c52_codsis = conplano.c60_codsis
       inner join conclass as a
          on a.c51_codcla = conplano.c60_codcla
       inner join consistema as b
          on b.c52_codsis = conplano.c60_codsis
 where orcfontes.o57_codfon = :codfon
   and orcfontes.o57_anousu = :exercicio
 order by /* ordenacao dinamica */
```

Cuidados:

- `conclass` e `consistema` entram duas vezes com aliases diferentes sem alterar a chave de join.
- O metodo retorna `analiseQueryPlanoOrcamento($sql)`, entao a SQL final consumida pode ser transformada fora da classe.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `orcfontes`.

```sql
select /* campos dinamicos */
  from orcfontes
 where orcfontes.o57_codfon = :codfon
   and orcfontes.o57_anousu = :exercicio
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia da fonte;
- validar a hierarquia textual de `o57_fonte`;
- listar fontes do exercicio sem multiplicacao por joins de plano.

### Consulta: `sql_query_previsao`

- **Objetivo:** relacionar a fonte ao plano e, opcionalmente, a receitas previstas da instituicao corrente.
- **Tabelas:** `orcfontes`, `conplano`, `conclass`, `consistema`, `orcreceita`
- **Join opcional adicional:** `conplanoorcamentoanalitica` quando `filtraInstit = true`

```sql
select /* campos dinamicos */
  from orcfontes
       inner join conplano
          on conplano.c60_codcon = orcfontes.o57_codfon
         and conplano.c60_anousu = orcfontes.o57_anousu
       inner join conclass on conclass.c51_codcla = conplano.c60_codcla
       inner join consistema on consistema.c52_codsis = conplano.c60_codsis
       inner join conclass as a on a.c51_codcla = conplano.c60_codcla
       inner join consistema as b on b.c52_codsis = conplano.c60_codsis
       left join orcreceita
          on orcreceita.o70_anousu = conplano.c60_anousu
         and orcreceita.o70_codfon = conplano.c60_codcon
         and orcreceita.o70_instit = :instituicao_sessao
       /* opcional:
       inner join conplanoorcamentoanalitica
          on conplanoorcamentoanalitica.c61_codcon = conplano.c60_codcon
         and conplanoorcamentoanalitica.c61_anousu = conplano.c60_anousu
         and conplanoorcamentoanalitica.c61_instit = :instituicao_sessao
       */
```

Regras comprovadas:

- A previsao da receita e opcional por causa do `left join orcreceita`.
- Quando `filtraInstit = true`, a fonte so aparece se tiver vinculo analitico para a instituicao corrente.

### Regra: `db_verifica_fonte_exclusao`

- **Objetivo:** impedir exclusao de uma fonte quando existem fontes filhas abaixo dela.
- **Base:** leitura de `o57_fonte` com `substr(...)` por nivel retornado por `db_le_mae_rec`.

Interpretacao segura:

- a hierarquia e inferida pelo formato textual de `o57_fonte`, nao por tabela de relacionamento pai-filho.
- niveis inferiores sao detectados verificando prefixo comum e sufixo diferente de zeros.
- se houver qualquer fonte filha no exercicio, a exclusao e bloqueada.

### Regra: `db_verifica_fonte`

- **Objetivo:** validar a inclusao de uma fonte nova na hierarquia.
- **Etapas comprovadas:**
  1. Para niveis acima do primeiro, exige que a fonte pai textual (`db_le_mae_rec(..., false)`) exista.
  2. Para niveis intermediarios, bloqueia a inclusao se ja existir fonte filha abaixo daquele ponto.
  3. Niveis extremos (`nivel = 1` e `nivel = 10`) recebem tratamento especial de liberacao.

Cuidados:

- As regras dependem fortemente do formato de `o57_fonte`.
- Nao reinterpretar os niveis sem validar a funcao `db_le_mae_rec`.

### Consulta: `sql_query_desdobramento`

- **Objetivo:** relacionar a fonte ao plano, reduzido institucional, tipo de recurso e desdobramentos de fonte.
- **Tabelas:** `orcfontes`, `conplano`, `conclass`, `consistema`, `conplanoreduz`, `orctiporec`, `orcfontesdes`
- **Parametro de negocio:** `sInstits` define a lista de instituicoes aceitas no `conplanoreduz`

```sql
select /* campos dinamicos */
  from orcfontes
       inner join conplano
          on conplano.c60_codcon = orcfontes.o57_codfon
         and conplano.c60_anousu = orcfontes.o57_anousu
       inner join conclass on conclass.c51_codcla = conplano.c60_codcla
       inner join consistema on consistema.c52_codsis = conplano.c60_codsis
       inner join conclass as a on a.c51_codcla = conplano.c60_codcla
       inner join consistema as b on b.c52_codsis = conplano.c60_codsis
       left join conplanoreduz
          on conplanoreduz.c61_codcon = conplano.c60_codcon
         and conplanoreduz.c61_anousu = conplano.c60_anousu
         and conplanoreduz.c61_instit in (:instituicoes)
       left join orctiporec
          on orctiporec.o15_codigo = conplanoreduz.c61_codigo
       left join orcfontesdes
          on orcfontesdes.o60_codfon = orcfontes.o57_codfon
         and orcfontesdes.o60_anousu = orcfontes.o57_anousu
```

Interpretacao segura:

- O reduzido institucional e opcional.
- O tipo de recurso so aparece quando a fonte conseguiu ser resolvida por `conplanoreduz.c61_codigo`.
- Os desdobramentos de fonte tambem sao opcionais.

### Consulta: `sql_query_fonte_receita`

- **Objetivo:** ligar a fonte diretamente as receitas previstas que a utilizam.
- **Tabelas:** `orcfontes`, `orcreceita`
- **Grau do resultado:** uma linha por combinacao de fonte e receita prevista

```sql
select /* campos dinamicos */
  from orcfontes
       inner join orcreceita
          on orcreceita.o70_codfon = orcfontes.o57_codfon
         and orcreceita.o70_anousu = orcfontes.o57_anousu
 where /* filtro dinamico */
 order by /* ordenacao dinamica */
```

Regra comprovada:

- Uma mesma fonte pode aparecer em varias receitas do mesmo exercicio.

### Regras de negocio confirmadas

1. `orcfontes` e a dimensao base da fonte no exercicio.
2. A relacao com receita prevista ocorre por `orcreceita.o70_codfon = orcfontes.o57_codfon` no mesmo exercicio.
3. A hierarquia funcional da fonte e controlada pelo valor textual de `o57_fonte`.
4. Parte das consultas assume que a fonte tambem existe como conta no plano (`conplano.c60_codcon = o57_codfon`).

### Cuidados para consultas do agente

- Nao confundir `o57_codfon` com `o57_fonte`: um e identificador numerico, o outro e codigo textual hierarquico.
- Para validar previsao, lembre que `sql_query_previsao` usa `left join orcreceita`; ausencia de receita nao elimina a fonte.
- Para responder sobre hierarquia/pai/filho, use as regras de prefixo de `o57_fonte`, nao apenas o codigo numerico.
- `sql_query` e `sql_query_desdobramento` passam por `analiseQueryPlanoOrcamento($sql)`, entao o SQL final pode ser alterado externamente.
