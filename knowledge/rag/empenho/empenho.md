## empenho.empenho

Mapeia as regras de negócio para a execução da despesa pública: empenho (compromisso), liquidação (recebimento do serviço/bem) e pagamento (efetiva saída de caixa).

---

### Regras de Negócio e Ciclo da Despesa

1. **Empenho (Compromisso):**
   - Registrado em `empenho.empempenho` (identificado por `e60_numemp`).
   - Associa-se a uma dotação orçamentária (`e60_coddot`) e a um credor/fornecedor (`e60_numcgm` ligado a `protocolo.cgm`).
   - O valor empenhado total é a soma de seus itens em `empenho.empempitem.e62_vltot`.

2. **Liquidação (Nota de Liquidação):**
   - Registrado em `empenho.empnota` (identificado por `e69_codnota`).
   - Uma liquidação atesta que o fornecedor entregou o material ou prestou o serviço.
   - O valor liquidado é registrado nos itens em `empenho.empnotaitem.e72_vlrliq` (líquido) e descontos ou anulações em `e72_vlranu`.

3. **Pagamento (Saída de Caixa):**
   - A saída efetiva de dinheiro é registrada em `empenho.empagemov` (movimento de pagamento da agenda, identificado por `e81_codmov`).
   - Um pagamento só é considerado válido se `e81_cancelado IS NULL`.
   - O valor pago reside em `e81_valor`.

4. **Saldos da Despesa (Restos a Pagar / Saldo a Liquidar):**
   - *Saldo a Liquidar:* `Valor Empenhado - Valor Liquidado`.
   - *Saldo a Pagar:* `Valor Liquidado - Valor Pago`.

---

### Conceitos & Relacionamentos Base
- **Vínculo Empenho-Dotação:** `empempenho.e60_coddot = orcdotacao.o58_coddot` AND `empempenho.e60_anousu = orcdotacao.o58_anousu`
- **Vínculo Empenho-Credor:** `empempenho.e60_numcgm = cgm.z01_numcgm`
- **Vínculo Empenho-Liquidação:** `empempenho.e60_numemp = empnota.e69_numemp`
- **Vínculo Liquidação-Itens:** `empnota.e69_codnota = empnotaitem.e72_codnota`
- **Vínculo Empenho-Pagamento:** `empempenho.e60_numemp = empagemov.e81_numemp`

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Qual o total empenhado por credor (fornecedor) em um determinado ano?
- **Descrição:** Consolida o valor total de despesas empenhadas (contratadas) por fornecedor no exercício.
- **Receita SQL:**
```sql
SELECT 
    cgm.z01_numcgm as codigo_credor,
    cgm.z01_nome as nome_credor,
    SUM(ei.e62_vltot) as total_empenhado
FROM empenho.empempenho e
JOIN protocolo.cgm cgm ON e.e60_numcgm = cgm.z01_numcgm
JOIN empenho.empempitem ei ON e.e60_numemp = ei.e62_numemp
WHERE e.e60_anousu = :ano
GROUP BY cgm.z01_numcgm, cgm.z01_nome
ORDER BY total_empenhado DESC;
```

#### 2. Qual o valor total Liquidado e Pago de um empenho específico?
- **Descrição:** Retorna a situação financeira de execução de um empenho (quanto já foi atestado e quanto já foi efetivamente pago).
- **Receita SQL:**
```sql
WITH liq AS (
  SELECT e69_numemp, SUM(e72_vlrliq) as total_liquidado
  FROM empenho.empnota n
  JOIN empenho.empnotaitem ni ON n.e69_codnota = ni.e72_codnota
  WHERE e69_numemp = :numemp
  GROUP BY e69_numemp
),
pag AS (
  SELECT e81_numemp, SUM(e81_valor) as total_pago
  FROM empenho.empagemov
  WHERE e81_numemp = :numemp 
    AND e81_cancelado IS NULL
  GROUP BY e81_numemp
)
SELECT 
    e.e60_numemp as numero_empenho,
    COALESCE(l.total_liquidado, 0) as liquidado,
    COALESCE(p.total_pago, 0) as pago,
    (COALESCE(l.total_liquidado, 0) - COALESCE(p.total_pago, 0)) as saldo_a_pagar
FROM empenho.empempenho e
LEFT JOIN liq l ON e.e60_numemp = l.e69_numemp
LEFT JOIN pag p ON e.e60_numemp = p.e81_numemp
WHERE e.e60_numemp = :numemp;
```

