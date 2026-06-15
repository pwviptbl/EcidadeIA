# e-Cidade — Cadastro Imobiliário 

## Resumo

- Classe analisada: `cl_iptubase`
- Tabela principal: `iptubase`
- Domínio funcional: Cadastro Imobiliário
- Foco da classe: manutenção cadastral de matrículas imobiliárias, vínculos com lote, proprietário, endereço, construção, registro imobiliário e consultas auxiliares para localização e titularidade.
- Operações principais: consultas SQL.

---

## Tabela Principal: `iptubase`

Cadastro de matrículas de imóveis no IPTU. Cada registro representa uma matrícula imobiliária. A matrícula (`j01_matric`) é a chave principal para vincular lote, proprietário, construções, cálculo, endereço de entrega, baixas e dados de registro imobiliário.

| Coluna | Tipo | Descrição |
|---|---:|---|
| `j01_matric` | int4 | **PK** — Matrícula do imóvel |
| `j01_numcgm` | int4 | **FK lógica** → `cgm.z01_numcgm` — CGM do contribuinte/proprietário principal |
| `j01_idbql` | int4 | **FK lógica** → `lote.j34_idbql` — lote vinculado à matrícula |
| `j01_baixa` | date | Data de baixa da matrícula. `NULL` indica matrícula ativa |
| `j01_codave` | int4 | Código da averbação |
| `j01_fracao` | float8 | Fração ideal da matrícula |
| `j01_tipoproprietario` | int4 | Tipo do proprietário. Relaciona com `tipoproprietario.j163_tipoproprietario` |
| `j01_tipoimovel` | int4 | Tipo de imóvel |
| `j01_distrito` | char(4) | Distrito |
| `j01_hectare` | float8 | Área em hectares para imóvel rural |
| `j01_situcad` | varchar(50) | Situação cadastral |
| `j01_datacad` | date | Data de cadastro |
| `j01_processo` | int4 | Processo relacionado |
| `j01_incra` | int4 | Inscrição INCRA |
| `j01_descrlocal` | varchar(255) | Descrição da localização |
| `j01_unidade` | int8 | Unidade. Default usado pela classe: `1` |
| `j01_areaprivativa` | float8 | Área privativa do lote |
| `j01_fracaoproprietario` | float8 | Fração por proprietário. Default usado pela classe: `100` |

**Sequence:** `iptubase_j01_matric_seq`

Usada na inclusão quando `j01_matric` não é informado. A classe chama `nextval('iptubase_j01_matric_seq')`.

---

## Regras operacionais

## Tabelas Relacionadas

### Pessoas / Entidades

| Tabela | Chave principal / campo | Relação com `iptubase` | Descrição |
|---|---|---|---|
| `cgm` / `protocolo.cgm` | `z01_numcgm` | `j01_numcgm = z01_numcgm` | Cadastro Geral do Município; proprietário principal |
| `propri` | `j42_matric`, `j42_numcgm` | `j42_matric = j01_matric` | Outros proprietários / coproprietários |
| `promitente` | `j41_matric`, `j41_numcgm` | `j41_matric = j01_matric` | Promitentes compradores |
| `imobil` | `j44_matric`, `j44_numcgm` | `j44_matric = j01_matric` | Imobiliárias vinculadas à matrícula |
| `tipoproprietario` | `j163_tipoproprietario` | `j163_tipoproprietario = j01_tipoproprietario` | Tipo do proprietário |
| `tipopromitente` | `j164_promitipo` | `j164_promitipo = j41_promitipo` | Tipo do promitente |
| `tipoproprietariopromitente` | variável | usado em consultas de tipo | Vínculo entre tipos de proprietário e promitente |

