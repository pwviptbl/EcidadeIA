## orcamento.orcamento

Mapeia as regras de negócio para análise da receita prevista, despesa fixada e dotações orçamentárias (orcdotacao).

---

### Conceitos & Relacionamentos Base
A dotação orçamentária (`orcdotacao`) é a autorização de despesa pública associada a um determinado ano (exercício), órgão, elemento de despesa e função.

- **Dotação:** `orcamento.orcdotacao`
  - `o58_anousu`: Ano/exercício do orçamento.
  - `o58_coddot`: Código reduzido da dotação (Primary Key junto com `o58_anousu`).
  - `o58_valor`: Valor fixado da dotação (Orçamento inicial previsto para a despesa).
- **Órgão e Unidade:** `orcamento.orcorgao` e `orcamento.orcunidade`
  - `orcdotacao.o58_orgao = orcorgao.o40_orgao` E `orcdotacao.o58_anousu = orcorgao.o40_anousu`
  - `orcdotacao.o58_unidade = orcunidade.o41_unidade` E `orcdotacao.o58_orgao = orcunidade.o41_orgao` E `orcdotacao.o58_anousu = orcunidade.o41_anousu`
- **Elemento de Despesa:** `orcamento.orcelemento`
  - `orcdotacao.o58_codele = orcelemento.o56_codele` E `orcdotacao.o58_anousu = orcelemento.o56_anousu`

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Qual o orçamento total previsto (despesa fixada) para um exercício específico?
- **Descrição:** Retorna a soma de todas as dotações iniciais fixadas para um determinado ano.
- **Receita SQL:**
```sql
SELECT SUM(o58_valor) as total_orcamento
FROM orcamento.orcdotacao
WHERE o58_anousu = :ano;
```

#### 2. Quais órgãos possuem as maiores dotações orçamentárias previstas no ano?
- **Descrição:** Lista os órgãos governamentais (`orcorgao`) classificados pelo valor total sob sua gestão no ano.
- **Receita SQL:**
```sql
SELECT 
    org.o40_orgao as codigo_orgao, 
    org.o40_descr as nome_orgao, 
    SUM(dot.o58_valor) as valor_total_orcado
FROM orcamento.orcdotacao dot
JOIN orcamento.orcorgao org ON dot.o58_orgao = org.o40_orgao AND dot.o58_anousu = org.o40_anousu
WHERE dot.o58_anousu = :ano
GROUP BY org.o40_orgao, org.o40_descr
ORDER BY valor_total_orcado DESC;
```

---

### Consultas extraídas de `db_orcdotacao_classe.php`

#### Consulta: `sql_query`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_orcdotacao_classe.php`
- **Objetivo:** Montar a visão mais completa da dotação com instituição, classificação funcional, programa, projeto/atividade, elemento, fonte, característica peculiar, localizador de gasto e produto.
- **Tabelas:** `orcdotacao`, `db_config`, `orctiporec`, `complementofonterecurso`, `orcfuncao`, `orcsubfuncao`, `orcprograma`, `orcelemento`, `orcprojativ`, `orcorgao`, `orcunidade`, `concarpeculiar`, `ppasubtitulolocalizadorgasto`, `cgm`, `db_tipoinstit`, `orcproduto`
- **Grau do resultado:** Uma linha por dotação em `orcdotacao`, assumindo unicidade dos cadastros auxiliares por chave.
- **Parâmetros:** `:o58_anousu`, `:o58_coddot`, `:campos`, `:ordem`, `:dbwhere`
- **Junções principais:**
  - `db_config.codigo = orcdotacao.o58_instit`
  - `orctiporec.o15_codigo = orcdotacao.o58_codigo`
  - `orctiporec.o15_complemento = complementofonterecurso.o200_sequencial`
  - `orcprograma.(o54_anousu, o54_programa) = (orcdotacao.o58_anousu, orcdotacao.o58_programa)`
  - `orcelemento.(o56_anousu, o56_codele) = (orcdotacao.o58_anousu, orcdotacao.o58_codele)`
  - `orcprojativ.(o55_anousu, o55_projativ) = (orcdotacao.o58_anousu, o58_projativ)`
  - `orcorgao.(o40_anousu, o40_orgao) = (orcdotacao.o58_anousu, o58_orgao)`
  - `orcunidade.(o41_anousu, o41_orgao, o41_unidade) = (orcdotacao.o58_anousu, o58_orgao, o58_unidade)`