---

## Consultas extraídas de `db_empempenho_classe.php`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_empempenho_classe.php`
- **Classe:** `cl_empempenho`
- **Tabela principal:** `empenho.empempenho`
- **Chave do empenho:** `e60_numemp`
- **Número exibido do empenho:** `e60_codemp`
- **Exercício:** `e60_anousu`
- **Instituição:** `e60_instit`
- **Dotação:** `e60_coddot`
- **Credor:** `e60_numcgm`
- **Data de emissão:** `e60_emiss`
- **Valores mantidos no cabeçalho:** `e60_vlrorc`, `e60_vlremp`, `e60_vlrliq`, `e60_vlrpag`, `e60_vlranu`
- **Tipo do empenho:** `e60_codtipo`
- **Tipo de compra:** `e60_codcom`
- **Processo protocolado direto:** `e60_protprocesso_id`

As consultas da classe recebem listas de campos, ordenação e cláusulas `WHERE` montadas pelo chamador. Os exemplos abaixo representam a estrutura fixa; os filtros adicionais dependem da tela ou relatório consumidor.

### Consulta base do empenho: `sql_query`

- **Objetivo:** Recuperar o empenho com credor, instituição, dotação e classificações orçamentárias.
- **Grão do resultado:** Em regra, uma linha por empenho, desde que os cadastros relacionados sejam únicos nas chaves usadas.
- **Junções principais:**
  - `empempenho.e60_numcgm = cgm.z01_numcgm`
  - `empempenho.e60_instit = db_config.codigo`
  - `(empempenho.e60_anousu, empempenho.e60_coddot) = (orcdotacao.o58_anousu, orcdotacao.o58_coddot)`
  - `empempenho.e60_codtipo = emptipo.e41_codtipo`
  - `empempenho.e60_codcom = pctipocompra.pc50_codcom`
  - `empempenho.e60_concarpeculiar = concarpeculiar.c58_sequencial`
- **Classificação da dotação:** A dotação liga função, subfunção, programa, projeto/atividade, elemento, órgão, unidade e tipo de recurso.
- **Filtro padrão:** `empempenho.e60_numemp = :numemp`, quando o número interno é informado e não há `$dbwhere`.
- **Cuidados:** Todos os relacionamentos são `INNER JOIN`; um cadastro classificatório ausente elimina o empenho do resultado.

```sql
SELECT /* campos dinâmicos */
FROM empempenho
JOIN cgm
  ON cgm.z01_numcgm = empempenho.e60_numcgm
JOIN db_config
  ON db_config.codigo = empempenho.e60_instit
JOIN orcdotacao
  ON orcdotacao.o58_anousu = empempenho.e60_anousu
 AND orcdotacao.o58_coddot = empempenho.e60_coddot
JOIN emptipo
  ON emptipo.e41_codtipo = empempenho.e60_codtipo
JOIN pctipocompra
  ON pctipocompra.pc50_codcom = empempenho.e60_codcom
/* demais classificações da dotação */
WHERE empempenho.e60_numemp = :numemp;
```

### Variantes de leitura: `sql_query_file` e `sql_query_buscaempenhos`

- **`sql_query_file`:** Lê somente `empempenho`, sem joins, usando `e60_numemp` como filtro padrão.
- **`sql_query_buscaempenhos`:** Consulta reduzida com instituição, dotação, credor, projeto/atividade e elemento.
- **Uso recomendado:** Preferir `sql_query_file` quando apenas os campos físicos do empenho forem necessários; usar a variante de busca quando a resposta depender de descrições básicas da classificação orçamentária.
- **Cuidados:** `sql_query_buscaempenhos` usa `INNER JOIN`; empenhos com relacionamento classificatório inconsistente não aparecem.

