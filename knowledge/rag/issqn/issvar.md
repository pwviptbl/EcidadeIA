## issqn.issvar

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_issvar_classe.php`

Apuracao mensal do ISSQN variavel e de seus fluxos associados de retencao, complemento, notas e arrecadacao. Esta classe e o ponto central para gravar o imposto devido por competencia, ligar a arrecadacao do `numpre` e produzir visoes de consulta e manutencao.

### Resumo tecnico

- **Classe:** `cl_issvar`
- **Tabela principal:** `issvar`
- **Chave primaria tecnica:** `q05_codigo`
- **Numpre:** `q05_numpre`
- **Parcela:** `q05_numpar`
- **Valor do imposto devido:** `q05_valor`
- **Ano da competencia:** `q05_ano`
- **Mes da competencia:** `q05_mes`
- **Historico:** `q05_histor`
- **Aliquota aplicada:** `q05_aliq`
- **Valor bruto/base informada:** `q05_bruto`
- **Valor informado pelo contribuinte:** `q05_vlrinf`
- **Grau:** uma linha por apuracao mensal de ISS variavel, identificada tecnicamente por `q05_codigo`.

Interpretacao segura:

- `q05_valor` e o imposto devido da apuracao, nao o valor de uma nota isolada.
- `q05_vlrinf` e o valor informado pelo contribuinte ou atualizado pelo fluxo; nao tratar como sinônimo de `q05_valor`.
- `q05_bruto` representa a base ou valor bruto relacionado ao calculo.
- Em consultas por competencia, a chave operacional costuma ser `q05_ano`, `q05_mes`, `q05_numpre` e `q05_numpar`.

### Relacionamentos

- `q05_numpre -> arrecad.k00_numpre`
- `q05_numpre -> arreinscr.k00_numpre`
- `q05_numpre -> arrenumcgm.k00_numpre`
- `q05_numpre -> issplannumpre.q32_numpre`
- `q05_numpre -> issplan.q20_numpre`
- `q05_codigo -> issvarnotas.q06_codigo`
- `q05_codigo -> issvarold.q22_codigo`
- `q05_codigo -> issvarsemmovreg.q15_issvar`
- `q05_numpre -> isscalc.q01_numpre`

### Consultas da classe

#### `sql_query`

- **Objetivo:** leitura direta da apuracao de ISS variavel.
- **Tabelas:** `issvar`
- **Grau do resultado:** uma linha por apuracao, identificada por `q05_codigo`
- **Juncoes:** nenhuma
- **Filtro padrao:** `issvar.q05_codigo = :codigo`
- **Uso seguro:** obter a apuracao sem multiplicacao por arrecadacao ou notas.

```sql
select /* campos dinamicos */
  from issvar
 where issvar.q05_codigo = :codigo;
```

#### `sql_query_file`

- **Objetivo:** leitura fisica direta da tabela `issvar`.
- **Tabelas:** `issvar`
- **Grau do resultado:** uma linha por apuracao
- **Juncoes:** nenhuma
- **Uso seguro:** recuperar o registro bruto quando a visao com joins nao for necessaria.

#### `sql_query_arrecad`

- **Objetivo:** consultar a apuracao com os dados de arrecadacao do mesmo `numpre` e `numpar`.
- **Tabelas:** `issvar`, `arreinscr`, `arrecad`
- **Grau do resultado:** uma linha por apuracao, podendo multiplicar pelos registros de arrecadacao associados
- **Juncoes:**
  - `arreinscr.k00_numpre = issvar.q05_numpre` `inner join`
  - `arrecad.k00_numpre = arreinscr.k00_numpre and arrecad.k00_numpar = issvar.q05_numpar` `inner join`
- **Uso seguro:** analisar o ISS variavel em conjunto com o debito arrecadado da mesma competencia.

```sql
select /* campos dinamicos */
  from issvar
 inner join arreinscr on issvar.q05_numpre = arreinscr.k00_numpre
 inner join arrecad on arreinscr.k00_numpre = arrecad.k00_numpre
                   and issvar.q05_numpar = arrecad.k00_numpar
 where issvar.q05_codigo = :codigo;