### Localização / Lote

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `lote` | `j34_idbql` | `j34_idbql = j01_idbql` | Lote/terreno vinculado à matrícula |
| `bairro` | `j13_codi` | `j13_codi = lote.j34_bairro` | Bairro do lote |
| `setor` | `j30_codi` | `j30_codi = lote.j34_setor` | Setor cadastral/fiscal |
| `zonas` | `j50_zona` | `j50_zona = lote.j34_zona` | Zona de valor |
| `testpri` | `j49_idbql`, `j49_face` | `j49_idbql = j01_idbql` | Testada principal do lote |
| `testada` | `j36_idbql`, `j36_face` | `j36_idbql = j49_idbql` e `j36_face = j49_face` | Testadas do lote |
| `testadanumero` | `j15_idbql`, `j15_face` | `j15_idbql = j36_idbql` e `j15_face = j36_face` | Numeração predial pela testada |
| `face` | `j37_face` | `j37_face = j36_face` | Face de quadra |
| `ruas` | `j14_codigo` | `j14_codigo = j49_codigo` | Logradouro |
| `ruastipo` | `j88_codigo` | `j88_codigo = ruas.j14_tipo` | Tipo do logradouro |
| `loteloc` | `j06_idbql` | `j06_idbql = j01_idbql` | Localização alternativa |
| `setorloc` | `j05_codigo` | `j05_codigo = loteloc.j06_setorloc` | Setor de localização |
| `lotesetorfiscal` | `j91_idbql` | `j91_idbql = j01_idbql` | Setor fiscal do lote |
| `setorfiscal` | `j90_codigo` | `j90_codigo = j91_codigo` | Setores fiscais |
| `loteloteam` / `loteam` | `j34_idbql`, `j34_loteam` | via lote | Loteamentos |

### Construções / Edificações

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptuconstr` | `j39_matric`, `j39_idcons` | `j39_matric = j01_matric` | Construções/edificações da matrícula |
| `iptuant` | `j40_matric` | `j40_matric = j01_matric` | Dados anteriores / referência anterior |
| `carconstr` | `j48_matric`, `j48_idcons`, `j48_caract` | via `iptuconstr` | Características da construção |
| `caracter` | `j31_codigo` | `j31_codigo = j48_caract` | Descrição das características |
| `iptubasecondominio` | `j108_matric` | `j108_matric = j01_matric` | Vínculo da matrícula com condomínio |
| `condominio` | `j107_sequencial` | `j107_sequencial = j108_condominio` | Condomínios |
| `iptubasepredio` | `j109_matric` | `j109_matric = j01_matric` | Vínculo da matrícula com prédio |
| `predio` | `j111_sequencial` | `j111_sequencial = j109_predio` | Prédios |

### Registro de Imóveis / Baixa / Endereço

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptubaseregimovel` | `j04_matric` | `j04_matric = j01_matric` | Dados de registro imobiliário/cartório |
| `setorregimovel` | `j69_sequencial` | `j69_sequencial = j04_setorregimovel` | Setor no registro de imóveis |
| `iptubaixa` | `j02_matric` | `j02_matric = j01_matric` | Baixas da matrícula |
| `iptuender` | `j43_matric` | `j43_matric = j01_matric` | Endereço de entrega/carnê |

### Cálculo IPTU / Arrecadação

| Tabela | Chave principal / campo | Relação | Descrição |
|---|---|---|---|
| `iptucalc` | `j23_anousu`, `j23_matric` | `j23_matric = j01_matric` | Cálculo principal do IPTU por exercício |
| `iptucale` | `j22_anousu`, `j22_matric`, `j22_idcons` | `j22_matric = j01_matric` | Cálculo por edificação |
| `iptucalv` | `j21_anousu`, `j21_matric` | `j21_matric = j01_matric` | Valores calculados por matrícula |
| `iptunump` | `j20_anousu`, `j20_matric` | `j20_matric = j01_matric` | Número de débito/numpre relacionado ao cálculo |
| `cfiptu` | `j18_anousu` | ano da sessão | Configuração anual do IPTU |

### Histórico / Observações

| Tabela | Relação | Descrição |
|---|---|---|
| `histocorrenciamatric` | `ar25_matric = j01_matric` | Ocorrências da matrícula |
| `histocorrencia` | `ar23_sequencial = ar25_histocorrencia` | Descrição da ocorrência |

### Views / fontes auxiliares

| View / Fonte | Uso |
|---|---|
| `proprietario` | Consolida proprietário, imóvel, lote, endereço e construção |
| `proprietario_ender` | Endereço completo do proprietário/matrícula |
| `fc_iptu_fracionalote(matric, anousu, ...)` | Função usada para calcular fração/área proporcional do lote |