### Consulta com permissão orçamentária: `sql_query_consulta`

- **Objetivo:** Consultar empenhos respeitando as classificações orçamentárias permitidas ao usuário logado.
- **Regra comprovada:** O empenho só aparece quando a dotação corresponde integralmente a uma permissão em `db_permemp` vinculada ao usuário em `db_usupermemp`.
- **Usuário:** `db_usupermemp.db21_id_usuario = DB_id_usuario` da sessão.
- **Dimensões verificadas:** exercício, órgão, unidade, função, subfunção, programa, projeto/atividade, elemento e recurso.
- **Cuidados:** Não reutilizar esta consulta como catálogo geral de empenhos. Ela representa a visão autorizada para o usuário atual.

```sql
SELECT /* campos dinâmicos */
FROM empempenho
JOIN orcdotacao
  ON orcdotacao.o58_anousu = empempenho.e60_anousu
 AND orcdotacao.o58_coddot = empempenho.e60_coddot
JOIN db_permemp
  ON db20_anousu = o58_anousu
 AND db20_orgao = o58_orgao
 AND db20_unidade = o58_unidade
 AND db20_funcao = o58_funcao
 AND db20_subfuncao = o58_subfuncao
 AND db20_programa = o58_programa
 AND db20_projativ = o58_projativ
 AND db20_codele = o58_codele
 AND db20_codigo = o58_codigo
JOIN db_usupermemp
  ON db21_codperm = db20_codperm
 AND db21_id_usuario = :usuario_logado
WHERE /* filtro dinâmico */;
```

### Empenho, documentos e histórico: `sql_query_doc` e `sql_query_hist`

- **Objetivo:** Associar o empenho a lançamentos/documentos contábeis e ao histórico textual.
- **Caminho documental:** `empempenho -> conlancamemp -> conlancam -> conlancamdoc -> conhistdoc`.
- **Caminho do histórico:** `empempenho -> empemphist -> emphist`.
- **Diferença importante:**
  - `sql_query_doc` usa `LEFT JOIN` nos documentos, classificações auxiliares e histórico.
  - `sql_query_hist` exige credor, instituição, dotação, tipo, tipo de compra e classificações, mantendo apenas histórico como opcional.
- **Grão do resultado:** Pode haver várias linhas por empenho quando existirem vários lançamentos, documentos ou históricos.
- **Cuidados:** Para contar empenhos, usar `COUNT(DISTINCT e60_numemp)`.

### Restos a pagar: `sql_query_empresto`, `sql_query_encerramento_empresto` e `sql_query_resto`

- **Tabela de restos:** `empenho.empresto`.
- **Vínculo:** `empresto.e91_numemp = empempenho.e60_numemp`.
- **Regra de existência:**
  - `sql_query_empresto` usa `INNER JOIN` e retorna apenas empenhos que possuem registro em restos a pagar.
  - `sql_query_encerramento_empresto` usa `LEFT JOIN` e também permite localizar empenhos sem registro em restos.
- **Filtro padrão de `sql_query_resto`:** Quando recebe `e60_numemp` sem `$dbwhere`, restringe `empresto.e91_anousu` ao exercício `DB_anousu` da sessão.
- **Cuidados:** O exercício do resto (`e91_anousu`) e o exercício original do empenho (`e60_anousu`) têm papéis diferentes. Não assumir que são sempre iguais.

```sql
SELECT /* campos dinâmicos */
FROM empresto
JOIN empempenho
  ON empresto.e91_numemp = empempenho.e60_numemp
JOIN cgm
  ON cgm.z01_numcgm = empempenho.e60_numcgm
JOIN orcdotacao
  ON orcdotacao.o58_anousu = empempenho.e60_anousu
 AND orcdotacao.o58_coddot = empempenho.e60_coddot
WHERE empresto.e91_anousu = :exercicio_sessao
  AND empresto.e91_numemp = :numemp;
```

### Saldos do empenho: `sql_query_saldo`

- **Objetivo:** Obter valores consolidados do empenho, opcionalmente por elemento.
- **Fonte do cálculo:** Função PostgreSQL `fc_empsaldo(:numemp, :codele)`.
- **Parâmetros:**
  - `:numemp` - chave interna `e60_numemp`.
  - `:codele` - código do elemento; o padrão da classe é `0`.
