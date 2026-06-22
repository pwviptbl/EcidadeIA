## issqn.isscalc

> Fonte de código: `/var/www/html/e-cidade-php74/classes/db_isscalc_classe.php`

Registra resultados de cálculo do ISSQN por exercício, inscrição, tipo de cálculo, receita e número de arrecadação. A situação financeira atual do débito deve ser obtida nas tabelas de arrecadação.

### Resumo técnico

- **Classe:** `cl_isscalc`
- **Tabela principal:** `isscalc`
- **Chave composta:** `q01_anousu`, `q01_inscr`, `q01_cadcal`, `q01_recei`, `q01_numpre`
- **Exercício:** `q01_anousu`
- **Inscrição municipal:** `q01_inscr`
- **Tipo/cadastro de cálculo:** `q01_cadcal`
- **Receita:** `q01_recei`
- **Número de arrecadação:** `q01_numpre`
- **Valor calculado:** `q01_valor`
- **Valor de isenção:** `q01_valorisencao`
- **Memória/log do cálculo:** `q01_manual`
- **Grão:** Resultado de cálculo para uma inscrição, receita, tipo de cálculo e número de arrecadação em um exercício.

### Cuidados sobre `q01_valor`

- Em cálculos fixos, consumidores tratam `q01_valor` como valor calculado.
- Em alguns fluxos variáveis, consumidores exibem `q01_valor` como alíquota.
- Não interpretar `q01_valor` sem considerar `q01_cadcal` e a rotina consumidora.
- Evidências locais identificam `q01_cadcal = 2` como ISSQN fixo e `q01_cadcal = 3` como ISSQN variável.
- `q01_valorisencao` é separado de `q01_valor`; não presumir que o valor líquido seja sempre a subtração direta sem validar a rotina de cálculo.

---

### Consulta completa do cálculo: `sql_query`

- **Objetivo:** Recuperar o cálculo com inscrição, contribuinte, configuração de cálculo, receita, vencimento, fórmula e juros/multa.
- **Junções obrigatórias:**
  - `issbase.q02_inscr = isscalc.q01_inscr`
  - `cadcalc.q85_codigo = isscalc.q01_cadcal`
  - `tabrec.k02_codigo = isscalc.q01_recei`
  - `cgm.z01_numcgm = issbase.q02_numcgm`
  - `cadvencdesc.q92_codigo = cadcalc.q85_codven`
  - `forcaldesc.q87_codigo = cadcalc.q85_forcal`
  - `tabrecjm.k02_codjm = tabrec.k02_codjm`
- **Filtros opcionais:** Todos os componentes da chave composta.
- **Grão:** Uma linha de cálculo, desde que os cadastros relacionados sejam únicos.
- **Cuidados:** Como todos os joins são internos, inconsistências de configuração podem ocultar um registro existente em `isscalc`.

```sql
SELECT /* campos dinâmicos */
FROM isscalc
JOIN issbase ON issbase.q02_inscr = isscalc.q01_inscr
JOIN cadcalc ON cadcalc.q85_codigo = isscalc.q01_cadcal
JOIN tabrec ON tabrec.k02_codigo = isscalc.q01_recei
JOIN cgm ON cgm.z01_numcgm = issbase.q02_numcgm
JOIN cadvencdesc ON cadvencdesc.q92_codigo = cadcalc.q85_codven
JOIN forcaldesc ON forcaldesc.q87_codigo = cadcalc.q85_forcal
JOIN tabrecjm ON tabrecjm.k02_codjm = tabrec.k02_codjm
WHERE isscalc.q01_anousu = :exercicio
  AND isscalc.q01_inscr = :inscricao
  AND isscalc.q01_cadcal = :tipo_calculo
  AND isscalc.q01_recei = :receita
  AND isscalc.q01_numpre = :numpre;
```

### Leitura física: `sql_query_file`

- **Objetivo:** Consultar diretamente `isscalc` sem depender dos cadastros auxiliares.
- **Filtros opcionais:** Exercício, inscrição, cálculo, receita e número de arrecadação.
- **Uso recomendado:** Somar resultados, consultar memória do cálculo ou verificar registro mesmo quando alguma configuração relacionada estiver ausente.

### Cálculo com débito em aberto: `sql_query_arrecad`

- **Vínculo:** `arrecad.k00_numpre = isscalc.q01_numpre`.
- **Regra comprovada:** O `INNER JOIN` retorna somente cálculos cujo número de arrecadação ainda possui linha em `arrecad`.
- **Grão:** Pode multiplicar o cálculo por parcelas e receitas existentes no mesmo `numpre`.
- **Cuidados:**
  - O join fixo usa apenas `k00_numpre`; ele não restringe parcela nem receita.
  - Para relacionar a receita exata, acrescentar `arrecad.k00_receit = isscalc.q01_recei`.
  - Para contar cálculos, usar a chave composta ou `DISTINCT`.
  - A ausência em `arrecad` não prova pagamento: o débito também pode estar cancelado, compensado, migrado ou em outra situação.

```sql
SELECT /* campos dinâmicos */
FROM isscalc
JOIN arrecad
  ON arrecad.k00_numpre = isscalc.q01_numpre
WHERE /* filtros do cálculo e do débito */;
```

---

### Consolidação de ISSQN e vistorias: `sql_queryIssqnVistorias`

