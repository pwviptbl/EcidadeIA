# Departamentos, órgãos, divisões e usuários

> Fonte principal: `/var/www/html/e-cidade-php74/classes/db_db_depart_classe.php`
>
> Classe: `cl_db_depart`
>
> Tabela principal: `db_depart`

## Visão geral

`db_depart` representa os departamentos administrativos cadastrados no e-Cidade. A chave é `coddepto` e cada departamento pertence a uma instituição por meio de `instit`.

A classe não contém relacionamento pai-filho entre departamentos. A estrutura encontrada relaciona o departamento a:

- instituição;
- órgão orçamentário por exercício;
- divisões;
- almoxarifados;
- usuários;
- unidades de saúde.

Campos relevantes:

| Campo | Significado definido pela classe |
|---|---|
| `coddepto` | Código do departamento |
| `descrdepto` | Descrição do departamento |
| `nomeresponsavel` | Nome do responsável |
| `emailresponsavel` | E-mail do responsável |
| `limite` | Data limite |
| `fonedepto` | Telefone do departamento |
| `emaildepto` | E-mail do departamento |
| `faxdepto` | Fax |
| `ramaldepto` | Ramal |
| `instit` | Código da instituição |
| `id_usuarioresp` | Login/usuário responsável |

Na inclusão, somente descrição e instituição são obrigatórias. A data limite e o usuário responsável podem ser nulos.

Defeito de preenchimento observado:

- Em `atualizacampos`, quando `emailresponsavel` ainda está vazio, o valor é lido de `HTTP_POST_VARS["emaildepto"]`.
- Assim, dependendo do formulário, o e-mail do departamento pode ser copiado para o campo do responsável.

## Consulta cadastral completa

### Consulta: `sql_query`

- **Objetivo:** Recuperar o departamento com a instituição, o CGM institucional e o tipo de instituição.
- **Grão esperado:** Uma linha por departamento.

```sql
select /* campos dinâmicos */
  from db_depart
       inner join db_config
          on db_config.codigo = db_depart.instit
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
       inner join db_tipoinstit
          on db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit
 where db_depart.coddepto = :departamento
 order by /* ordenação dinâmica */
```

Regras:

- A instituição, seu CGM e o tipo da instituição são obrigatórios devido aos `inner joins`.
- Um departamento com instituição inconsistente não aparece nessa consulta.
- A associação com `db_usuarios` pelo campo `id_usuarioresp` está comentada na classe. Portanto, esse método não retorna automaticamente os dados do usuário responsável.

### Consulta: `sql_query_file`

Consulta somente `db_depart`:

```sql
select /* campos dinâmicos */
  from db_depart
 where db_depart.coddepto = :departamento
```

É a consulta mais direta para descrição, contatos, instituição, data limite e código do usuário responsável.

## Vigência operacional do departamento

Os métodos da classe não filtram departamentos vigentes automaticamente.

Telas de seleção e transferência aplicam:

```sql
limite is null
or limite >= :data_sessao
```

Interpretação comprovada pelos consumidores:

- `limite is null` mantém o departamento disponível sem prazo final.
- Quando preenchida, a data limite deve ser igual ou posterior a `DB_datausu`.
- Essa é uma regra aplicada pelas telas consumidoras, não uma condição obrigatória de todas as consultas sobre `db_depart`.

Não trate um departamento vencido como excluído. Ele continua cadastrado e pode ser necessário em consultas históricas.

## Departamento e almoxarifado

### Consulta: `sql_query_almox`

```sql
select /* campos dinâmicos */
  from db_depart
       left join db_almoxdepto
         on db_almoxdepto.m92_depto = db_depart.coddepto
       left join db_almox
         on db_almox.m91_codigo = db_almoxdepto.m92_codalmox
 where db_depart.coddepto = :departamento
```

Regras:

- O departamento é preservado mesmo sem almoxarifado vinculado.
- Um departamento pode gerar várias linhas quando estiver relacionado a vários almoxarifados.
- Para contar departamentos, use `count(distinct db_depart.coddepto)`.
- A tela de pesquisa de departamentos/almoxarifados também aplica a regra de data limite.

## Departamento, órgão e divisão

### Consulta: `sql_query_div`

- **Objetivo:** Recuperar departamentos vinculados a órgãos orçamentários e, opcionalmente, suas divisões.
- **Grão:** Uma linha por combinação de departamento, órgão/exercício e divisão.

```sql
select /* campos dinâmicos */
  from db_depart
       inner join db_departorg
          on db_departorg.db01_coddepto = db_depart.coddepto
       inner join orcorgao
          on orcorgao.o40_orgao = db_departorg.db01_orgao
         and orcorgao.o40_anousu = db_departorg.db01_anousu
       left join departdiv
         on departdiv.t30_depto = db_depart.coddepto
       inner join db_config
          on db_config.codigo = db_depart.instit
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
 where db_depart.coddepto = :departamento
```

Regras:

- O vínculo com órgão é obrigatório.
- O exercício do órgão deve ser o mesmo de `db_departorg.db01_anousu`.
- A divisão é opcional.
- Um departamento com várias divisões ou vínculos anuais retorna várias linhas.
- Consumidores filtram `db01_anousu` para obter a estrutura do exercício desejado.
- Há consumidores que filtram `o40_instit` ou `db_depart.instit`; escolha o campo conforme a pergunta, pois um identifica a instituição do órgão e o outro a instituição do departamento.

