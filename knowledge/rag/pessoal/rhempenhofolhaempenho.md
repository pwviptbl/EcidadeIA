## pessoal.rhempenhofolhaempenho

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_rhempenhofolhaempenho_classe.php`

Vinculo entre a folha de pessoal e o empenho gerado para ela. Esta classe nao descreve a folha nem o empenho em si; ela guarda apenas a amarracao folha -> numemp.

### Resumo tecnico

- **Classe:** `cl_rhempenhofolhaempenho`
- **Tabela principal:** `rhempenhofolhaempenho`
- **Chave primaria:** `rh76_sequencial`
- **Folha de origem:** `rh76_rhempenhofolha`
- **Numero do empenho:** `rh76_numemp`
- **Grão:** uma linha por vinculo entre folha e empenho

Interpretacao segura:

- A tabela e a ponte operacional para localizar qual empenho foi gerado por uma folha.
- Nao usar `rh76_numemp` como se fosse o empenho geral sem considerar a folha de origem.
- Para a folha completa, consultar `pessoal.rhempenhofolha`; para o empenho geral, consultar `empenho.empempenho`.

### Relacionamentos

- `rh76_rhempenhofolha -> rhempenhofolha.rh72_sequencial`
- `rh76_numemp -> empenho.empempenho.e60_numemp`

### Consulta: `sql_query`

- **Objetivo:** recuperar o vinculo com contexto da folha, do empenho e de classificacoes orcamentarias.
- **Tabelas:** `rhempenhofolhaempenho`, `empempenho`, `rhempenhofolha`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`, `orctiporec`, `orcelemento`, `orcprojativ`, `orcunidade`
- **Grau do resultado:** uma linha por vinculo folha x empenho, podendo desaparecer se algum join obrigatorio nao existir
- **Juncoes principais:**
  - `empempenho.e60_numemp = rhempenhofolhaempenho.rh76_numemp` `inner join`
  - `rhempenhofolha.rh72_sequencial = rhempenhofolhaempenho.rh76_rhempenhofolha` `inner join`
  - `cgm.z01_numcgm = empempenho.e60_numcgm` `inner join`
  - `db_config.codigo = empempenho.e60_instit` `inner join`
  - `orcdotacao.o58_anousu = empempenho.e60_anousu and o58_coddot = empempenho.e60_coddot` `inner join`
  - `pctipocompra.pc50_codcom = empempenho.e60_codcom` `inner join`
  - `emptipo.e41_codtipo = empempenho.e60_codtipo` `inner join`
  - `concarpeculiar.c58_sequencial = empempenho.e60_concarpeculiar` `inner join`
  - `orctiporec.o15_codigo = rhempenhofolha.rh72_recurso` `inner join`
  - `orcelemento.o56_codele = rhempenhofolha.rh72_codele and o56_anousu = rh72_anousu` `inner join`
  - `orcprojativ.o55_anousu = rhempenhofolha.rh72_anousu and o55_projativ = rh72_projativ` `inner join`
  - `orcunidade.o41_anousu = rhempenhofolha.rh72_anousu and o41_orgao = rh72_orgao and o41_unidade = rh72_unidade` `inner join`
  - `orcdotacao a.o58_anousu = rhempenhofolha.rh72_coddot and a.o58_coddot = rhempenhofolha.rh72_anousu` `inner join`

```sql
select /* campos dinamicos */
  from rhempenhofolhaempenho
 inner join empempenho on empempenho.e60_numemp = rhempenhofolhaempenho.rh76_numemp
 inner join rhempenhofolha on rhempenhofolha.rh72_sequencial = rhempenhofolhaempenho.rh76_rhempenhofolha
 /* demais joins orcamentarios e cadastrais */
 where rhempenhofolhaempenho.rh76_sequencial = :sequencial;
```

### Consulta: `sql_query_file`

- **Objetivo:** leitura fisica direta do vinculo.
- **Tabelas:** `rhempenhofolhaempenho`
- **Grau do resultado:** uma linha por vinculo
- **Uso seguro:** confirmar persistencia do relacionamento folha -> empenho sem depender de joins.

### Regras de manutencao observadas

1. `incluir()` exige `rh76_rhempenhofolha` e `rh76_numemp`.
2. Quando `rh76_sequencial` nao e informado, a classe usa a sequence `rhempenhofolhaempenho_rh76_sequencial_seq`.
3. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.

### Perguntas que ela responde bem

- Qual empenho foi vinculado a uma folha?
- Qual folha originou um numero de empenho?
- Existe algum vinculo persistido entre folha e empenho para este sequencial?

### Cuidados

- Nao tratar essa tabela como folha nem como empenho completo.
- O join com o empenho e a folha e propositalmente restritivo; se um cadastro relacionado faltar, a consulta analitica pode nao retornar a linha.
- Para visão operacional de empenho da folha, combine esta nota com [`pessoal.rhempenhofolha`](/home/dbseller/Modelos/MVP/knowledge/rag/pessoal/rhempenhofolha.md).