- **Valores extraídos do retorno:** empenhado, anulado, liquidado, pago, processado e não processado.
- **Regra técnica:** A função retorna um texto posicional; a classe usa `substr(..., posição, 12)::float8`.
- **Cuidados:** A fórmula interna não está nesta classe. Não reproduzir o saldo apenas com os campos do cabeçalho sem analisar `fc_empsaldo`.

```sql
SELECT
  substr(saldo, 16, 12)::float8 AS e60_vlremp,
  substr(saldo, 29, 12)::float8 AS e60_vlranu,
  substr(saldo, 42, 12)::float8 AS e60_vlrliq,
  substr(saldo, 55, 12)::float8 AS e60_vlrpag,
  substr(saldo, 68, 12)::float8 AS vlr_proc,
  substr(saldo, 81, 12)::float8 AS vlr_nproc
FROM (
  SELECT fc_empsaldo(:numemp, :codele) AS saldo
) AS x;
```

### Estornos e movimentação contábil: `sql_query_buscaestornos`, `sql_query_buscaliquidacoes` e `sql_queryMovimentacaoPatrimonial`

- **Estorno/anulação:** `sql_query_buscaestornos` exige registro em `empenho.empanulado`, ligado por `empanulado.e94_numemp = empempenho.e60_numemp`.
- **Liquidação contábil:** `sql_query_buscaliquidacoes` percorre `conlancamemp`, `conlancam`, `conlancamdoc` e `conhistdoc`.
- **Movimentação patrimonial:** `sql_queryMovimentacaoPatrimonial` percorre `conlancamemp`, `conlancam` e `conlancamdoc`, além da classificação completa da dotação.
- **Grão do resultado:** Uma linha pode representar um documento ou lançamento associado, não necessariamente um empenho único.
- **Cuidados:** O nome `sql_query_buscaliquidacoes` não contém filtro fixo que sozinho classifique o lançamento como liquidação. A seleção depende dos campos e do `$dbwhere` fornecidos pelo consumidor.

### Materiais e itens adquiridos: `sql_query_impconsulta`, `sql_query_itemmaterial` e `sql_query_itensadquiridos`

- **Vínculo dos itens:** `empempitem.e62_numemp = empempenho.e60_numemp`.
- **Material:** `pcmater.pc01_codmater = empempitem.e62_item`.
- **Filtro padrão:** `pcmater.pc01_codmater = :codigo_material`.
- **Diferenças:**
  - `sql_query_impconsulta` consulta empenho, item, material, credor, dotação e tipo de compra.
  - `sql_query_itemmaterial` acrescenta órgão, unidade e uma ordem de pagamento opcional.
  - `sql_query_itensadquiridos` exige ordem de pagamento e a classificação orçamentária completa.
- **Grão do resultado:** Item de empenho combinado com seus relacionamentos. Um empenho com vários itens gera várias linhas.
- **Cuidados:** O `LEFT JOIN pagordem` em `sql_query_itemmaterial` preserva itens ainda sem ordem; o `INNER JOIN` em `sql_query_itensadquiridos` retorna apenas itens vinculados a ordem de pagamento.

### Saldo e origem dos itens: `sql_query_itens_consulta_empenho`

- **Objetivo:** Consultar itens do empenho com saldo e rastreamento até solicitação, processo de compras, licitação e orçamento vencedor.
- **Fonte do saldo por item:** `fc_saldoitensempenho(:numemp)`.
- **Vínculo ao item:** retorno `ricoditem = empempitem.e62_sequencial`.
- **Caminho principal:** empenho -> autorização -> item da autorização -> item do processo -> item da solicitação -> item da licitação -> orçamento/julgamento.
- **Regra comprovada de julgamento:** `pcorcamjulg.pc24_pontuacao = 1`.
- **Fallback de origem:** Também percorre `solicitemvinculo` para buscar um item pai e seu processo/licitação/orçamento.
- **Grão esperado:** Item do empenho, mas joins opcionais de compras podem multiplicar linhas quando houver mais de um relacionamento compatível.
- **Cuidados:** Para totalizar saldo, validar a cardinalidade antes de somar os valores retornados pela função.

