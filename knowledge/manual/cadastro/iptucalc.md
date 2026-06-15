# e-Cidade — Cadastro Imobiliário

## Tabela Principal: `iptucalc`

Tabela financeira principal do cálculo de IPTU por exercício e matrícula.

Cada registro representa o resultado principal do cálculo de IPTU de uma matrícula (`j23_matric`) em um exercício (`j23_anousu`).

## Chave primária / chave de negócio

| campo | papel |
|---|---|
| `j23_anousu` | Exercício do cálculo |
| `j23_matric` | Matrícula do imóvel |
| `j23_anousu, j23_matric` | Chave composta do cálculo |

## Colunas

| coluna | tipo | descrição |
|---|---|---|
| `j23_anousu` | int4 | Exercicio |
| `j23_matric` | int4 | Matricula |
| `j23_testad` | float8 | Testada do Calculo |
| `j23_arealo` | float8 | Area Calculada |
| `j23_areafr` | float8 | Area Fracionada |
| `j23_areaed` | float8 | Area Total Edificada |
| `j23_m2terr` | float8 | Valor M2 Terreno |
| `j23_vlrter` | float8 | Valor Venal Terreno |
| `j23_aliq` | float8 | Aliquita do Iptu |
| `j23_vlrisen` | float8 | Valor da Isencao |
| `j23_tipoim` | varchar(1) | Tipo de imposto |
| `j23_manual` | text | Log do calculo |
| `j23_tipocalculo` | int8 | Tipo de calculo |

## Regras operacionais

## Tabelas relacionadas extraídas dos JOINs

| tabela | relação | descrição |
|---|---|---|
| `iptubase` | `iptubase.j01_matric = iptucalc.j23_matric` | Cadastro principal da matrícula/imóvel |
| `lote` | `lote.j34_idbql = iptubase.j01_idbql` | Lote/terreno vinculado ao imóvel |
| `cgm` | `cgm.z01_numcgm = iptubase.j01_numcgm` | Contribuinte/proprietário principal |

## Prefixos identificados

| prefixo | tabela provável | significado |
|---|---|---|
| `j23` | `iptucalc` | Dados financeiros principais do cálculo de IPTU |
| `j01` | `iptubase` | Matrícula/imóvel |
| `j34` | `lote` | Lote/terreno |
| `z01` | `cgm` | Cadastro Geral do Município |

## Operações SQL

### 2. Buscar cálculo por exercício e matrícula, com dados cadastrais


### 3. Buscar cálculo somente na tabela `iptucalc`


### 4. Atualizar cálculo por chave composta


### 5. Excluir cálculo por chave composta


## Perguntas que esta tabela ajuda a responder

- Qual foi o cálculo principal de IPTU de uma matrícula em determinado exercício?
- Qual área de lote foi usada no cálculo?
- Qual área fracionada foi usada?
- Qual área total edificada entrou no cálculo?
- Qual valor de metro quadrado de terreno foi aplicado?
- Qual foi o valor venal territorial calculado?
- Qual alíquota foi aplicada?
- Qual valor de isenção foi considerado?
- O cálculo foi predial ou territorial?
- Qual log/manual do cálculo foi gravado?

## Filtros seguros

| filtro | uso recomendado |
|---|---|
| `j23_anousu = :anousu` | Filtrar exercício |
| `j23_matric = :matricula` | Filtrar imóvel |
| `j23_tipoim = :tipo_imposto` | Separar tipo de imposto |
| `j23_tipocalculo = :tipo_calculo` | Separar modalidade de cálculo |

## Cuidados / riscos

- `iptucalc` representa o cálculo principal do IPTU, mas não detalha todos os valores por imposto/taxa. Para detalhamento por imposto ou taxa, usar tabelas como `iptucalv`.
- `j23_vlrter` é valor venal do terreno; não deve ser confundido automaticamente com valor total do imóvel se houver edificações.
- `j23_areaed` indica área total edificada usada no cálculo, mas detalhes por construção normalmente ficam em tabelas como `iptucale` ou `iptuconstr`.
- `j23_manual` pode conter log textual grande; cuidado ao usar em agrupamentos ou comparações.
- A classe usa SQL concatenado em PHP legado. Para reuso, sempre converter para placeholders parametrizados.
- A chave do cálculo é composta por exercício e matrícula. Consultar só por matrícula pode retornar múltiplos exercícios.

## Uso recomendado para IA

Use `iptucalc` como tabela principal quando a pergunta envolver o resultado cadastral/financeiro principal do cálculo de IPTU por matrícula e exercício.

Para enriquecer a resposta, juntar com:

| objetivo | tabela |
|---|---|
| Dados do imóvel | `iptubase` |
| Dados do lote | `lote` |
| Proprietário principal | `cgm` |
| Detalhamento de valores | `iptucalv` |
| Cálculo por edificação | `iptucale` |
| Construções cadastradas | `iptuconstr` |
| Configuração anual do IPTU | `cfiptu` |
