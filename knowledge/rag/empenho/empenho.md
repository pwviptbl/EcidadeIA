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