### Ordem de material: `sql_query_codord`

- **Objetivo:** Relacionar o empenho com ordem de material e o CGM da ordem.
- **Vínculos:**
  - `matordemitem.m52_numemp = empempenho.e60_numemp`
  - `matordem.m51_codordem = matordemitem.m52_codordem`
  - `matordem.m51_numcgm = cgm.z01_numcgm`
- **Grão do resultado:** Ordem/item de ordem relacionado ao empenho.
- **Cuidados:** O credor retornado é o CGM vinculado à ordem de material, não necessariamente uma nova validação do `e60_numcgm`.

### Liberação do empenho: `sql_query_empnome` e `sql_query_liberarempenho`

- **Tabela:** `empenho.empempenholiberado`.
- **Vínculo opcional:** `empempenholiberado.e22_numemp = empempenho.e60_numemp`.
- **Regra comprovada:** O `LEFT JOIN` preserva empenhos sem registro de liberação.
- **Relacionamentos adicionais:** `sql_query_empnome` exige `empelemento`; ambos ligam o credor em `cgm`.
- **Cuidados:** A classe não define, neste método, qual valor de `empempenholiberado` significa liberado. Essa interpretação depende das colunas selecionadas e do filtro consumidor.

### Fonte de recurso e relatórios: `sql_query_relatorio`

- **Objetivo:** Montar dados completos do empenho para relatório, incluindo fonte de recurso e itens.
- **Origem do complemento:** `origemcomplementorecurso.o206_numero = empempenho.e60_numemp`.
- **Regra de origem:** `origemcomplementorecurso.o206_origem = 1`.
- **Fonte no exercício:** `fonterecurso.orctiporec_id = orctiporec.o15_codigo` e `fonterecurso.exercicio = orcdotacao.o58_anousu`.
- **Grão do resultado:** Item de empenho, podendo multiplicar por históricos ou fontes relacionadas.
- **Cuidados:** Não somar valores do cabeçalho após o join com `empempitem` sem controlar duplicidade.

### Processo administrativo: `sql_queryProcessoAdministrativo` e `sql_query_relatorio_processo_administrativo`

- **Caminho:** `empempenho -> empempaut -> empautoriza -> empautorizaprocesso`.
- **Vínculos:**
  - `empempaut.e61_numemp = empempenho.e60_numemp`
  - `empempaut.e61_autori = empautoriza.e54_autori`
  - `empautorizaprocesso.e150_empautoriza = empautoriza.e54_autori`
- **Regra comprovada:** Como os joins são internos, somente empenhos com autorização ligada a processo administrativo aparecem.
- **Relatório completo:** A variante `sql_query_relatorio_processo_administrativo` também exige item de empenho, fonte de recurso e toda a classificação da dotação.
- **Grão do resultado:** Pode haver mais de uma linha por empenho quando houver vários itens, autorizações ou processos.

### Contratos: `sql_query_empenhocontrato`

- **Objetivo:** Consultar vínculos do empenho com autorização e contrato.
- **Vínculos opcionais:**
  - `empempaut.e61_numemp = empempenho.e60_numemp`
  - `empautoriza.e54_autori = empempaut.e61_autori`
  - `empempenhocontrato.e100_numemp = empempenho.e60_numemp`
- **Regra comprovada:** Todos são `LEFT JOIN`; a consulta também retorna empenhos sem contrato.
- **Cuidados:** Para listar apenas empenhos contratados, o consumidor precisa filtrar uma coluna não nula de `empempenhocontrato`.

### Cota mensal: `sql_query_cota_mensal`

- **Objetivo:** Relacionar o empenho às cotas mensais e à dotação.
- **Vínculos:**
  - `empenhocotamensal.e05_numemp = empempenho.e60_numemp`
  - `(orcdotacao.o58_coddot, orcdotacao.o58_anousu) = (empempenho.e60_coddot, empempenho.e60_anousu)`