- **Filtros e regras:**
  - Sem `dbwhere`, o método filtra por exercício e/ou código reduzido da dotação.
  - `complementofonterecurso` entra por `left join`, então nem toda dotação precisa ter complemento de fonte preenchido.
- **Cuidados:**
  - O método não entra em `fonterecurso`; ele descreve o cadastro da dotação, não valida a fonte no catálogo anual normalizado.
  - O alias adicional `orcorgao as a` repete o órgão da unidade e tende a ser usado apenas para exposição de campos.

#### Consulta: `sql_query2`

- **Objetivo:** Igual a `sql_query`, mas forçando fonte de recurso válida no exercício via `fonterecurso`.
- **Tabelas adicionais:** `fonterecurso`
- **Regra principal:** A dotação só aparece se `fonterecurso.orctiporec_id = orctiporec.o15_codigo` e `fonterecurso.exercicio = orcdotacao.o58_anousu`.
- **Diferença de negócio:** Use esta versão quando a pergunta exigir a fonte anual efetivamente cadastrada para o exercício; `sql_query` aceita a dotação mesmo sem esse vínculo.
- **Cuidado:** Aqui `complementofonterecurso` vira `join` obrigatório, então dotações sem complemento ficam de fora.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler somente `orcdotacao`, sem expandir joins.
- **Uso prático:** Auditoria de chaves (`o58_anousu`, `o58_coddot`), conferência de valores brutos e base segura para agregações próprias.

#### Consulta: `sql_query_ele`

- **Objetivo:** Listar dotações com foco em elemento de despesa e tipo de recurso.
- **Tabelas:** `orcdotacao`, `db_config`, `orcelemento`, `orctiporec`
- **Regras:**
  - Por padrão, restringe `db_config.codigo = db_getsession("DB_instit")`.
  - Se `geracaoEmpenhoFolha = true`, remove essa trava institucional no join de `db_config`.
- **Cuidados:**
  - Esse método é útil para telas e rotinas que precisam escolher dotação dentro da instituição logada.
  - A quebra dessa trava em `geracaoEmpenhoFolha` sugere uso especial em rotinas centralizadas de folha.

#### Consulta: `sql_query_autoriza`

- **Objetivo:** Relacionar dotação com a estrutura de departamentos e usuários autorizados.
- **Tabelas:** `orcdotacao`, `db_config`, `orctiporec`, `orcfuncao`, `orcsubfuncao`, `orcprograma`, `orcprojativ`, `orcelemento`, `orcorgao`, `orcunidade`, `db_departorg`, `db_depart`, `db_depusu`, `db_usuarios`
- **Junções de autorização:**
  - `db_departorg.(db01_anousu, db01_orgao, db01_unidade) = (orcdotacao.o58_anousu, orcorgao.o40_orgao, orcunidade.o41_unidade)`
  - `db_depart.coddepto = db_departorg.db01_coddepto`
  - `db_depusu.coddepto = db_depart.coddepto`
  - `db_usuarios.id_usuario = db_depusu.id_usuario`
- **Regra de negócio:** A dotação é conectada à cadeia órgão/unidade e, a partir daí, aos departamentos e usuários associados para autorização operacional.
- **Cuidados:** Uma mesma dotação pode multiplicar linhas por usuário autorizado; para contar dotações, use `distinct o58_coddot, o58_anousu`.

#### Consulta: `sql_query_dotacao`

