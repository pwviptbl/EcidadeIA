# e-Cidade — Cadastro Imobiliário 

## Resumo

A classe `cl_cfiptu` representa os parâmetros do cadastro imobiliário/IPTU por exercício. A tabela principal é `cfiptu`, usando `j18_anousu` como chave de exercício. Ela concentra configurações usadas no cálculo do IPTU, vencimentos, receitas territorial e predial, parâmetros de certidão de isenção, regras de área privativa, fracionamento por lote, validação de proprietário, validação de ano da construção, simulação de cálculo, taxas separadas e parâmetros de recálculo.

Use esta referência quando precisar entender quais parâmetros controlam o comportamento do cadastro imobiliário e do cálculo de IPTU em determinado exercício.

## Tabela principal `cfiptu`

| Tabela | Chave principal | Descrição |
|---|---:|---|
| `cfiptu` | `j18_anousu` | Parâmetros anuais do IPTU/cadastro imobiliário. |

## Colunas da tabela

| Campo | Tipo | Descrição |
|---|---|---|
| `j18_anousu` | `int4` | Exercício |
| `j18_vlrref` | `float8` | Valor Referência |
| `j18_dtoper` | `date` | Data Operação |
| `j18_rterri` | `int4` | Receita Territorial |
| `j18_rpredi` | `int4` | Receita Predial |
| `j18_vencim` | `int4` | Tabela de Vencimento |
| `j18_logradauto` | `bool` | Código do Logradouro Automático |
| `j18_segundavia` | `int4` | Segunda Via |
| `j18_infla` | `varchar(5)` | Código do Inflator |
| `j18_utilizasetfisc` | `bool` | Utiliza Setor Fiscal |
| `j18_testadanumero` | `bool` | Utiliza Número na Testada |
| `j18_excconscalc` | `bool` | Excluir Construção do Cálculo |
| `j18_textoprom` | `varchar(20)` | Texto Promitente |
| `j18_calcvenc` | `int4` | Perguntar Vencimentos Durante Cálculo |
| `j18_utilizaloc` | `bool` | Utilizar Informações de Localização |
| `j18_permvenc` | `int4` | Permite Escolher Vencimentos Durante Cálculo |
| `j18_utidadosdiver` | `bool` | Utiliza Dados Diversos no Cálculo |
| `j18_dadoscertisen` | `int4` | Dados da Certidão de Isenção |
| `j18_formatsetor` | `int4` | Permite Digitar para Setor |
| `j18_formatquadra` | `int4` | Permite Digitar para Quadra |
| `j18_formatlote` | `int4` | Permite Digitar para o Lote |
| `j18_utilpontos` | `int4` | Utilizar Pontuação por Construção |
| `j18_ordendent` | `int4` | Ordem no Endereço de Entrega |
| `j18_iptuhistisen` | `int8` | Código do histórico de isenção |
| `j18_db_sysfuncoes` | `int4` | Código Função |
| `j18_tipoisen` | `int4` | Código da Isenção |
| `j18_perccorrepadrao` | `float8` | Percentual de Correção |
| `j18_templatecertidaoexitencia` | `int4` | Documento Template |
| `j18_templatecertidaoisencao` | `int4` | Template Certidão Isenção |
| `j18_receitacreditorecalculo` | `int4` | Receita de Crédito |
| `j18_tipodebitorecalculo` | `int4` | Tipo de Débito |
| `j18_taxaseparada` | `int4` | Calcular Taxas Separadas |
| `j18_permitectmcgf` | `bool` | Permite consultar CTM com Matric na CGF |
| `j18_bicmarcasigilo` | `bool` | BIC marca emissão de dados sigilosos |
| `j18_utilizaareaprivativa` | `bool` | Utiliza Área Privativa |
| `j18_fracionaidbql` | `bool` | Fraciona por Idbql |
| `j18_validarano` | `bool` | Permite construção sem ano |
| `j18_validaproprietario` | `bool` | Valida proprietário |
| `j18_desvinculadebitosaverbacao` | `bool` | Desvincula débitos com averbação |
| `j18_mostraareairregular` | `bool` | Mostra área irregular no CTM |
| `j18_caracterirregular` | `varchar(40)` | Características de área irregular |
| `j18_simulacaocalculo` | `bool` | Habilita simulação do cálculo de IPTU |
| `j18_func_separa_taxa` | `int4` | Função separa taxa |
| `j18_grupotipoconstr` | `int4` | Grupo Tipo da Construção |
| `j18_modelocapaiptu` | `integer` | Modelo de Capa IPTU |
| `j18_usa_caract_matricula` | `bool` | Usa Características da Matrícula |