- **Grão do resultado:** Cota mensal do empenho.
- **Cuidados:** Um empenho pode gerar várias linhas, conforme a quantidade de cotas mensais.

### Classificação do credor: `sql_query_classificacao_credor`

- **Objetivo:** Recuperar o empenho e seu credor com classificação opcional.
- **Vínculos:**
  - `cgm.z01_numcgm = empempenho.e60_numcgm`
  - `classificacaocredoresempenho.cc31_empempenho = empempenho.e60_numemp`
  - `classificacaocredores.cc30_codigo = classificacaocredoresempenho.cc31_classificacaocredores`
- **Regra comprovada:** Os `LEFT JOIN` preservam empenhos sem classificação de credor.
- **Cuidados:** Não tratar ausência de classificação como uma categoria específica sem regra adicional.

### Classificação, liquidação e pagamento da nota: `sql_query_empenho_classificacao_nota`

- **Objetivo:** Alimentar relatório de empenhos por classificação de credores, combinando nota de liquidação, ordem de pagamento, movimento de pagamento, documento contábil, fonte de recurso e possível movimento bancário.
- **Grão do resultado:** Combinação de empenho, nota e ordem de pagamento; o relatório consumidor agrupa explicitamente esses campos.
- **Caminho financeiro:**
  - `empempenho -> empnota`
  - `empnota -> pagordemnota -> pagordemele -> pagordem`
  - `pagordem -> empord -> empagemov`
- **Caminho contábil da nota:** `empnota -> conlancamnota -> conlancam -> conlancamdoc -> conhistdoc`.
- **Regra de documento:** `conhistdoc.c53_tipo IN (20, 21)`.
- **Classificação obrigatória:** Nesta consulta, `classificacaocredoresempenho` e `classificacaocredores` são `INNER JOIN`; empenhos sem classificação não aparecem.
- **Dados opcionais:**
  - Processo da ordem em `pagordemprocesso`.
  - Movimento bancário em `corempagemov -> corrente`.
  - Justificativa do movimento em `empagemovjustificativa`.
- **Fonte de recurso:** Exige `origemcomplementorecurso.o206_origem = 1` e fonte do mesmo exercício do empenho.
- **Cuidados:** A classe aceita `$sWhere` contendo também `GROUP BY` e `ORDER BY`. A seleção de pagos, a pagar, datas e instituições é definida pelo relatório consumidor, não por filtros fixos deste método.

```sql
SELECT /* campos e agregações definidos pelo relatório */
FROM empempenho
JOIN empnota
  ON empnota.e69_numemp = empempenho.e60_numemp
JOIN pagordemnota
  ON pagordemnota.e71_codnota = empnota.e69_codnota
JOIN pagordemele
  ON pagordemele.e53_codord = pagordemnota.e71_codord
JOIN pagordem
  ON pagordem.e50_codord = pagordemele.e53_codord
JOIN empord
  ON empord.e82_codord = pagordem.e50_codord
JOIN empagemov
  ON empagemov.e81_codmov = empord.e82_codmov
JOIN conlancamnota
  ON conlancamnota.c66_codnota = empnota.e69_codnota
JOIN conlancam
  ON conlancam.c70_codlan = conlancamnota.c66_codlan
JOIN conlancamdoc
  ON conlancamdoc.c71_codlan = conlancam.c70_codlan
JOIN conhistdoc
  ON conhistdoc.c53_coddoc = conlancamdoc.c71_coddoc
 AND conhistdoc.c53_tipo IN (20, 21)
JOIN classificacaocredoresempenho
  ON classificacaocredoresempenho.cc31_empempenho = empempenho.e60_numemp
JOIN classificacaocredores
  ON classificacaocredores.cc30_codigo =
     classificacaocredoresempenho.cc31_classificacaocredores
WHERE /* filtros definidos pelo relatório */;
```

### Ordem de pagamento: `db_pagordem_classe.php`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_pagordem_classe.php`
- **Tabela central:** `pagordem`
- **Chave primaria:** `e50_codord`
- **Grão base:** Uma linha por ordem de pagamento; os joins com empenho, notas, movimento bancário e contabilidade podem multiplicar o resultado.

