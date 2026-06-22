# Dívida ativa, inscrição e situação dos débitos

> Fonte principal: `/var/www/html/e-cidade-php74/classes/db_divida_classe.php`
>
> Classe: `cl_divida`
>
> Tabela principal: `divida`

## Visão geral

A tabela `divida` registra débitos inscritos em dívida. A chave do registro é `v01_coddiv`.

O grão básico é uma parcela de dívida identificada pelo código da dívida e relacionada ao débito de arrecadação por `v01_numpre` e `v01_numpar`.

Campos relevantes:

| Campo | Significado definido pela classe |
|---|---|
| `v01_coddiv` | Código da dívida |
| `v01_numcgm` | CGM relacionado à dívida |
| `v01_dtinsc` | Data de inscrição |
| `v01_exerc` | Exercício da dívida |
| `v01_numpre` | Número do débito na arrecadação |
| `v01_numpar` | Parcela |
| `v01_numtot` | Total de parcelas |
| `v01_vlrhis` | Valor histórico |
| `v01_proced` | Procedência da dívida |
| `v01_livro`, `v01_folha` | Livro e folha |
| `v01_dtvenc` | Data de vencimento |
| `v01_dtoper` | Data de operação |
| `v01_valor` | Valor registrado |
| `v01_numdig` | Número/dígito do débito |
| `v01_instit` | Instituição da dívida |
| `v01_dtinclusao` | Data de inclusão |
| `v01_processo` | Código do processo |
| `v01_titular` | Titular do processo |
| `v01_dtprocesso` | Data do processo |

Na inclusão, a classe exige:

- CGM;
- data de inscrição;
- exercício;
- número do débito;
- parcela e total de parcelas;
- valor histórico;
- procedência;
- data de vencimento;
- data de operação;
- valor;
- número/dígito.

Livro, folha, observação, instituição e dados do processo não aparecem entre as validações obrigatórias do método de inclusão analisado.

## Consulta cadastral completa

### Consulta: `sql_query`

- **Objetivo:** Recuperar a dívida com contribuinte, instituição, procedência, histórico e receita.
- **Grão esperado:** Uma linha por dívida, salvo multiplicação por registros opcionais.

```sql
select /* campos dinâmicos */
  from divida
       inner join cgm
          on cgm.z01_numcgm = divida.v01_numcgm
       inner join db_config
          on db_config.codigo = divida.v01_instit
       inner join proced
          on proced.v03_codigo = divida.v01_proced
       inner join histcalc
          on histcalc.k01_codigo = proced.k00_hist
       inner join tabrec
          on tabrec.k02_codigo = proced.v03_receit
       inner join db_config as a
          on a.codigo = proced.v03_instit
       left join tipoproced
          on tipoproced.v07_sequencial = proced.v03_codigo
       left join termoinscrreg
          on termoinscrreg.v93_coddiv = divida.v01_coddiv
 where divida.v01_coddiv = :codigo_divida
```

Regras:

- O CGM, a instituição da dívida, a procedência, o histórico de cálculo, a receita e a instituição da procedência são obrigatórios nessa consulta.
- `termoinscrreg` é opcional e pode multiplicar linhas se houver vários registros para a mesma dívida.
- O alias `a` representa a instituição cadastrada em `proced.v03_instit`; `db_config` sem alias representa `divida.v01_instit`.

Defeito ou divergência importante:

- Este método relaciona `tipoproced.v07_sequencial = proced.v03_codigo`.
- As consultas analíticas da mesma classe relacionam `tipoproced.v07_sequencial = proced.v03_tributaria`.
- Não reutilize o join de `tipoproced` desse método sem confirmar qual coluna representa o tipo da procedência.

### Consulta: `sql_query_divida`

Versão reduzida sem instituição e sem vínculos com termo:

```sql
select /* campos dinâmicos */
  from divida
       inner join cgm
          on cgm.z01_numcgm = divida.v01_numcgm
       inner join proced
          on proced.v03_codigo = divida.v01_proced
       inner join histcalc
          on histcalc.k01_codigo = proced.k00_hist
       inner join tabrec
          on tabrec.k02_codigo = proced.v03_receit
 where divida.v01_coddiv = :codigo_divida
```

### Consulta: `sql_query_file`

Consulta somente a tabela `divida`:

```sql
select /* campos dinâmicos */
  from divida
 where divida.v01_coddiv = :codigo_divida
```

Os três métodos aceitam campos, condições e ordenação montados dinamicamente. Em consultas novas, utilize allowlist de colunas e parâmetros vinculados.