---

## Métodos relevantes da classe

| Método | Finalidade |
|---|---|
| `atualizacampos()` | Carrega atributos a partir de `HTTP_POST_VARS` |
| `incluir($j01_matric)` | Insere matrícula em `iptubase` |
| `alterar($j01_matric)` | Atualiza matrícula em `iptubase` |
| `excluir($j01_matric, $dbwhere)` | Exclui matrícula(s) |
| `sql_record($sql)` | Executa consulta e controla erros/numrows |
| `sql_query()` | Consulta completa de `iptubase` com lote, CGM, bairro, setor, zonas e tipo proprietário |
| `sql_query_file()` | Consulta direta em `iptubase` |
| `sql_query_regmovel()` | Consulta ampla com dados de lote, testada, construção, registro e baixa |
| `proprietario_query()` | Consulta na view `proprietario` |
| `sqlmatriculas_setor()` | Busca matrículas por setor |
| `sqlmatriculas_ruas()` | Busca matrículas por rua/número/tipo |
| `sqlmatriculas_nome()` | Busca matrículas por CGM, incluindo proprietário, coproprietário e promitente |
| `sqlmatriculas_nome_numero()` | Busca por CGM com regras distintas de titularidade |
| `sqlmatriculas_imobiliaria()` | Busca matrículas por imobiliária |
| `sqlmatriculas_bairros()` | Busca matrículas por bairro |
| `sqlmatriculas_IDBQL()` | Busca matrícula por lote (`j01_idbql`) |
| `sqlmatriculas_setorQuadra()` | Busca por setor e quadra |
| `sql_query_constr()` | Consulta matrícula com construções |
| `sql_query_enderecoEntrega()` | Consulta endereço de entrega da matrícula |
| `sql_query_area_total()` | Soma área de lotes ativos por setor/quadra/lote |
| `sql_query_area_contruida()` | Soma área construída ativa por matrícula |
| `sql_query_imobiliaria()` | Consulta imobiliária vinculada à matrícula |
| `sql_query_setorfiscal()` | Consulta setor fiscal da matrícula |
| `sql_query_proprietariolote()` | Consulta detalhada de proprietário/lote |
| `sql_query_promitentes()` | Lista promitentes da matrícula |
| `sql_query_proprietarios()` | Lista proprietário principal e, opcionalmente, coproprietários |
| `sql_query_construcoes()` | Consulta construções da matrícula |
| `sql_queryCalculoMatricula()` | Consulta cálculo IPTU da matrícula/ano |
| `consultaDebitosMatricula()` | Consulta débitos relacionados à matrícula |
| `findBydId()` | Busca direta por matrícula |
| `sql_query_area_contruida_lote()` | Soma área construída ativa por lote |
| `sql_query_tipos_promitentes()` | Consulta tipos de promitente da matrícula |
| `sql_query_envolvidos_matricula()` | Consolida proprietário, coproprietários e promitentes |
| `sql_query_buscaOcorrenciasMatricula()` | Busca ocorrências da matrícula |
| `sql_query_informacoesImovel()` | Consulta consolidada de dados do imóvel |
| `sql_query_buscaConstrucoesMatricula()` | Busca construções por matrícula/ano |
| `sql_query_construcoesMatricula()` | Consulta construções da matrícula e permite filtrar códigos de área irregular |

---

## Queries SQL prontas

### 1. Busca completa por matrícula


### 2. Busca simples na tabela principal


### 3. Busca ampla com registro imobiliário, testada, construção e baixa


### 4. Busca por CGM — proprietário principal, coproprietário e promitente


### 5. Busca por imobiliária


### 6. Busca por setor


### 7. Busca por setor e quadra


### 8. Busca por bairro


### 9. Área total de lotes ativos por setor/quadra/lote


### 10. Área construída ativa por matrícula


### 11. Endereço de entrega por proprietário ou filtro customizado


### 12. Promitentes da matrícula


### 13. Proprietário principal e coproprietários


### 14. Cálculo IPTU por matrícula e exercício


### 15. Ocorrências da matrícula