- **Objetivo:** Alimentar o Relatório de Lançamentos Tributários, consolidando valores por tipo de débito e receita.
- **Parâmetro:** `:ano_calculo`.
- **Grão final:** Tipo de débito e receita.
- **Campos consolidados:**
  - `valor_calculado`
  - `valor_importado`
  - `valor_pago`
  - `valor_cancelado`
  - `valor_a_pagar`
  - `valor_compensado`
  - `quantidade`
- **Ordenação:** Descrição do tipo de débito.

O método combina dois blocos com `UNION ALL`.

#### Bloco 1: cálculos de `isscalc`

- **Filtro:** `q01_anousu = :ano_calculo AND q01_cadcal = 2`.
- **Evidência de domínio:** Outros consumidores identificam `q01_cadcal = 2` como ISSQN fixo.
- **Valor calculado:** `isscalc.q01_valor`.
- **Tipo de débito:** `cadcalc.q85_codigo/q85_descr`.
- **Receita:** `tabrec.k02_codigo/k02_descr`.
- **Quantidade:** Uma unidade por registro de cálculo.
- **Valor em aberto:** Soma de `arrecad.k00_valor` pelo `q01_numpre`.
- **Valor importado:** Soma de `arreold.k00_valor` por número de arrecadação e receita.
- **Valor cancelado:** Histórico `arrecant` ligado a `cancdebitosreg -> cancdebitosprocreg`.

#### Bloco 2: vistorias com número de arrecadação

- **Caminho:** `vistorias -> vistorianumpre -> vistinscr`.
- **Exercício:** `EXTRACT(YEAR FROM vistorias.y70_data) = :ano_calculo`.
- **Estados financeiros:** Obtidos por `LEFT JOIN` com `arrecad`, `arrepaga` e `arrecant`.
- **Receita/tipo de débito:** Escolhidos pelo primeiro valor não nulo entre aberto, pago e histórico.
- **Quantidade:** `1` quando existe `vistinscr.y71_inscr`, senão `0`.
- **Filtro final do bloco:** Exige algum valor aberto, pago, cancelado ou compensado diferente de zero.
- **Valor calculado reconstruído:** Soma de aberto, pago e cancelado.

#### Pagamento

O valor pago considera:

- Valor histórico em `arrecant` quando existe correspondente em `arrepaga`.
- Exclui parcelas utilizadas como crédito (`TIPO_CREDITO = 3`) para não duplicar.
- Acrescenta abatimentos de pagamento parcial (`TIPO_PAGAMENTO_PARCIAL = 1`) em registros abertos e históricos.

#### Compensação

O valor compensado combina:

- Uso de crédito por `abatimentoutilizacaodestino -> abatimentoutilizacao -> abatimento`, com `TIPO_CREDITO = 3`.
- Compensação vinculada a `arreckey -> abatimentoarreckey`, com `TIPO_COMPENSACAO = 4`.

#### Cancelamento

- Usa `arrecant` ligado a `cancdebitosreg` e `cancdebitosprocreg`.
- No primeiro bloco existe `SUM(COALESCE(arrecant.k00_valor, 2))`.
- **Anomalia:** O fallback `2` adicionaria valor quando `k00_valor` fosse nulo. Como o campo vem de `arrecant`, esse comportamento deve ser tratado como suspeito e não reproduzido em nova SQL sem validação.

#### SQL normalizada

```sql
SELECT
  codigo_tipodebito,
  tipodebito,
  codigo_receita,
  receita,
  COALESCE(ROUND(SUM(valor_calculado), 2), 0) AS valor_calculado,
  COALESCE(ROUND(SUM(valor_importado), 2), 0) AS valor_importado,
  COALESCE(ROUND(SUM(valor_pago), 2), 0) AS valor_pago,
  COALESCE(ROUND(SUM(valor_cancelado), 2), 0) AS valor_cancelado,
  COALESCE(ROUND(SUM(valor_a_pagar), 2), 0) AS valor_a_pagar,
  COALESCE(ROUND(SUM(valor_compensado), 2), 0) AS valor_compensado,
  SUM(quantidade) AS quantidade
FROM (
  /* isscalc do exercício com q01_cadcal = 2 */
  UNION ALL
  /* vistorias do exercício ligadas a numpre */
) AS x
GROUP BY
  codigo_tipodebito,
  tipodebito,
  codigo_receita,
  receita
ORDER BY tipodebito;
```

### Cuidados gerais

- Não usar `isscalc` sozinho para concluir se um débito está pago ou em aberto.
- `q01_numpre` liga o cálculo ao ciclo de arrecadação.
- Para vínculo exato com parcela/receita, complementar as chaves de `arrecad`, `arrepaga` e `arrecant`.
- `valor_calculado` do relatório não tem a mesma origem nos dois blocos: no primeiro é `q01_valor`; no segundo é reconstruído por estados financeiros.
- O nome `sql_queryIssqnVistorias` abrange ISSQN fixo e vistorias, não apenas vistorias.
- Valores compensados e pagamentos parciais devem ser tratados separadamente para evitar dupla contagem.
- `q01_manual` contém memória textual do cálculo e pode ser útil para auditoria, mas não deve ser agregado como dimensão financeira.
- Para cadastro e situação da inscrição, consultar `knowledge/rag/issqn/issbase.md`.