## Localização da dívida por origem

### Consulta: `sql_queryinscricao`

Relaciona a dívida a uma inscrição municipal:

```sql
select /* campos dinâmicos */
  from divida
       inner join divinscr
          on divinscr.v01_coddiv = divida.v01_coddiv
 where divinscr.v01_inscr = :inscricao
```

### Consulta: `sql_querymatric`

Relaciona a dívida a uma matrícula imobiliária:

```sql
select /* campos dinâmicos */
  from divida
       inner join divmatric
          on divmatric.v01_coddiv = divida.v01_coddiv
 where divmatric.v01_matric = :matricula
```

### Consulta: `sql_querynumcgm`

Localiza dívidas pelo CGM:

```sql
select /* campos dinâmicos */
  from divida
       inner join cgm
          on cgm.z01_numcgm = divida.v01_numcgm
 where divida.v01_numcgm = :cgm
```

### Consulta: `sql_queryproced`

Localiza dívidas pela procedência:

```sql
select /* campos dinâmicos */
  from divida
       inner join proced
          on proced.v03_codigo = divida.v01_proced
 where divida.v01_proced = :procedencia
```

Cuidados de cardinalidade:

- Uma inscrição, matrícula, CGM ou procedência pode possuir várias dívidas.
- Para contar dívidas, use `count(distinct divida.v01_coddiv)`.
- Para contar contribuintes, use `count(distinct divida.v01_numcgm)`.
- Não trate inscrição, matrícula e CGM como identificadores equivalentes; são origens cadastrais diferentes.

## Situação paga ou não paga

### Consulta: `sql_querysituacao`

O método monta:

```sql
select case
         when x.aberto is not null then 'divida nao paga'
         else 'divida ja paga'
       end
  from (
        select arrecad.k00_numpre as aberto,
               arrepaga.k00_numpre as pago
          from divida
               left join arrecad
                 on arrecad.k00_numpre = divida.v01_numpre
               left join arrepaga
                 on arrepaga.k00_numpre = divida.v01_numpre
         where divida.v01_coddiv = :codigo_divida
           and /* condição adicional */
       ) as x
```

Comportamento real:

- A classificação verifica somente se `arrecad.k00_numpre` não é nulo.
- O campo `pago`, vindo de `arrepaga`, é selecionado mas não participa do `case`.
- Se existirem registros simultaneamente em `arrecad` e `arrepaga`, o resultado continua sendo `divida nao paga`.
- Os joins usam apenas `numpre`, sem restringir `numpar`, podendo gerar múltiplas linhas e situações repetidas.

Portanto, esse método não é uma regra confiável e completa para determinar quitação. Para responder se uma parcela foi paga, relacione também `k00_numpar` e defina explicitamente a precedência entre as tabelas de débito aberto, pago, anterior e histórico.

## Observação gerada na importação

### Regra: `resumo_importacao`

O texto de observação da dívida importada depende de `cadtipo.k03_tipo`:

| Tipo | Origem consultada | Regra resumida |
|---|---|---|
| `3` | `issvar`, `issvarlev`, `levanta` | Usa `levanta.y60_obs`; sem levantamento usa `issvar.q05_histor` |
| `4` | contribuição de melhoria | Compõe lista, edital, contribuição, rua e descrição |
| `7` | `diversos` | Usa `diversos.dv05_obs` |
| `11` | `autonumpre`, `auto` | Compõe número e observação do auto de infração |
| `16` | `termo`, `termodiver`, `diversos` | Agrupa diversos, observações e parcelas do parcelamento |
| `17` | parcelamento de contribuição de melhoria | Compõe lista, edital, contribuição, rua e descrição |
| `19` | `vistorianumpre`, `vistorias` | Usa `vistorias.y70_obs` |

Todas as consultas partem do `numpre` informado. Para tipos não mapeados, o método retorna observação vazia.

No tipo `16`, a consulta agrupa por `dv05_obs` e `v07_parcel` ao mesmo tempo que agrega observações distintas. Isso pode produzir mais de uma linha por parcelamento; o método utiliza apenas a primeira linha retornada.

## Exercício da dívida importada

### Regra: `getExercicioDivida`

O exercício é obtido conforme o tipo do débito:

| Tipo | Fonte do exercício |
|---|---|
| `1` - IPTU | `iptunump.j20_anousu` |
| `2` - ISS fixo | `isscalc.q01_anousu` |
| `3` - ISS variável | `issvar.q05_ano` |
| `7` - Diversos | `diversos.dv05_exerc` |
| `9` - Alvará | `isscalc.q01_anousu` |
| `19` - Vistoria | Ano de `vistorias.y70_data` |