Não use `count(*)` para contar departamentos nessa consulta. Use `count(distinct db_depart.coddepto)`.

### Consulta: `sql_query_departamento_divisao`

Retorna somente departamentos que possuem divisão:

```sql
select /* campos dinâmicos */
  from db_depart
       inner join departdiv
          on departdiv.t30_depto = db_depart.coddepto
       inner join db_config
          on db_config.codigo = db_depart.instit
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
 where db_depart.coddepto = :departamento
```

É usada no patrimônio/inventário para listar `t30_codigo` e `t30_descr` de cada departamento.

Um departamento sem divisão não aparece. Um departamento com várias divisões retorna uma linha por divisão.

## Departamento e usuário

### Consulta: `sql_query_deptousuario`

```sql
select /* campos dinâmicos */
  from db_depart
       inner join db_config
          on db_config.codigo = db_depart.instit
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
       left join db_depusu
         on db_depusu.coddepto = db_depart.coddepto
        and db_depusu.id_usuario = :usuario
 where /* filtros dinâmicos */
```

Comportamento real:

- O parâmetro do usuário fica na condição do `left join`.
- A consulta preserva todos os departamentos que passam pelo `where`, mesmo quando o usuário não possui vínculo.
- Para identificar os vinculados, verifique se `db_depusu.id_usuario` não é nulo.
- Para retornar somente departamentos do usuário, acrescente `db_depusu.id_usuario = :usuario` no `where` ou use diretamente a entidade de vínculo.

A tela `con1_departamentos.RPC.php` usa esse método para listar todos os departamentos disponíveis e faz outra consulta em `db_depusu` para separar os selecionados.

Essa consulta não deve ser interpretada como autorização automática do usuário sobre todos os departamentos retornados.

## Dados do departamento e instituição

### Consulta: `sql_query_dados_depart`

```sql
select /* campos dinâmicos */
  from db_depart
       inner join db_config
          on db_config.codigo = db_depart.instit
 where db_depart.coddepto = :departamento
```

Objetivo observado:

- recuperar dados institucionais junto do departamento;
- obter, por exemplo, o logo de `db_config` para documentos;
- apoiar cadastros que precisam da instituição associada ao departamento.

A granularidade permanece uma linha por departamento se `db_config.codigo` for único.

## Departamento e unidade de saúde

### Consulta: `sql_query_unidades`

```sql
select /* campos dinâmicos */
  from db_depart
       left join unidades
         on unidades.sd02_i_codigo = db_depart.coddepto
 where db_depart.coddepto = :departamento
```

Regras:

- O código da unidade de saúde é relacionado diretamente ao código do departamento.
- O `left join` preserva departamentos sem unidade de saúde.
- A importação CNES usa essa consulta para obter `sd02_v_cnes` e identificar vínculos existentes.
- A tela geral de departamentos pode excluir unidades de saúde com:

```sql
db_depart.coddepto not in (
  select unidades.sd02_i_codigo
    from unidades
)
```

Não conclua que todo departamento é uma unidade de saúde; somente os que possuem correspondência em `unidades`.

## Órgão do departamento da sessão

### Consulta: `get_orgao`

Retorna o órgão orçamentário do departamento e exercício correntes:

```sql
select orcorgao.o40_descr,
       orcorgao.o40_orgao
  from db_depart
       left join db_departorg
         on db_departorg.db01_coddepto = db_depart.coddepto
       left join orcorgao
         on orcorgao.o40_orgao = db_departorg.db01_orgao
 where db_depart.coddepto = :departamento_sessao
   and orcorgao.o40_anousu = :exercicio_sessao
   and db_departorg.db01_anousu = :exercicio_sessao
```

Parâmetros:

- departamento: `DB_coddepto`;
- exercício: `DB_anousu`.

Retorno:

```text
<código do órgão> - <descrição do órgão>
```

Cuidados:

- Apesar dos `left joins`, os filtros de `orcorgao` e `db_departorg` no `where` eliminam linhas sem vínculo. Na prática, os relacionamentos tornam-se obrigatórios.
- Sem resultado, o método retorna `null`.
- Se houver mais de um órgão para o mesmo departamento e exercício, o método usa apenas a primeira linha sem `order by`.
- O método não filtra explicitamente a instituição.

## Recomendações para consultas do agente

- Use `db_depart.coddepto` como identificador do departamento.
- Sempre considere `db_depart.instit` em consultas multi-instituição.
- Para departamentos operacionais na data atual da sessão, aplique `limite is null or limite >= DB_datausu`.
- Para histórico, não aplique o filtro de limite automaticamente.
- Relacione órgãos por `db_departorg` e sempre informe o exercício.
- Diferencie órgão, departamento e divisão; são entidades distintas.
- Para permissões, a existência de linha em `db_depusu` é o vínculo do usuário. O `left join` de `sql_query_deptousuario` sozinho não concede acesso.
- Para almoxarifados, divisões e órgãos, controle multiplicação de linhas com `distinct` quando a pergunta for sobre departamentos.
- Para unidade de saúde, valide a correspondência em `unidades`; não infira pela descrição do departamento.
- O usuário responsável (`id_usuarioresp`) é diferente dos usuários vinculados em `db_depusu`.
- Campos, filtros e ordenações são concatenados pela classe. Novas consultas devem usar allowlist e parâmetros vinculados.
