## orcamento.fonterecurso

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_fonterecurso_classe.php`

Versiona a fonte de recurso por exercicio. A classe liga o tipo de recurso do e-Cidade (`orctiporec`) a classificacao, gestao, codigo Siconfi, detalhamento e descricao textual usados no modelo mais novo de fontes.

### Estrutura e interpretacao

- **Classe:** `cl_fonterecurso`
- **Tabela principal:** `fonterecurso`
- **Chave primaria:** `id`
- **Grau basico:** uma linha por versao de fonte de recurso em um exercicio

Campos de negocio confirmados:

- `id`: identificador da fonte versionada
- `orctiporec_id`: codigo do recurso em `orctiporec`
- `exercicio`: exercicio da vigencia da fonte
- `codigo_siconfi`: codigo Siconfi no exercicio
- `gestao`: codigo/identificador da fonte na gestao
- `classificacaofr_id`: classificacao da fonte
- `tipo_detalhamento`: detalhamento da fonte
- `descricao`: descricao textual da fonte

Interpretacao segura:

- `fonterecurso` e a camada mais nova de mapeamento de fonte por exercicio.
- `orctiporec_id` ancora a fonte no cadastro legado de tipo de recurso.
- `gestao`, `codigo_siconfi`, `classificacaofr_id` e `tipo_detalhamento` enriquecem a fonte para regras atuais e integrações externas.

### Consulta: `sql_query`

- **Objetivo:** recuperar a fonte de recurso com enriquecimento do tipo de recurso, classificacao e estrutura associada.
- **Tabelas:** `fonterecurso`, `orctiporec`, `classificacaofr`, `db_estruturavalor`

```sql
select /* campos dinamicos */
  from fonterecurso
       join orctiporec
         on orctiporec.o15_codigo = fonterecurso.orctiporec_id
       join classificacaofr
         on classificacaofr.id = fonterecurso.classificacaofr_id
       join db_estruturavalor
         on db_estruturavalor.db121_sequencial = orctiporec.o15_db_estruturavalor
 where fonterecurso.id = :id
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta principal para resolver a fonte já no modelo novo.
- O join com `db_estruturavalor` sugere que a estrutura do tipo de recurso ainda importa para exibicao e validacao.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `fonterecurso`.

```sql
select /* campos dinamicos */
  from fonterecurso
 where fonterecurso.id = :id
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar existencia da fonte versionada;
- ler somente os campos gravados sem joins adicionais.

### Consulta: `sqlFonteRecruso`

- **Objetivo:** variante da consulta enriquecida incluindo o complemento da fonte de recurso.
- **Tabelas:** `fonterecurso`, `orctiporec`, `complementofonterecurso`, `classificacaofr`, `db_estruturavalor`

```sql
select /* campos dinamicos */
  from fonterecurso
       join orctiporec
         on orctiporec.o15_codigo = fonterecurso.orctiporec_id
       join complementofonterecurso
         on complementofonterecurso.o200_sequencial = orctiporec.o15_complemento
       join classificacaofr
         on classificacaofr.id = fonterecurso.classificacaofr_id
       join db_estruturavalor
         on db_estruturavalor.db121_sequencial = orctiporec.o15_db_estruturavalor
 where fonterecurso.id = :id
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Apesar do nome do metodo estar escrito como `sqlFonteRecruso`, o objetivo e enriquecer a fonte com o complemento legado.
- Use esta variante quando a analise precisar cruzar a fonte nova com o caminho antigo de `complementofonterecurso`.

### Regras de manutencao observadas

1. `incluir()` exige `orctiporec_id`, `gestao`, `classificacaofr_id`, `tipo_detalhamento` e `descricao`.
2. `exercicio` nulo e normalizado para `0`.
3. `codigo_siconfi` nulo e normalizado para string vazia.
4. Quando `id` nao e informado, a classe usa a sequence `fonterecurso_id_seq`.
5. Se o `id` informado for maior que o ultimo valor da sequence, a inclusao e bloqueada.

### Relacionamentos de negocio confirmados no catalogo

- `fonterecurso.orctiporec_id -> orctiporec.o15_codigo`
- `fonterecurso.classificacaofr_id -> classificacaofr.id`

Interpretacao segura:

- O eixo principal de negocio e `fonterecurso -> orctiporec`.
- A classificacao complementa a semantica da fonte para uso fiscal/gerencial.

### Relacionamentos semanticos relevantes

- `fonterecurso -> orcdotacao` via `orctiporec.o15_codigo = orcdotacao.o58_codigo`
- `fonterecurso -> fontesiconfi` via `classificacaofr`

Interpretacao segura:

- Para responder perguntas sobre dotacoes por fonte no modelo novo, o caminho natural passa por `orctiporec`.
- Para integrações ou relatórios Siconfi, a classificacao da fonte tambem e parte central.

### Cuidados para consultas do agente

- Nao confundir `fonterecurso` com `orcfontes`: a primeira e o versionamento novo por exercicio, a segunda e a fonte legacy ligada ao plano/conta.
- Se a pergunta mencionar "fonte de recurso atual" ou "gestao/codigo Siconfi", prefira `fonterecurso`.
- Se a pergunta exigir compatibilidade com consultas antigas, pode ser necessario cruzar `fonterecurso` com `orctiporec` e `complementofonterecurso`.