Para os demais tipos, ou quando a consulta não retorna linha, o método usa o ano padrão recebido em `$iAnoDefult`.

O vínculo é feito pelo `numpre`. Caso a origem possua mais de um registro para o mesmo número, o método lê apenas a primeira linha.

## Resumo das receitas inscritas

### Regra: `getResumoDeReceitas`

Seleciona dívidas:

```sql
where divida.v01_instit = :instituicao_sessao
  and divida.v01_dtinclusao between :data_inicial and :data_final
```

A consulta combina por `union all` três fontes de débito:

- `arrecad`;
- `arrecant`;
- `arreold`.

Em todas as fontes, o vínculo com a dívida utiliza:

```sql
fonte.k00_numpre = divida.v01_numpre
and fonte.k00_numpar = divida.v01_numpar
```

Também relaciona `proced`, `tipoproced`, `tabrec`, `taborc`, `arretipo`, `cadtipo` e, opcionalmente, os dados da importação e a origem por matrícula, inscrição ou CGM.

### Origem e contribuinte

A prioridade usada para formar a origem é:

1. matrícula: prefixo `M-`;
2. inscrição: prefixo `I-`;
3. CGM: prefixo `C-`.

O nome é obtido por `fc_busca_envolvidos` com o mesmo tipo de origem.

Se existirem simultaneamente vínculos de matrícula e inscrição, prevalece matrícula.

### Correção, juros e multa

O total é:

```text
total = corrigido + juros + multa
```

Funções utilizadas:

- `fc_corre` para valor corrigido;
- `fc_juros` multiplicado pelo valor original;
- `fc_multa` multiplicado pelo valor original.

Quando a dívida possui registro em `divimporta`, a data final da importação (`v02_datafim`) é usada como referência. Sem importação, usa a data corrente da sessão (`DB_datausu`) e seu exercício.

### Curto e longo prazo

A classificação usa `cadtipo.k03_tipo` e o limite:

```text
31 de dezembro do exercício seguinte à dívida
```

Regras implementadas:

- tipos `5`, `15` e `18`: longo prazo;
- tipos `6` e `13` com vencimento posterior ao limite: longo prazo;
- tipos `6` e `13` com vencimento até o limite: curto prazo.

Tipos fora desses conjuntos não são incluídos nas estruturas de curto ou longo prazo desse método.

Os valores são agrupados por receita (`k00_receit`).

### Ajuste pela arrecadação histórica

O método soma pagamentos realizados nos três anos anteriores ao ano inicial solicitado. Depois calcula:

```text
estimativa de curto prazo = (total pago nos 3 anos / 3) * 2
```

Essa estimativa é convertida em percentual do saldo de longo prazo e transferida proporcionalmente para curto prazo, limitada ao total disponível.

Defeito de implementação:

- Ao inicializar alguns metadados de uma receita de curto prazo, o código grava descrição e código orçamentário em `$aLongoPrazo`, enquanto os valores são gravados em `$aCurtoPrazo`.
- Consumidores não devem presumir que todos os metadados do curto prazo estarão preenchidos corretamente.

## Resumo geral da dívida por data-base

### Consulta: `sql_queryProcessamentoResumoGeralDivida`

Esta rotina não é somente leitura: antes de retornar a consulta final, cria tabelas temporárias e índices na conexão.

A tabela de débitos da data-base é calculada dinamicamente:

```text
debitos_<data somente com números>_<instituição>
```

Exemplo conceitual para `2025-12-31` e instituição `1`:

```text
debitos_20251231_1
```

### Parcelamentos corrigidos

Cria `w_parcelamentos_corrigidos`, agrupando por parcelamento, número do débito, tipo e receita:

```text
valor_total = k22_vlrcor + k22_juros + k22_multa
```

Filtros obrigatórios:

- instituição da sessão;
- data-base;
- tipos de débito recebidos em `$sListaTipo`.

### Dívidas relacionadas a certidões

Cria `w_certidao_dividas` unindo cinco origens:

| Tipo | Descrição usada pela classe |
|---|---|
| `1` | Certidão de parcelamento de dívida |
| `2` | Parcelamento de inicial de certidão do parcelamento |
| `3` | Parcelamento de inicial de certidão de dívida |
| `4` | Certidão do foro |
| `5` | Certidão de dívida |

