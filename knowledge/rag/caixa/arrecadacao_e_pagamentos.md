## caixa.arrecadacao_e_pagamentos

> Fonte manual: `knowledge/manual/caixa/arrecadacao_e_pagamentos.md`

Mapeia as relações financeiras do IPTU, vinculando o cadastro imobiliário com a arrecadação em caixa, pagamentos e taxas de inadimplência.

---

### Conceito: ligacao_iptu_arrecadacao
- **Descrição:** Vínculo base das matrículas de IPTU (cadastro) com os débitos e pagamentos na arrecadação (caixa).
- **Tabelas:** `cadastro.iptubase`, `cadastro.iptunump`, `caixa.arrecad`, `caixa.arrepaga`
- **Junções:**
  - `iptubase.j01_matric = iptunump.j20_matric`
  - `iptunump.j20_numpre = arrecad.k00_numpre`
  - `arrecad.k00_numpre = arrepaga.k00_numpre` AND `arrecad.k00_numpar = arrepaga.k00_numpar` (Junção por prestação e parcela).

---

### Receita: `arrecadacao_iptu_por_periodo`
- **Descrição:** Calcula o valor de IPTU efetivamente arrecadado (pago) em determinado período ou exercício.
- **Tabelas:** `cadastro.iptubase`, `cadastro.iptunump`, `caixa.arrepaga`, `cadastro.iptucalv`, `cadastro.iptucalh`
- **Junções:**
  - `iptubase.j01_matric = iptunump.j20_matric`
  - `iptunump.j20_numpre = arrepaga.k00_numpre`
  - `iptubase.j01_matric = iptucalv.j21_matric` AND `iptunump.j20_anousu = iptucalv.j21_anousu`
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- **Filtro de Negócio (Rigor Tributário):**
  - Isolar IPTU: `iptucalh.j17_descr = 'IPTU'`
  - Ano de Operação/Exercício: `iptunump.j20_anousu = :ano` (ou usar data específica `arrepaga.k00_dtpaga BETWEEN :data_inicio AND :data_fim`).
- **Regra de Agregação:** `SUM(arrepaga.k00_valor)`.

---

### Receita: `comparacao_iptu_pago_vs_calculado`
- **Descrição:** Permite analisar o valor lançado (calculado) contra o valor efetivamente pago de IPTU.
- **Tabelas:** `cadastro.bairro`, `cadastro.lote`, `cadastro.iptubase`, `cadastro.iptucalv`, `cadastro.iptunump`, `caixa.arrepaga`
- **Atenção:** Nunca junte `caixa.arrepaga` diretamente a `cadastro.iptucalh`.
- **Passo a passo (Joins):**
  1. `bairro.j13_codi = lote.j34_bairro`
  2. `lote.j34_idbql = iptubase.j01_idbql`
  3. `iptubase.j01_matric = iptucalv.j21_matric`
  4. `iptubase.j01_matric = iptunump.j20_matric`
  5. `iptunump.j20_numpre = arrepaga.k00_numpre`
- **Regras:** O calculado vem de `iptucalv.j21_valor` e o pago de `arrepaga.k00_valor`.

---

### Receita: `calculo_taxa_inadimplencia_iptu`
- **Descrição:** Calcula o valor inadimplente e a taxa de inadimplência de IPTU por exercício ou bairro.
- **Regra de Negócio Crucial (Efeito Multiplicador / Fan-out):**
  - **Débitos em Aberto (Não Pagos):** Ficam na tabela `caixa.arrecad`. O valor em aberto é a soma de `caixa.arrecad.k00_valor`.
  - **Débitos Pagos:** Ficam na tabela `caixa.arrepaga` e saem de `arrecad` após quitados.
  - **Valor Lançado/Calculado:** Vem de `cadastro.iptucalv.j21_valor` (imposto total originalmente calculado).
  - **Cálculo da Taxa:** O percentual de inadimplência é `(SUM(valor_aberto) / SUM(valor_lancado)) * 100`.
  - **Prevenção do Efeito Multiplicador:** Como a divisão em parcelas de `arrecad` multiplica as linhas em relação à `iptucalv`, **SEMPRE** calcule as agregações (Total Lançado e Total Aberto) de forma independente em CTEs separadas antes de efetuar o JOIN final, para evitar a multiplicação errônea de valores.
- **Junções:**
  - `cadastro.bairro -> cadastro.lote -> cadastro.iptubase`
  - `cadastro.iptubase -> cadastro.iptucalv` (Calculado)
  - `cadastro.iptubase -> cadastro.iptunump -> caixa.arrecad` (Aberto)
