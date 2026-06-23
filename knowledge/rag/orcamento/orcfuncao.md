## orcamento.orcfuncao

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_orcfuncao_classe.php`

Cadastro das funcoes do orcamento. A classe mantem a dimensao basica da funcao orcamentaria, com descricao, codigo do tribunal, finalidade e codigo Siconfi, e serve de referencia para dotacoes, PPA e impactos orcamentarios.

### Estrutura e interpretacao

- **Classe:** `cl_orcfuncao`
- **Tabela principal:** `orcfuncao`
- **Chave primaria:** `o52_funcao`
- **Grau basico:** uma linha por funcao orcamentaria

Campos de negocio confirmados:

- `o52_funcao`: codigo da funcao do orcamento
- `o52_descr`: descricao da funcao
- `o52_codtri`: codigo do tribunal
- `o52_finali`: finalidade textual da funcao
- `o52_siconfi`: codigo Siconfi usado na matriz de saldo contabil

Interpretacao segura:

- `o52_funcao` e a chave numerica da funcao, reutilizada por tabelas como `orcdotacao`.
- `o52_descr` e o rotulo operacional da funcao para exibicao e filtros.
- `o52_finali` guarda texto livre de finalidade e pode estar mais detalhado que a descricao curta.
- `o52_codtri` e `o52_siconfi` sao codigos regulatorios/integração, nao descricoes de negocio.

### Consulta: `sql_query`

- **Objetivo:** ler o cadastro de funcoes diretamente da tabela `orcfuncao`.
- **Tabelas:** `orcfuncao`

```sql
select /* campos dinamicos */
  from orcfuncao
 where orcfuncao.o52_funcao = :funcao
 order by /* ordenacao dinamica */
```

Comportamento observado:

- Se `o52_funcao` nao for informado, a consulta pode listar varias funcoes.
- Se `dbwhere` for informado, ele substitui o filtro simples por codigo.
- Nao ha joins nem enriquecimento adicional no proprio metodo.

### Consulta: `sql_query_file`

- **Objetivo:** ler a tabela fisica `orcfuncao`.
- **Tabelas:** `orcfuncao`

```sql
select /* campos dinamicos */
  from orcfuncao
 where orcfuncao.o52_funcao = :funcao
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia de uma funcao;
- obter descricao, finalidade e codigos regulatorios sem multiplicacao de joins;
- listar o cadastro base de funcoes do orcamento.

### Regras de manutencao observadas

1. `incluir()` exige `o52_descr`, `o52_codtri` e `o52_siconfi`.
2. `o52_finali` e opcional na inclusao e alteracao.
3. Inclusao, alteracao e exclusao registram auditoria em `db_acount*` quando a sessao nao desativa account.

### Relacionamentos de negocio confirmados no catalogo

- `orcdotacao.o58_funcao -> orcfuncao.o52_funcao`
- `orcimpacto.o90_funcao -> orcfuncao.o52_funcao`
- `orcimpactomov.o63_funcao -> orcfuncao.o52_funcao`
- `orcparamfunc.o45_func -> orcfuncao.o52_funcao`
- `orcppa.o23_funcao -> orcfuncao.o52_funcao`
- `ppadotacao.o08_funcao -> orcfuncao.o52_funcao`

Interpretacao segura:

- `orcfuncao` funciona como dimensao classificatoria reutilizada por varias estruturas orcamentarias.
- Para perguntas sobre dotacao por funcao, o caminho mais direto costuma passar por `orcdotacao.o58_funcao`.

### Cuidados para consultas do agente

- Nao inferir exercicio a partir de `orcfuncao`: a tabela em si nao tem coluna de tempo.
- Para recortes anuais ou valores, a funcao precisa ser combinada com tabelas como `orcdotacao`, `orcppa` ou `orcimpacto`.
- `sql_query` e `sql_query_file` sao equivalentes na pratica nesta classe; ambos leem apenas `orcfuncao`.