- **Objetivo:** Retornar uma visão simplificada da dotação da instituição logada, com elemento, projeto/atividade e tipo de recurso.
- **Tabelas:** `orcdotacao`, `db_config`, `orcelemento`, `orcprojativ`, `orctiporec`
- **Regra principal:** O join com `db_config` impõe `db_config.codigo = db_getsession("DB_instit")`.
- **Uso prático:** Base compacta para seleção de dotação dentro da instituição corrente.

#### Consulta: `sql_query_dotacao_finalidade`

- **Objetivo:** Expor a finalidade SICONFI associada à dotação.
- **Tabelas:** `orcdotacao`, `siconfidotacaofinalidade`
- **Junções:**
  - `siconfidotacaofinalidade.(c119_coddot, c119_anousu) = (orcdotacao.o58_coddot, orcdotacao.o58_anousu)`
- **Regra:** O vínculo é `left join`, então a dotação pode existir sem finalidade SICONFI cadastrada.
- **Uso prático:** Identificar cobertura ou ausência de classificação de finalidade exigida para prestação de contas.

#### Consulta: `sql_recurso`

- **Objetivo:** Resolver a fonte de recurso anual da dotação.
- **Tabelas:** `orcdotacao`, `orctiporec`, `fonterecurso`, `complementofonterecurso`
- **Junções:**
  - `orctiporec.o15_codigo = orcdotacao.o58_codigo`
  - `fonterecurso.orctiporec_id = orctiporec.o15_codigo`
  - `fonterecurso.exercicio = orcdotacao.o58_anousu`
  - `complementofonterecurso.o200_sequencial = orctiporec.o15_complemento`
- **Regra de negócio:** A fonte usada pela dotação depende do cadastro de `orctiporec`, mas a validação anual está em `fonterecurso`.

#### Consulta: `sql_dotacao_planodespesa`

- **Objetivo:** Ligar a dotação ao plano de despesa e ao plano orçamentário contábil.
- **Tabelas:** `orcdotacao`, `orcelemento`, `conplanoorcamento`, `planodespesaconplanoorcamento`, `planodespesa`, `orcprojativ`, `orcfuncao`, `orcsubfuncao`, `orctiporec`, `fonterecurso`
- **Junções principais:**
  - `conplanoorcamento.(c60_codcon, c60_anousu) = (orcelemento.o56_codele, orcelemento.o56_anousu)`
  - `planodespesaconplanoorcamento.conplanoorcamento_codigo = conplanoorcamento.c60_codigo`
  - `planodespesa.id = planodespesaconplanoorcamento.planodespesa_id`
  - `planodespesa.exercicio = conplanoorcamento.c60_anousu`
  - `planodespesa.uniao = :utilizaPlanoUniao`
  - `fonterecurso.orctiporec_id = orctiporec.o15_codigo`
  - `fonterecurso.exercicio = o58_anousu`
- **Parâmetros adicionais:** `:groupBy`, `:utilizaPlanoUniao`
- **Regra de negócio:** A associação ao plano de despesa depende do elemento contábil/orçamentário e pode ser filtrada pelo plano da União ou não.
- **Cuidados:**
  - O método aceita `group by` dinâmico; a agregação correta depende do grão escolhido por quem chama.
  - Como passa por tabelas de relacionamento, uma dotação pode aparecer em mais de uma linha se houver múltiplos mapeamentos de plano.

#### Cuidados para consultas do agente

- Para total de despesa fixada, a base mais segura continua sendo `orcdotacao` puro ou `sql_query_file`.
- Quando a pergunta exigir fonte de recurso válida no exercício, prefira receitas baseadas em `sql_query2` ou `sql_recurso`, não apenas `sql_query`.
- Consultas com autorização (`sql_query_autoriza`) e plano de despesa (`sql_dotacao_planodespesa`) alteram bastante a cardinalidade; não some `o58_valor` sem deduplicar a dotação.