---

## Convenção de prefixos observada

| Prefixo | Tabela / fonte provável |
|---|---|
| `j01_` | `iptubase` |
| `j34_` | `lote` |
| `z01_` | `cgm` / `protocolo.cgm` |
| `j13_` | `bairro` |
| `j30_` | `setor` |
| `j50_` | `zonas` |
| `j49_` | `testpri` |
| `j36_` | `testada` |
| `j15_` | `testadanumero` |
| `j37_` | `face` |
| `j14_` | `ruas` |
| `j88_` | `ruastipo` |
| `j39_` | `iptuconstr` |
| `j40_` | `iptuant` |
| `j41_` | `promitente` |
| `j42_` | `propri` |
| `j44_` | `imobil` |
| `j04_` | `iptubaseregimovel` |
| `j69_` | `setorregimovel` |
| `j06_` | `loteloc` |
| `j05_` | `setorloc` |
| `j02_` | `iptubaixa` |
| `j91_` | `lotesetorfiscal` |
| `j90_` | `setorfiscal` |
| `j43_` | `iptuender` |
| `j23_` | `iptucalc` |
| `j22_` | `iptucale` |
| `j21_` | `iptucalv` |
| `j20_` | `iptunump` |
| `j18_` | `cfiptu` |
| `j163_` | `tipoproprietario` |
| `j164_` | `tipopromitente` |

---

## Perguntas que esta classe ajuda a responder

- Qual proprietário principal de uma matrícula?
- Quais coproprietários ou promitentes estão vinculados a uma matrícula?
- Qual lote está vinculado à matrícula?
- A matrícula está ativa ou baixada?
- Qual endereço/logradouro/bairro/setor/quadra/lote de uma matrícula?
- Quais construções existem para a matrícula?
- Qual área total do lote e área construída ativa?
- Quais matrículas pertencem a um CGM?
- Quais matrículas estão associadas a uma imobiliária?
- Quais matrículas existem em um setor, quadra, bairro ou rua?
- Quais dados de registro imobiliário existem para a matrícula?
- Qual cálculo de IPTU foi gerado para matrícula/ano?
- Quais ocorrências estão registradas para a matrícula?

---

## Filtros seguros e recomendados

| Filtro | Campo / expressão | Observação |
|---|---|---|
| Matrícula específica | `j01_matric = :matricula` | Filtro mais seguro para detalhe |
| Matrículas ativas | `j01_baixa IS NULL` | Usado para excluir baixadas |
| Proprietário principal | `j01_numcgm = :numcgm` | Apenas proprietário principal |
| Coproprietário | `propri.j42_numcgm = :numcgm` | Exige join/union com `propri` |
| Promitente | `promitente.j41_numcgm = :numcgm` | Exige join/union com `promitente` |
| Lote | `j01_idbql = :idbql` | Busca por vínculo técnico do lote |
| Setor/quadra/lote | `j34_setor`, `j34_quadra`, `j34_lote` | Requer join com `lote` |
| Construção ativa | `j39_dtdemo IS NULL` | Evita construções demolidas |
| Ano do cálculo | `j23_anousu = :ano` | Requer `iptucalc` |

---

## Cuidados / riscos

- `j01_numcgm` representa o proprietário principal. Para listar todos os envolvidos, é necessário incluir `propri` e `promitente`.
- `j01_baixa IS NULL` deve ser usado quando a análise exigir apenas matrículas ativas.
- Construções devem considerar `j39_dtdemo IS NULL` para evitar incluir construções demolidas.
- A classe usa SQL por concatenação de strings; em uso moderno, substituir variáveis por placeholders parametrizados.
- Nem toda relação aparece como foreign key explícita no código PHP; algumas são relações lógicas inferidas pelos joins.
- `proprietario` e `proprietario_ender` são views/fontes auxiliares e podem carregar regras internas não visíveis nesta classe.
- A consulta por CGM muda conforme a regra aplicada: proprietário principal, coproprietário e promitente podem ou não ser considerados.
- `cfiptu` depende do ano da sessão (`DB_anousu`), portanto consultas de cálculo devem sempre explicitar o exercício quando usadas fora do e-Cidade.