## Métodos relevantes

| Método | Finalidade |
|---|---|
| `__construct()` | Inicializa rótulos da tabela `cfiptu` e página de retorno. |
| `erro($mostra, $retorna)` | Exibe mensagem de erro/sucesso e opcionalmente redireciona. |
| `atualizacampos($exclusao = false)` | Carrega dados de `HTTP_POST_VARS`; em exclusão carrega apenas `j18_anousu`. |
| `incluir($j18_anousu)` | Insere um conjunto de parâmetros para o exercício. |
| `alterar($j18_anousu = null)` | Atualiza dinamicamente os campos informados para o exercício. |
| `excluir($j18_anousu = null, $dbwhere = null)` | Exclui parâmetros por exercício ou por condição customizada. |
| `sql_record($sql)` | Executa uma consulta e atualiza `numrows`. |
| `sql_query(...)` | Consulta principal com joins de apoio para isenção, receita, inflator, função, templates e tipo de débito. |
| `sql_query_file(...)` | Consulta direta apenas na tabela `cfiptu`. |
| `getParametrosCadastroImobiliario($iAnoUsu = null)` | Retorna objetos de parâmetros do cadastro imobiliário, opcionalmente por exercício. |
| `sql_query_param(...)` | Consulta parametrizada simplificada com joins para `tipoisen`, `inflan` e `db_sysfuncoes`. |
| `verificaReceitasInvalidas($iAnousu)` | Verifica se receitas/taxas do exercício possuem data limite inválida. |
| `verificaReceitaCreditoRecalculo($iAnousu, $sCampos = "*")` | Consulta a receita de crédito configurada para recálculo. |
| `verificaTipoDebitoRecalculo($iAnousu, $sCampos = "*", $iCadTipo = 7)` | Consulta o tipo de débito configurado para recálculo. |
| `verificaProcedenciaDebitoRecalculo($iAnousu, $sCampos = "*")` | Consulta a procedência/histórico/receita do tipo de débito de recálculo. |

## Regras de inclusão

A inclusão exige, entre outros, valor de referência, data de operação, receitas territorial e predial, tabela de vencimento, inflator, parâmetros de cálculo/localização/certidão, função, tipo de isenção, taxa separada, marcação de sigilo, permissão de CTM/CGF e uso de área privativa.

Campos com default aplicado antes da inclusão:

| Campo | Default |
|---|---|
| `j18_validarano` | `'f'` |
| `j18_validaproprietario` | `'t'` |
| `j18_desvinculadebitosaverbacao` | `'f'` |
| `j18_mostraareairregular` | `'f'` |
| `j18_simulacaocalculo` | `'f'` |
| `j18_func_separa_taxa` | `null` |
| `j18_usa_caract_matricula` | `null` |
| `j18_templatecertidaoexitencia` | `null` |
| `j18_templatecertidaoisencao` | `null` |
| `j18_receitacreditorecalculo` | `null` |
| `j18_tipodebitorecalculo` | `null` |
| `j18_perccorrepadrao` | `0` |
| `j18_fracionaidbql` | `false` |
| `j18_caracterirregular` | `''` |

## Relacionamentos identificados

| Origem | Destino | Uso |
|---|---|---|
| `cfiptu.j18_tipoisen` | `tipoisen.j45_tipo` | Tipo de isenção padrão. |
| `cfiptu.j18_infla` | `inflan.i01_codigo` | Inflator/correção. |
| `cfiptu.j18_db_sysfuncoes` | `db_sysfuncoes.codfuncao` | Função configurada. |
| `cfiptu.j18_iptuhistisen` | `iptucalh.j17_codhis` | Histórico de isenção. |
| `cfiptu.j18_receitacreditorecalculo` | `tabrec.k02_codigo` | Receita de crédito de recálculo. |
| `cfiptu.j18_tipodebitorecalculo` | `arretipo.k00_tipo` | Tipo de débito de recálculo. |
| `db_documentotemplate.db82_sequencial` | `cfiptu.j18_templatecertidaoexitencia` | Template de documento. |
| `arretipo.k03_tipo` | `cadtipo.k03_tipo` | Tipo cadastral do débito. |
| `arretipo.k00_taxaespecifica` | `tabdesc.codsubrec` | Taxa específica. |
| `tabrec.k02_codjm` | `tabrecjm.k02_codjm` | Juros/multa da receita. |
| `tabrec.k02_tabrectipo` | `tabrectipo.k116_sequencial` | Tipo da receita. |
| `iptucadtaxaexe.j08_tabrec` | `tabrec.k02_codigo` | Receita de taxa por exercício, usada em validação. |