As principais tabelas são `certter`, `termodiv`, `termoini`, `inicialcert`, `certdiv`, `certid` e `divida`.

Cuidados:

- O tipo `1` parte de `certter`, mas filtra `certter.v14_certid is null`. Essa condição é suspeita e deve ser validada antes de reutilizar a receita.
- O tipo `4` exclui iniciais já relacionadas a `termoini`.
- O tipo `5` exclui certidões presentes em `inicialcert` e restringe `certid.v13_instit` à instituição da sessão.
- Quando fornecida, a lista de exercícios restringe `divida.v01_exerc`.

### Agregação final

O resultado combina:

- dívida ativa da tabela de débitos da data-base;
- dívidas de parcelamentos;
- parcelamentos de iniciais/certidões, com rateio proporcional;
- certidões de dívida.

O grão final é a combinação de:

- exercício;
- procedência;
- tipo de débito;
- tipo de procedência;
- receita;
- vencimento;
- descrições correspondentes.

Valores agregados:

- histórico;
- corrigido;
- juros;
- multa;
- total.

Não conte as linhas como quantidade de dívidas. Para quantidade de registros, consulte os identificadores da origem antes da agregação.

## Débitos pagos em exercícios anteriores

### Consulta: `sql_queryDebitosAnteriores`

Para uma data ou ano de referência, considera os três exercícios anteriores:

```sql
select arretipo.k03_tipo,
       arrecant.k00_receit as receit,
       divida.v01_proced,
       divida.v01_exerc,
       proced.v03_tributaria,
       round(sum(arrepaga.k00_valor), 2) as total
  from divida
       inner join arrepaga
          on arrepaga.k00_numpre = divida.v01_numpre
         and arrepaga.k00_numpar = divida.v01_numpar
       inner join arrecant
          on arrecant.k00_numpre = divida.v01_numpre
         and arrecant.k00_numpar = divida.v01_numpar
       inner join arretipo
          on arretipo.k00_tipo = arrecant.k00_tipo
       inner join proced
          on proced.v03_codigo = divida.v01_proced
 where extract(year from arrepaga.k00_dtpaga) in (
       :ano_referencia_menos_1,
       :ano_referencia_menos_2,
       :ano_referencia_menos_3
 )
 group by arretipo.k03_tipo,
          arrecant.k00_receit,
          divida.v01_proced,
          divida.v01_exerc,
          proced.v03_tributaria
```

O resultado representa valor pago agregado, não quantidade de dívidas ou pagamentos.

O método não filtra instituição. Em ambiente multi-instituição, uma consulta nova deve avaliar a inclusão de `divida.v01_instit`.

## Auto de infração relacionado a dívida antiga

### Consulta: `sql_query_auto`

```sql
select distinct arreauto.k00_auto,
                divida.v01_numpre
  from divida
       inner join divold
          on divold.k10_coddiv = divida.v01_coddiv
       inner join diversos
          on diversos.dv05_numpre = divold.k10_numpre
       inner join diverimportaold
          on diverimportaold.dv13_diversos = diversos.dv05_coddiver
       inner join arreauto
          on arreauto.k00_numpre = diverimportaold.dv13_numpre
 where /* condição dinâmica */
```

Objetivo observado: localizar o número do auto relacionado a dívidas importadas por meio da cadeia de registros antigos e diversos.

O parâmetro `$campos` não é utilizado pelo método; o retorno é sempre `distinct k00_auto, v01_numpre`.

## Recomendações para consultas do agente

- Use `v01_coddiv` como identificador da dívida e o par `v01_numpre`/`v01_numpar` para relacionar a parcela às tabelas de arrecadação.
- Sempre filtre `v01_instit` em perguntas restritas à instituição atual.
- Diferencie quantidade de dívidas, parcelas, contribuintes, inscrições e matrículas.
- Para situação de pagamento, não reutilize `sql_querysituacao` sem corrigir a lógica e incluir a parcela.
- Para valores atualizados, explicite a data-base e use as funções municipais de correção, juros e multa.
- Não some diretamente resultados de `arrecad`, `arrecant` e `arreold` sem controlar duplicidade e precedência.
- A origem segue prioridade matrícula, inscrição e CGM nas consultas de resumo.
- Não reutilize silenciosamente o join divergente de `tipoproced`.
- Trate CPF/CNPJ, nome e dados de processo como informações sensíveis e retorne apenas o necessário.
- Condições, listas e nomes de tabelas são concatenados pela classe legada. Novas consultas devem validar listas e usar parâmetros vinculados sempre que possível.
