## caixa.iptu

Mapeia as regras de negócio para cálculo, lançamento, arrecadação e inadimplência do Imposto Predial e Territorial Urbano (IPTU).

---

### Conceitos & Relacionamentos Base (REGRAS DE NEGÓCIO)
- **Cálculo de IPTU:** `cadastro.iptubase -> cadastro.iptunump -> cadastro.iptucalv -> cadastro.iptucalh`
- **Valores Lançados (Calculado):** `cadastro.iptucalv.j21_valor` (imposto total originalmente calculado).
- **Valores Efetivamente Pagos:** `caixa.arrepaga.k00_valor` (juntando via `iptunump.j20_numpre = arrepaga.k00_numpre`).
- **Valores em Aberto (Inadimplência / Débitos / Não Pagos):** `caixa.arrecad.k00_valor`. Para achar inadimplentes, você **deve cruzar** o IPTU com a tabela `caixa.arrecad` usando `iptunump.j20_numpre = arrecad.k00_numpre`. A tabela `arrecad` só guarda as parcelas que **não foram pagas** (em aberto).

> [!IMPORTANT]
> **Regra de Ouro para Inadimplência:** Sempre que a pergunta envolver "inadimplência", "não pagos", ou "débitos", NÃO USE a tabela de cálculo (`iptucalv`) para somar valores. Você OBRIGATORIAMENTE deve usar a tabela `caixa.arrecad` cruzando com `cadastro.iptunump`.
>
> **Prevenção do Efeito Multiplicador:** Nunca faça JOIN direto entre tabelas agregadas de parcelas (`caixa.arrecad`/`caixa.arrepaga`) e tabelas de cálculo (`cadastro.iptucalv`) sem usar subconsultas ou CTEs separadas. Caso contrário, os valores se multiplicarão devido ao número de parcelas.

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Qual é o valor total de IPTU lançado/calculado para um determinado exercício?
- **Descrição:** Calcula o montante total de imposto IPTU originalmente lançado para o ano desejado.
- **Receita SQL:**
```sql
SELECT SUM(c.j21_valor) as total_calculado
FROM cadastro.iptucalv c
JOIN cadastro.iptucalh h ON c.j21_codhis = h.j17_codhis
WHERE c.j21_anousu = :ano
  AND h.j17_descr = 'IPTU';
```

#### 2. Qual bairro concentra o maior valor de IPTU total calculado no ano?
- **Descrição:** Classifica os bairros com maior volume de IPTU lançado.
- **Receita SQL:**
```sql
SELECT b.j13_descr as bairro, SUM(cv.j21_valor) as total_calculado
FROM cadastro.iptubase ib
JOIN cadastro.iptucalv cv ON ib.j01_matric = cv.j21_matric
JOIN cadastro.iptucalh ch ON cv.j21_codhis = ch.j17_codhis
JOIN cadastro.lote l ON ib.j01_idbql = l.j34_idbql
JOIN cadastro.bairro b ON l.j34_bairro = b.j13_codi
WHERE cv.j21_anousu = :ano
  AND ch.j17_descr = 'IPTU'
GROUP BY b.j13_descr
ORDER BY total_calculado DESC
LIMIT 1;
```

#### 3. Qual foi o valor total de IPTU efetivamente pago pelos contribuintes em um exercício?
- **Descrição:** Calcula o valor de IPTU que já entrou no caixa da prefeitura para determinado ano de referência.
- **Receita SQL:**
```sql
SELECT SUM(ap.k00_valor) as total_arrecadado
FROM cadastro.iptunump n
JOIN caixa.arrepaga ap ON n.j20_numpre = ap.k00_numpre
JOIN cadastro.iptucalv c ON n.j20_matric = c.j21_matric AND n.j20_anousu = c.j21_anousu
JOIN cadastro.iptucalh h ON c.j21_codhis = h.j17_codhis
WHERE n.j20_anousu = :ano
  AND h.j17_descr = 'IPTU';
```

#### 4. Qual é a taxa de inadimplência (soma em aberto / soma calculada) de IPTU por bairro?
- **Descrição:** Calcula o percentual de valores não pagos de IPTU para um exercício agrupado por bairro, prevenindo o efeito fan-out.
- **Receita SQL:**
```sql
WITH calculado_bairro AS (
  SELECT b.j13_codi, b.j13_descr as bairro, SUM(cv.j21_valor) as total_calculado
  FROM cadastro.iptubase ib
  JOIN cadastro.iptucalv cv ON ib.j01_matric = cv.j21_matric
  JOIN cadastro.iptucalh ch ON cv.j21_codhis = ch.j17_codhis
  JOIN cadastro.lote l ON ib.j01_idbql = l.j34_idbql
  JOIN cadastro.bairro b ON l.j34_bairro = b.j13_codi
  WHERE cv.j21_anousu = :ano
    AND ch.j17_descr = 'IPTU'
  GROUP BY b.j13_codi, b.j13_descr
),
aberto_bairro AS (
  SELECT b.j13_codi, SUM(arr.k00_valor) as total_aberto
  FROM cadastro.iptubase ib
  JOIN cadastro.iptunump np ON ib.j01_matric = np.j20_matric
  JOIN caixa.arrecad arr ON np.j20_numpre = arr.k00_numpre
  JOIN cadastro.lote l ON ib.j01_idbql = l.j34_idbql
  JOIN cadastro.bairro b ON l.j34_bairro = b.j13_codi
  WHERE np.j20_anousu = :ano
  GROUP BY b.j13_codi
)
SELECT 
  cb.bairro,
  cb.total_calculado,
  COALESCE(ab.total_aberto, 0) as total_aberto,
  ROUND((COALESCE(ab.total_aberto, 0) / cb.total_calculado) * 100, 2) as percentual_inadimplencia
FROM calculado_bairro cb
LEFT JOIN aberto_bairro ab ON cb.j13_codi = ab.j13_codi
ORDER BY percentual_inadimplencia DESC;
```