## Consultas SQL base

### Parâmetros do exercício

```sql
select *
  from cfiptu
 where j18_anousu = :anousu;
```

### Consulta principal com relacionamentos

```sql
select *
  from cfiptu
 inner join tipoisen on tipoisen.j45_tipo = cfiptu.j18_tipoisen
 left join tabrec on tabrec.k02_codigo = cfiptu.j18_receitacreditorecalculo
 inner join inflan on inflan.i01_codigo = cfiptu.j18_infla
 left join arretipo on arretipo.k00_tipo = cfiptu.j18_tipodebitorecalculo
 inner join db_sysfuncoes on db_sysfuncoes.codfuncao = cfiptu.j18_db_sysfuncoes
 left join iptucalh on iptucalh.j17_codhis = cfiptu.j18_iptuhistisen
 where cfiptu.j18_anousu = :anousu;
```

### Verificar receitas inválidas do exercício

```sql
select tabrec.k02_codigo,
       tabrec.k02_descr,
       tabrec.k02_limite as limite_receita_principal,
       juros.k02_limite as limite_receita_juros,
       multa.k02_limite as limite_receita_multa
  from tabrec
  left join tabrec juros on juros.k02_codigo = tabrec.k02_recjur
  left join tabrec multa on multa.k02_codigo = tabrec.k02_recmul
 where tabrec.k02_codigo in (
       select j08_tabrec from iptucadtaxaexe where j08_anousu = :anousu
       union
       select j18_rterri from cfiptu where j18_anousu = :anousu
       union
       select j18_rpredi from cfiptu where j18_anousu = :anousu
 )
   and (
       tabrec.k02_limite < (:anousu || '-01-01')::date
       or juros.k02_limite < (:anousu || '-01-01')::date
       or multa.k02_limite < (:anousu || '-01-01')::date
   );
```

### Receita de crédito do recálculo

```sql
select *
  from cfiptu
 inner join tabrec on j18_receitacreditorecalculo = k02_codigo
 where j18_anousu = :anousu;
```

### Tipo de débito do recálculo

```sql
select *
  from cfiptu
 inner join arretipo on j18_tipodebitorecalculo = k00_tipo
 inner join cadtipo on arretipo.k03_tipo = cadtipo.k03_tipo
 where j18_anousu = :anousu
   and cadtipo.k03_tipo = :cad_tipo;
```

## Perguntas que esta tabela ajuda a responder

- Quais receitas territorial e predial estão configuradas para o exercício?
- O cálculo utiliza setor fiscal, localização, área privativa, fracionamento por lote ou pontuação por construção?
- O sistema permite construção sem ano?
- O sistema valida proprietário?
- O exercício possui simulação de cálculo habilitada?
- Qual histórico de isenção é usado?
- Quais receita e tipo de débito são usados no recálculo?
- As receitas configuradas possuem data limite válida para o exercício?

## Cuidados e riscos

- A classe monta SQL por concatenação; filtros como `$dbwhere`, `$campos` e `$ordem` devem ser controlados para evitar injeção de SQL.
- Vários campos booleanos são armazenados como `'t'`/`'f'`, não como boolean nativo da linguagem.
- `j18_fracionaidbql` pode receber string `'false'` em inclusão, enquanto outros booleanos usam `'t'`/`'f'`; validar comportamento no banco.
- `j18_usa_caract_matricula` pode ser tratado como `null` sem aspas na inclusão; revisar se a coluna aceita nulo.
- Alterações usam SQL dinâmico e dependem de `HTTP_POST_VARS`/`$_POST`, o que pode gerar comportamento diferente conforme origem dos dados.

## Resumo para IA

`cfiptu` é a tabela central de parâmetros anuais do IPTU/cadastro imobiliário. A chave é `j18_anousu`. Ela define receitas, vencimentos, inflator, regras de cálculo, certidões, isenção, área privativa, fracionamento, simulação, validação de ano/proprietário, área irregular, taxas separadas e parâmetros de recálculo. Consultar esta tabela antes de interpretar cálculo de IPTU, geração de débitos, certidões de isenção e regras de cadastro imobiliário por exercício.