```

#### `sql_query_arreinscr`

- **Objetivo:** consultar a apuracao com visao de inscricao e situacao de arrecadacao/pagamento.
- **Tabelas:** `issvar`, `arreinscr`, `arrecad`, `arrepaga`
- **Grau do resultado:** uma linha por apuracao, com possibilidade de expandir por dados de arrecadacao e pagamento
- **Juncoes:**
  - `arreinscr.k00_numpre = issvar.q05_numpre` `inner join`
  - `arrecad.k00_numpre = arreinscr.k00_numpre and arrecad.k00_numpar = issvar.q05_numpar` `left join`
  - `arrepaga.k00_numpre = arreinscr.k00_numpre and arrepaga.k00_numpar = issvar.q05_numpar` `left join`
- **Uso seguro:** identificar o vinculo do `numpre` com a inscricao e visualizar aberto/pago.

#### `sql_query_arrenumcgm`

- **Objetivo:** consultar a apuracao com base no CGM do devedor/contribuinte.
- **Tabelas:** `arrenumcgm`, `issvar`, `arrepaga`
- **Grau do resultado:** uma linha por apuracao, dependendo do `numpre` vinculado ao CGM
- **Juncoes:**
  - `issvar.q05_numpre = arrenumcgm.k00_numpre` `inner join`
  - `arrepaga.k00_numpre = arrenumcgm.k00_numpre and arrepaga.k00_numpar = issvar.q05_numpar` `left join`
- **Uso seguro:** buscas orientadas pelo CGM, sem passar primeiro pela inscricao.

#### `sql_query_arretivprinc`

- **Objetivo:** consultar a apuracao com a dimensao cadastral e de atividade principal.
- **Tabelas:** `issvar`, `arreinscr`, `arrecad`, `issbase`, `cgm`, `tabativ`, `ativid`, `ativprinc`, `clasativ`, `classe`
- **Grau do resultado:** uma linha por apuracao, enriquecida com inscricao, contribuinte e classificacao da atividade principal
- **Uso seguro:** relatórios e analises de ISS variavel por contribuinte e atividade principal.

### Fluxos de negocio

#### `excluir_issvar($codigo, $codlev = 0)`

- Move a apuracao para `issvarold`.
- Move as notas associadas de `issvarnotas` para `issvarnotasold`.
- Exclui o registro original de `issvar`.
- Uso seguro: cancelamento/remoção com rastreabilidade historica.

#### `incluir_issvar_complementar(...)`

- Cria ou reaproveita a apuracao de ISS variavel.
- Adiciona notas em `issvarnotas`.
- Vincula `arreinscr` ao `numpre` da apuracao.
- Gera `arrecad` com vencimento definido por `confvencissqnvariavel` e `cadvenc`.
- Quando `sTipo = 'T'`, também cria `issplan` e `issplannumpre`.

#### `gerarIssqnVariavelComplementar(...)`

- Executa o fluxo atual de complemento de ISS variavel.
- Reaproveita a apuracao se ja existir registro na mesma competencia e `numpre`.
- Atualiza ou insere `arrecad` conforme existencia de parcela em aberto.
- E o caminho mais completo para gerar complemento de ISSQN variavel.

#### `incluir_issvar_nfse(...)`

- Reaproveita a apuracao existente para o mesmo ano, mes e `numpre`.
- Garante notas em `issvarnotas`.
- Gera ou atualiza a arrecadacao conforme competencia e configuracao de vencimento.
- Adiciona regra especial para empresa publica, ajustando a receita conforme configuracao.

#### `incluir_issvar_dms(...)`

- Fluxo semelhante ao de NFSe, mas com regras de vencimento e configuracao distintas.
- Usa `db_confplan` e `confvencissqnvariavel`.
- Gera `arrecad` com receita e historico configurados.

### Consultas auxiliares

#### `getDadosCompetenciaInscricao($iMes, $iAno, $iInscricao)`

- Retorna `numpre` e `numpar` da apuracao para uma inscricao em determinada competencia.
- Usa `issvar` com `arreinscr`.
- Filtro importante: `q05_mes`, `q05_ano` e `k00_inscr`.

#### `getDadosCompetenciaCgm($iMes, $iAno, $iNumCgm)`

- Retorna `numpre` e `numpar` da apuracao para um CGM.
- Usa `issvar` com `arrecad`.
- Filtro importante: `q05_mes`, `q05_ano` e `k00_numcgm`.

#### `sql_update_vlrinf($iNumpre, $iNumpar, $iVlrInf)`

- Gera `UPDATE` direto para `q05_vlrinf` por `numpre` e `numpar`.

#### `sql_update_vlrinf_if_null($q05_codigo, $q05_vlrinf)`

- Gera `UPDATE` apenas quando `q05_vlrinf = 0`.
- Uso seguro: corrigir valor informado sem sobrescrever registros ja preenchidos.

#### `sql_isscalc_numpre_numpar($iNumpre, $iNumpar)`

- Liga `issvar` a `isscalc` e `arreinscr` para um `numpre` e parcela.
- Filtra `q01_cadcal in (2, 3)`, ou seja, ISS fixo e ISS variavel.

### Perguntas que ela responde bem

- Qual foi o ISS variavel calculado em uma competencia?
- Qual o valor informado pelo contribuinte e qual o valor devido?
- Qual `numpre` e qual parcela pertencem a uma apuracao?
- Qual arrecadacao e qual inscricao estao vinculadas ao ISS variavel?
- Quais notas foram declaradas dentro de uma apuracao?

### Cuidados

- Nao tratar `q05_valor` como valor de cada nota.
- Nao usar `sql_query_file()` quando a pergunta exigir situacao financeira ou cadastral.
- `sql_query_arrecad()` multiplica resultado por detalhes de arrecadacao; para contagem, usar `DISTINCT` no grão correto.
- O fluxo de complemento e geracao de arrecadacao pode criar `issplan` e `issplannumpre`; nao confundir esses registros com a apuracao original.
- Quando a pergunta for por nota, usar `issvarnotas`; quando for por apuracao mensal, usar `issvar`.
