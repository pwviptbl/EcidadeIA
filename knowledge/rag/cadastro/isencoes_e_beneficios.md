## cadastro.isencoes_e_beneficios

> Fonte manual: `knowledge/manual/cadastro/isencoes_e_beneficios.md`

Mapeia isenções, imunidades e descontos concedidos no cálculo do IPTU.

---

### Conceito: isencao_iptu
- **Descrição:** Registra se houve concessão de isenção de IPTU para a matrícula.
- **Tabelas:** `cadastro.iptucalc`
- **Filtro de Negócio:** `COALESCE(iptucalc.j23_vlrisen, 0) > 0` (Valor da isenção superior a zero).
- **Ano da Isenção:** `iptucalc.j23_anousu = :ano`.

---

### Receita: `calculo_isencao_iptu_bairro`
- **Descrição:** Contabiliza imóveis isentos ou a soma do valor total isentado por bairro territorial.
- **Tabelas:** `cadastro.bairro`, `cadastro.lote`, `cadastro.iptubase`, `cadastro.iptucalc`
- **Junções:**
  - `bairro.j13_codi = lote.j34_bairro`
  - `lote.j34_idbql = iptubase.j01_idbql`
  - `iptubase.j01_matric = iptucalc.j23_matric`
- **Filtro de Negócio:**
  - Isenção ativa: `COALESCE(iptucalc.j23_vlrisen, 0) > 0`
  - Ano específico: `iptucalc.j23_anousu = :ano`
- **Regras de Agregação:**
  - Quantidade de imóveis isentos: `COUNT(DISTINCT j23_matric)`
  - Valor total isento: `SUM(j23_vlrisen)`
- **Exemplo SQL:**
  ```sql
  SELECT b.j13_descr AS bairro, COUNT(DISTINCT c.j23_matric) AS total_isentos, SUM(c.j23_vlrisen) AS valor_total_isento
  FROM cadastro.bairro b
  JOIN cadastro.lote l ON b.j13_codi = l.j34_bairro
  JOIN cadastro.iptubase i ON l.j34_idbql = i.j01_idbql
  JOIN cadastro.iptucalc c ON i.j01_matric = c.j23_matric
  WHERE c.j23_anousu = 2025
    AND COALESCE(c.j23_vlrisen, 0) > 0
  GROUP BY b.j13_descr;
  ```
