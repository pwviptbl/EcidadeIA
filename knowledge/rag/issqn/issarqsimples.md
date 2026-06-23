## issqn.issarqsimples

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_issarqsimples_classe.php`

Cabecalho do arquivo do Simples Nacional importado pelo modulo ISSQN. A classe representa o lote/arquivo com seus metadados e tambem concentra rotinas de leitura, validacao previa e processamento do arquivo.

### Resumo tecnico

- **Classe:** `cl_issarqsimples`
- **Tabela principal:** `issarqsimples`
- **Chave primaria:** `q17_sequencial`
- **Instituicao:** `q17_instit`
- **Data do arquivo:** `q17_data`
- **Numero da remessa:** `q17_nroremessa`
- **Versao:** `q17_versao`
- **Quantidade de registros:** `q17_qtdreg`
- **Valor total:** `q17_vlrtot`
- **Codigo do banco:** `q17_codbco`
- **OID do arquivo:** `q17_oidarq`
- **Nome do arquivo:** `q17_nomearq`
- **Grau:** uma linha por arquivo recebido/importado.

Interpretacao segura:

- Esta entidade nao representa lancamento tributario individual.
- O registro funciona como cabecalho do arquivo e ponto de partida para registros filhos, erros e processamento.
- Para contar arquivos, use `COUNT(DISTINCT q17_sequencial)`.

### Relacionamentos

- `q17_instit -> db_config.codigo`
- `db_config.numcgm -> cgm.z01_numcgm`
- `q17_sequencial -> issarqsimplesdisarq.q43_issarqsimples`

### Consultas da classe

#### `sql_query`

- **Objetivo:** ler o cabecalho do arquivo com enriquecimento da instituicao e do CGM vinculado.
- **Tabelas:** `issarqsimples`, `db_config`, `cgm`
- **Grau do resultado:** uma linha por arquivo, desde que a instituicao exista em `db_config` e o CGM esteja vinculado
- **Juncoes:**
  - `db_config.codigo = issarqsimples.q17_instit` `inner join`
  - `cgm.z01_numcgm = db_config.numcgm` `inner join`
- **Filtro padrao:** `issarqsimples.q17_sequencial = :sequencial`
- **Uso seguro:** consultar o arquivo com contexto da instituicao e do contribuinte.

```sql
select /* campos dinamicos */
  from issarqsimples
 inner join db_config on db_config.codigo = issarqsimples.q17_instit
 inner join cgm on cgm.z01_numcgm = db_config.numcgm
 where issarqsimples.q17_sequencial = :sequencial;
```

#### `sql_query_file`

- **Objetivo:** leitura fisica direta da tabela `issarqsimples`.
- **Tabelas:** `issarqsimples`
- **Grau do resultado:** uma linha por arquivo
- **Juncoes:** nenhuma
- **Uso seguro:** extrair ou validar apenas os metadados do arquivo, sem depender de cadastro auxiliar.

#### `sql_query_processados`

- **Objetivo:** listar arquivos com indicador de processamento/distribuicao.
- **Tabelas:** `issarqsimples`, `db_config`, `cgm`, `issarqsimplesdisarq`
- **Grau do resultado:** uma linha por arquivo, com opcao de aparecer sem distribuicao quando nao houver `issarqsimplesdisarq`
- **Juncoes:**
  - `db_config.codigo = issarqsimples.q17_instit` `inner join`
  - `cgm.z01_numcgm = db_config.numcgm` `inner join`
  - `issarqsimplesdisarq.q43_issarqsimples = q17_sequencial` `left join`
- **Uso seguro:** conferir quais arquivos foram processados ou estao pendentes de distribuicao.

### Rotinas de processamento

#### `validaArquivo($iCodigoArquivo)`

- **Objetivo:** fazer pre-processamento e detectar inconsistencias antes do processamento final.
- **Dependencias principais:** `issarqsimplesreg`, `issarqsimplesregerro`, `parissqn`, `issbase`, `isscalc`, `issvar`, `arrecad`, `isscadsimples`, `isscadsimplesbaixa`, `issbasecaracteristica`
- **Saida:** lista de erros e avisos gravados em `issarqsimplesregerro`
- **Regras observadas:**
  - valida duplicidade ou inexistencia de CGM para o CNPJ do registro;
  - verifica se existe inscricao ativa e univoca;
  - confere calculo de ISS e ISS variavel;
  - cruza competencia, pagamento e situacao do Simples quando aplicavel.

Interpretacao segura:

- Nao tratar essa rotina como simples validacao de formulario.
- Ela faz auditoria de consistencia do arquivo contra varias bases do ISSQN.

#### `processaArquivo($iRegistro, $sArquivo, $iBanco, $iAgencia, $iConta)`

- **Objetivo:** executar o processamento do arquivo e distribuir os registros relacionados.
- **Uso observado:** cria/atualiza distribuicoes, relaciona registros do Simples, alimenta bases auxiliares e registra inconsistencias quando necessario.
- **Cuidados:** o metodo depende fortemente de outras classes do ISSQN e do contexto transacional.

### Campos de negocio confirmados

- `q17_sequencial`: identificador do arquivo.
- `q17_instit`: instituicao responsavel pelo arquivo.
- `q17_data`: data de referencia do arquivo.
- `q17_nroremessa`: numero da remessa.
- `q17_versao`: versao do layout ou lote.
- `q17_qtdreg`: quantidade de registros informados.
- `q17_vlrtot`: valor total do arquivo.
- `q17_codbco`: banco associado.
- `q17_oidarq`: referencia binaria/arquivo armazenado.
- `q17_nomearq`: nome fisico do arquivo.

### Perguntas que ela responde bem

- Qual arquivo do Simples foi importado?
- Qual instituicao enviou o arquivo?
- Quais arquivos ja foram processados ou distribuidos?
- Qual o total e a quantidade informados no cabecalho do arquivo?

### Cuidados

- Nao confundir `issarqsimples` com lancamento tributario ou arrecadacao.
- `q17_qtdreg` e `q17_vlrtot` sao metadados do arquivo, nao prova de processamento concluido.
- `sql_query_file` e a leitura mais segura quando o cadastro auxiliar esta inconsistente.
- A classe usa fluxo legado com `HTTP_POST_VARS` e acoplamento alto com outras classes do ISSQN.
