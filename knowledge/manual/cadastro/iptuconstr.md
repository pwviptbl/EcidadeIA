# e-Cidade — Cadastro Imobiliário

## Resumo

Arquivo de referência extraído da classe PHP `cl_iptuconstr`, entidade `iptuconstr`, módulo `cadastro`.

A tabela `iptuconstr` representa as construções/edificações vinculadas a uma matrícula imobiliária. Cada construção é identificada pela composição `j39_matric + j39_idcons` e guarda dados físicos, endereço da construção, datas de lançamento/demolição, origem, pavimento, observações e indicação de construção principal.

---

## 1. Tabela principal  `cl_iptuconstr`

### `iptuconstr`

| Campo | Tipo | Descrição |
|---|---:|---|
| `j39_matric` | `int4` | Matrícula |
| `j39_idcons` | `int4` | Código da construção |
| `j39_ano` | `int4` | Ano da construção |
| `j39_area` | `float8` | Área da construção em m² |
| `j39_areap` | `float8` | Área privada da construção em m² |
| `j39_dtlan` | `date` | Data de inclusão/lançamento |
| `j39_codigo` | `int4` | Código do logradouro |
| `j39_numero` | `int4` | Número do imóvel/construção |
| `j39_compl` | `varchar(20)` | Complemento |
| `j39_dtdemo` | `date` | Data de demolição |
| `j39_codprotdemo` | `varchar(40)` | Processo de protocolo da demolição |
| `j39_idaument` | `int4` | Origem da construção |
| `j39_idprinc` | `bool` | Indica se é construção principal |
| `j39_pavim` | `int4` | Pavimento |
| `j39_obs` | `text` | Observações |

### Chave lógica


A classe trata `j39_matric + j39_idcons` como identificador do registro nas operações de inclusão, alteração, exclusão e consulta direta.

---

### Parâmetro de validação do ano

A classe carrega parâmetros de `cadastro.cfiptu` no construtor:


Quando `j18_validarano = 'f'`, a propriedade `validar_j39_ano` é ativada, exigindo que `j39_ano` seja informado com 4 caracteres.

---

## 3. Tabelas e objetos relacionados

### Relacionamentos diretos nas consultas