`pagordem` é o cabeçalho da ordem de pagamento associada ao empenho. A classe mostra que ela conecta o empenho a usuários, itens de pagamento, movimento de caixa, documento contábil, forma de pagamento, cheques e, em algumas consultas, à receita/fonte e à reserva.

#### Consulta: `sql_query`

- **Objetivo:** Ler a ordem de pagamento com o empenho, o usuário criador, o credor e a dotação do empenho.
- **Tabelas:** `pagordem`, `db_usuarios`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`
- **Junções:**
  - `db_usuarios.id_usuario = pagordem.e50_id_usuario`
  - `empempenho.e60_numemp = pagordem.e50_numemp`
  - `cgm.z01_numcgm = empempenho.e60_numcgm`
  - `db_config.codigo = empempenho.e60_instit`
  - `orcdotacao.(o58_anousu, o58_coddot) = (empempenho.e60_anousu, empempenho.e60_coddot)`
  - `pctipocompra.pc50_codcom = empempenho.e60_codcom`
  - `emptipo.e41_codtipo = empempenho.e60_codtipo`
  - `concarpeculiar.c58_sequencial = empempenho.e60_concarpeculiar`
- **Cuidados:** a ordem de pagamento não é independente do empenho; a maior parte do significado vem do cabeçalho do empenho vinculado.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler somente `pagordem`.
- **Uso prático:** base neutra para auditoria de chaves e filtro direto por ordem.

#### Consulta: `sql_query_cheques`

- **Objetivo:** Expor a ordem com itens, movimento bancário, configuração de pagamento e vínculos de cheque.
- **Tabelas principais:** `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `orctiporec`, `emptipo`, `empord`, `empagemov`, `empagemovforma`, `empage`, `corempagemov`, `empageconf`, `empageconfche`, `pagordemconta`, `empageconfgera`
- **Regra de negócio:** a consulta trabalha no nível da ordem e de seus movimentos, permitindo rastrear o caminho até a forma de pagamento e a conta vinculada.
- **Cuidados:** o parâmetro `$sJoin` permite extensões arbitrárias do SQL; não usar essa consulta como base “fixa” sem revisar o join extra.

#### Consulta: `sql_query_emp`

- **Objetivo:** Retornar a ordem com o empenho e o credor, com expansão opcional para `pagordemele`.
- **Tabelas:** `pagordem`, `empempenho`, `cgm`, `pagordemele`
- **Uso prático:** visão enxuta da ordem associada ao empenho, útil para telas e relatórios simples.

#### Consulta: `sql_query_empagemovforma`

- **Objetivo:** Relacionar ordem, movimento bancário, forma de pagamento, fonte de recurso e registros auxiliares de caixa.
- **Tabelas principais:** `empage`, `empagemov`, `empord`, `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `orctiporec`, `fonterecurso`, `emptipo`, `empresto`, `empageconcarpeculiar`, `corempagemov`, `empagemovconta`, `empageconf`, `empageconfche`, `pagordemconta`, `empagemovforma`, `empagepag`, `empagetipo`, `pagordemnota`, `empnota`, `corgrupocorrente`
- **Regra comprovada:** a ordem é resolvida a partir do movimento bancário (`empord -> pagordem`), não apenas do cabeçalho da ordem.
- **Cuidados:** essa é uma das consultas com maior cardinalidade, porque junta ordem, movimento, forma, nota, conta e corrente.

#### Consulta: `sql_query_impconsulta`

- **Objetivo:** Consultar a ordem com empenho, itens do empenho, material, credor, dotação e tipo de compra.
- **Tabelas:** `pagordem`, `empempenho`, `empempitem`, `pcmater`, `cgm`, `orcdotacao`, `pctipocompra`
- **Regra:** o item do empenho entra por `empempitem.e62_numemp = empempenho.e60_numemp`.

#### Consulta: `sql_query_notaliquidacao`

- **Objetivo:** Retornar a ordem e sua nota de liquidação com parâmetros posicionais.
- **Tabelas:** `pagordem`, `db_usuarios`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`, `pagordemnota`, `empnota`
- **Diferencial:** esta é a única consulta da classe que retorna também a lista de parâmetros, usando placeholders numerados.
- **Cuidados:** o método monta `WHERE pagordem.e50_codord = $N` conforme a quantidade de parâmetros informados; o consumidor precisa repassar os binds na mesma ordem.

