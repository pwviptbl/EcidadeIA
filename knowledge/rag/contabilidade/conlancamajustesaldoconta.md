## contabilidade.conlancamajustesaldoconta

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_conlancamajustesaldoconta_classe.php`

Documenta os ajustes de saldo por conta vinculados a um lancamento contabil, com classificacao orcamentaria complementar por exercicio, funcao, subfuncao, elemento e fonte/receita.

---

### Conceito: ajuste_saldo_conta

- **Classe:** `cl_conlancamajustesaldoconta`
- **Tabela principal:** `contabilidade.conlancamajustesaldoconta`
- **Chave primaria:** `c155_codigo`
- **Campos estruturantes observados na classe:**
  - `c155_conlancam` - codigo do lancamento contabil associado
  - `c155_exercicio` - exercicio da classificacao usada no ajuste
  - `c155_funcao` - funcao orcamentaria
  - `c155_subfuncao` - subfuncao orcamentaria
  - `c155_elemento` - elemento de despesa
  - `c155_ai` - AI
  - `c155_receita` - codigo de receita/fonte usado no ajuste
- **Grao base:** Uma linha por ajuste de saldo registrado para um lancamento.

A tabela nao guarda o valor do lancamento em si. Ela funciona como uma classificacao complementar do ajuste de saldo, apontando para um `conlancam` e detalhando como esse ajuste deve ser identificado na estrutura orcamentaria.

#### Consulta: `sql_query`

- **Objetivo:** Ler o ajuste de saldo com enriquecimento de classificacao orcamentaria.
- **Tabelas:** `conlancamajustesaldoconta`, `orcfuncao`, `orcsubfuncao`, `orcelemento`, `orcfontes`
- **Grau do resultado:** Uma linha por registro de `conlancamajustesaldoconta`, assumindo unicidade dos cadastros auxiliares.
- **Parametros:** `:c155_codigo`, `:campos`, `:ordem`, `:dbwhere`
- **Juncoes:**
  - `orcfuncao.o52_funcao = conlancamajustesaldoconta.c155_funcao`
  - `orcsubfuncao.o53_subfuncao = conlancamajustesaldoconta.c155_subfuncao`
  - `orcelemento.o56_codele = conlancamajustesaldoconta.c155_elemento`
  - `orcelemento.o56_anousu = conlancamajustesaldoconta.c155_exercicio`
  - `orcfontes.o57_codfon = conlancamajustesaldoconta.c155_receita`
  - `orcfontes.o57_anousu = conlancamajustesaldoconta.c155_exercicio`
- **Filtros e regras:**
  - Sem `dbwhere`, o metodo filtra apenas por `c155_codigo` se ele for informado.
  - Todas as tabelas auxiliares entram por `left join`, entao o ajuste continua aparecendo mesmo quando a classificacao nao estiver preenchida ou nao encontrar cadastro correspondente.
- **Campos relevantes:**
  - `c155_conlancam` conecta o ajuste ao lancamento contabil pai, mas este metodo nao faz join com `conlancam`.
  - `c155_receita` e tratada na SQL como chave de `orcfontes`, ou seja, a classe a usa como classificacao por fonte/receita do exercicio.
- **Cuidados:**
  - `orcsubfuncao` e ligada apenas por `o53_subfuncao`, sem amarrar `funcao`; se o cadastro reutilizar o mesmo codigo em contextos diferentes, a interpretacao depende da consistencia do dado.
  - O metodo nao valida instituicao nem relaciona o lancamento a documento contabil, conta reduzida ou conta corrente.
  - `c155_ai` existe na tabela, mas nao e expandido por join nesta classe; trate-o como codigo interno cuja semantica adicional nao foi comprovada aqui.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler somente a tabela `conlancamajustesaldoconta`.
- **Tabelas:** `conlancamajustesaldoconta`
- **Uso pratico:** Base mais segura para auditoria de chaves, confronto de registros e reconstrucao manual dos joins com outras tabelas contabeis.
- **Filtros:** aceita `c155_codigo` direto ou `dbwhere`.

#### Regras operacionais observadas na classe

- `c155_conlancam` e obrigatorio na inclusao; o ajuste sempre nasce vinculado a um lancamento contabil.
- `c155_funcao`, `c155_subfuncao`, `c155_elemento`, `c155_ai` e `c155_receita` sao normalizados para `null` quando vazios no `atualizacampos()`, indicando que a classificacao complementar pode ser parcial.
- O metodo de consulta nao tenta recompor o lancamento contabil nem seu valor; ele apenas descreve a classificacao associada ao ajuste.

#### Cuidados para consultas do agente

- Para entender o evento contabil completo, relacione `c155_conlancam` a `conlancam` e, se necessario, a `conlancamval`, `conlancamdoc` e `conlancaminstit`.
- Para classificacao orcamentaria do ajuste, use o exercicio do proprio ajuste (`c155_exercicio`) nas ligacoes com `orcelemento` e `orcfontes`.
- Nao trate ausencia de `funcao`, `subfuncao`, `elemento` ou `receita` como erro automaticamente; a classe aceita esses campos nulos.