| Tabela/View | Ligação extraída | Uso |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = iptuconstr.j39_matric` | Matrícula base do imóvel. |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Dados territoriais do lote. |
| `cgm` | `cgm.z01_numcgm = iptubase.j01_numcgm` | Proprietário principal da matrícula. |
| `ruas` | `ruas.j14_codigo = iptuconstr.j39_codigo` | Logradouro da construção. |
| `ruastipo` | `ruastipo.j88_codigo = ruas.j14_tipo` | Tipo do logradouro. |
| `carconstr` | `carconstr.j48_matric = iptuconstr.j39_matric` e `carconstr.j48_idcons = iptuconstr.j39_idcons` | Características da construção. |
| `proprietario_nome` | `proprietario_nome.j01_matric = carconstr.j48_matric` | Nome do proprietário associado à matrícula. |
| `caracter` | `caracter.j31_codigo = carconstr.j48_caract` | Característica da construção. |
| `cargrup` | `cargrup.j32_grupo = caracter.j31_grupo` | Grupo da característica. |
| `cadastro.cfiptu` | `cfiptu.j18_anousu = DB_anousu` | Parâmetros de validação do cadastro/cálculo do IPTU. |

### Relações usadas na exclusão geral

| Entidade | Filtro usado |
|---|---|
| `iptucaleold` | `j162_matric = :matricula and j162_idcons = :id_construcao` |
| `carconstr` | `j48_matric = :matricula and j48_idcons = :id_construcao` |
| `constrcar` | `j53_matric = :matricula and j53_idcons = :id_construcao` |
| `iptucale` | `j22_matric = :matricula and j22_idcons = :id_construcao` |
| `constrescr` | `j52_matric = :matricula and j52_idcons = :id_construcao` |
| `issmatric` | `q05_matric = :matricula and q05_idcons = :id_construcao` |
| `iptuconstrdemo` | `matricula + idcons` |
| `iptuconstrpontos` | `j83_matric = :matricula and j83_idcons = :id_construcao` |

---

## 4. Métodos relevantes

| Método | Finalidade |
|---|---|
| `__construct()` | Inicializa rótulos da entidade `iptuconstr`, página de retorno e parâmetros de `cfiptu`. |
| `getParametros()` | Consulta `cadastro.cfiptu` para configurar a validação do ano da construção. |
| `erro($mostra, $retorna)` | Exibe mensagens de erro/sucesso em JavaScript. |
| `atualizacampos($exclusao = false)` | Atualiza propriedades a partir de `HTTP_POST_VARS`; monta datas de lançamento e demolição. |
| `incluir($j39_matric, $j39_idcons)` | Insere construção. |
| `alterar($j39_matric = null, $j39_idcons = null)` | Atualiza construção. |
| `excluir($j39_matric = null, $j39_idcons = null, $dbwhere = null)` | Remove construção por chave ou filtro customizado. |
| `sql_record($sql)` | Executa query e atualiza `numrows`. |
| `sql_query(...)` | Consulta construção com matrícula base, lote, CGM, ruas e tipo de rua. |
| `sql_query_file(...)` | Consulta direta na tabela `iptuconstr`. |
| `excluirGeral(...)` | Remove construção e registros dependentes em cascata lógica. |
| `sql_query_proprietario_nome(...)` | Consulta construção com características e proprietário. |
| `sql_query_update_area($iMatric, $iIdCons, $iArea)` | Retorna SQL para atualizar a área da construção. |

---

## Regras operacionais recorrentes
### 5.1 Buscar construção por matrícula e código da construção


### 5.2 Buscar todas as construções de uma matrícula


### 5.3 Buscar construções ativas de uma matrícula

Construções ativas são as que não possuem data de demolição.


### 5.4 Buscar construção com dados do imóvel, lote, proprietário e logradouro


### 5.5 Somar área construída ativa por matrícula


### 5.6 Somar área privada ativa por matrícula


### 5.7 Buscar construção principal da matrícula


### 5.8 Buscar construções demolidas


### 5.9 Buscar construções por logradouro


### 5.10 Buscar características da construção e proprietário

Baseado em `sql_query_proprietario_nome`.


### 5.11 Atualizar área da construção

Baseado em `sql_query_update_area`.


### 5.12 Verificar construções com ano inválido

Útil quando a parametrização exige ano com 4 dígitos.


---

## 6. Convenção de prefixos

| Prefixo | Tabela provável | Observação |
|---|---|---|
| `j39_` | `iptuconstr` | Construções da matrícula. |
| `j01_` | `iptubase` | Cadastro base do imóvel. |
| `j34_` | `lote` | Dados do lote. |
| `z01_` | `cgm` | Cadastro geral municipal. |
| `j14_` | `ruas` | Logradouro. |
| `j88_` | `ruastipo` | Tipo de logradouro. |
| `j48_` | `carconstr` | Características da construção. |
| `j31_` | `caracter` | Características cadastrais. |
| `j32_` | `cargrup` | Grupos de características. |
| `j18_` | `cfiptu` | Parâmetros do IPTU por exercício. |

---

## 7. Perguntas que esta classe ajuda a responder

- Quais construções existem para determinada matrícula?
- Qual é a área construída ativa de um imóvel?
- Qual construção é a principal?
- Uma construção foi demolida? Quando?
- Qual logradouro/número/complemento está vinculado à construção?
- Qual o ano de construção, pavimento e origem da construção?
- Quais características estão vinculadas à construção?
- Quais registros dependem da construção antes de uma exclusão?

---

## 8. Filtros seguros e recomendados

| Cenário | Filtro recomendado |
|---|---|
| Construção específica | `j39_matric = :matricula and j39_idcons = :id_construcao` |
| Todas as construções da matrícula | `j39_matric = :matricula` |
| Construções ativas | `j39_dtdemo is null` |
| Construções demolidas | `j39_dtdemo is not null` |
| Construção principal | `j39_idprinc = 't'` |
| Por logradouro | `j39_codigo = :codigo_logradouro` |
| Por número | `j39_numero = :numero` |

---

## 9. Cuidados e riscos

- A classe concatena valores diretamente em SQL; ao reutilizar as consultas fora do padrão legado, usar parâmetros/bind variables.
- `j39_idprinc` é tratado como texto booleano (`'t'`/`'f'`).
- `j39_dtdemo is null` deve ser considerado o principal indicador de construção ativa.
- A exclusão direta em `excluir()` remove apenas `iptuconstr`; para remoção com dependências, a classe disponibiliza `excluirGeral()`.
- `excluirGeral()` executa uma cascata lógica em várias classes; qualquer falha interrompe o processo.
- A validação do ano depende de `cadastro.cfiptu.j18_validarano` para o exercício da sessão.
- O texto original apresenta caracteres acentuados corrompidos em alguns rótulos; este arquivo normaliza os nomes para facilitar uso por IA.