#### Consulta: `sql_query_pag`

- **Objetivo:** Retornar a ordem com o caminho contábil do pagamento.
- **Tabelas:** `pagordem`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `conlancamord`, `conlancampag`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conplanoreduz`, `conplano`, `pagordemconta`
- **Regra de negócio:** a ordem pode ser rastreada até o lançamento contábil e a conta reduzida usada no pagamento.
- **Cuidados:** o join com `conlancamord` e `conlancampag` aumenta fortemente a multiplicação por movimento e por plano.

#### Consulta: `sql_query_pagordemagenda`

- **Objetivo:** Ligar a ordem ao movimento de agenda/caixa.
- **Tabelas:** `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `empord`, `empagemov`, `empage`
- **Uso prático:** caminho útil quando a pergunta é sobre a agenda do pagamento e não apenas o cabeçalho da ordem.

#### Consulta: `sql_query_pagordemele`, `sql_query_pagordemele2` e `sql_query_pagordemeleempage`

- **Objetivo:** Expandir a ordem pelo detalhe `pagordemele` e pelo movimento bancário relacionado.
- **Tabelas recorrentes:** `pagordem`, `pagordemele`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `orctiporec`, `emptipo`, `empord`, `empagemov`, `empageconf`, `empageconfgera`, `pagordemconta`
- **Regra observada:** a versão `sql_query_pagordemeleempage` amarra `empord` e `empagemov` diretamente, deixando explícito o movimento que originou a ordem.
- **Cuidados:** essas variantes diferem mais pela estratégia de join do que pelo negócio; o grão final pode mudar bastante.

#### Consulta: `sql_query_pagDiversos`

- **Objetivo:** Trazer o caminho financeiro/contábil da ordem para pagamentos de diversos.
- **Tabelas:** `pagordem`, `empempenho`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `conlancamord`, `conlancampag`, `conlancam`, `conlancamdoc`, `conhistdoc`, `conplanoreduz`, `conplano`, `pagordemele`, `pagordemconta`
- **Regra de negócio:** a consulta cruza a ordem com o lançamento contábil e o plano reduzido, além de detalhes da ordem.

#### Consulta: `sql_query_movimento`

- **Objetivo:** Retornar o movimento bancário associado à ordem.
- **Tabelas:** `pagordem`, `empord`, `empagemov`
- **Uso prático:** consulta curta para localizar o movimento que fecha a ordem.

#### Consulta: `sql_query_empenho_rp`

- **Objetivo:** Verificar o vínculo da ordem com `empresto`, sugerindo rotina de restos a pagar/registro de comprometimento.
- **Tabelas:** `pagordem`, `empresto`
- **Cuidados:** o nome sugere um recorte funcional específico; a classe aqui só expõe o vínculo direto por número do empenho.

### Cuidados gerais das consultas extraídas

- `e60_numemp` é a chave interna; `e60_codemp` é o número textual exibido do empenho.
- Campos e ordenações são inseridos diretamente nas SQLs pelos parâmetros da classe.
- `$dbwhere` substitui o filtro padrão por número do empenho.
- A presença de joins com itens, históricos, documentos, fontes, autorizações ou pagamentos pode multiplicar linhas.
- Para contar empenhos, preferir `COUNT(DISTINCT empempenho.e60_numemp)`.
- Para somar valores do cabeçalho, agregar antes dos relacionamentos um-para-muitos ou controlar a cardinalidade.
- `sql_query_saldo` depende de `fc_empsaldo`; `sql_query_itens_consulta_empenho` depende de `fc_saldoitensempenho`.
- Nomes de métodos como `buscaliquidacoes`, `liberarempenho` ou `itensadquiridos` indicam a finalidade da tela, mas a regra final também depende do `$dbwhere` fornecido pelo consumidor.
