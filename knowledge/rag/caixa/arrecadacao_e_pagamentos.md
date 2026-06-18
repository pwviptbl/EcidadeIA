## caixa.arrecadacao_e_pagamentos

> Fonte manual: `knowledge/manual/caixa/arrecadacao_e_pagamentos.md`

Mapeia as relações financeiras da arrecadação e caixa, incluindo os vínculos com contribuintes (CGM), imóveis (matrículas), empresas (inscrições), e as classificações de tipos e grupos de débitos.

---

### Conceito: vinculo_cgm
- **Descrição:** Vínculo base de débitos com o Cadastro Geral de Contribuintes (CGM) do contribuinte correspondente.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arrenumcgm`, `protocolo.cgm`
- **Junções:**
  - `arrecad.k00_numpre = arrenumcgm.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arrenumcgm.k00_numpre` (para pagamentos)
  - `arrenumcgm.k00_numcgm = cgm.z01_numcgm`

---

### Conceito: vinculo_matricula
- **Descrição:** Vínculo base de débitos (como IPTU e taxas imobiliárias) com a matrícula do imóvel no Cadastro Imobiliário Municipal.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arrematric`, `cadastro.iptubase`
- **Junções:**
  - `arrecad.k00_numpre = arrematric.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arrematric.k00_numpre` (para pagamentos)
  - `arrematric.k00_matric = iptubase.j01_matric`

---

### Conceito: vinculo_inscricao
- **Descrição:** Vínculo de débitos (como ISSQN, taxas de alvará e tributos mobiliários) com a inscrição da empresa/atividade econômica no Cadastro Mobiliário Municipal.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arreinscr`, `issqn.issbase`
- **Junções:**
  - `arrecad.k00_numpre = arreinscr.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arreinscr.k00_numpre` (para pagamentos)
  - `arreinscr.k00_inscr = issbase.q02_inscr`

---

### Conceito: tipo_e_grupo_debito
- **Descrição:** Classificação dos débitos por tipo específico (arretipo) e grupo geral (cadtipo). O grupo do tipo (`cadtipo`) é fixo e global para todos os clientes, enquanto os tipos derivados (`arretipo`) são customizados por cada município.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arretipo`, `caixa.cadtipo`
- **Junções:**
  - `arrecad.k00_tipo = arretipo.k00_tipo` (ou `arrepaga.k00_tipo = arretipo.k00_tipo`)
  - `arretipo.k03_tipo = cadtipo.k03_tipo`
- **Regra de Negócio:** `cadtipo` representa a categoria geral padronizada (ex: IPTU, ISSQN, Taxas, etc.), enquanto `arretipo` possui a descrição e regras locais parametrizadas pelo município. Para análises globais consistentes entre clientes, deve-se agrupar ou filtrar pelo grupo `cadtipo.k03_tipo`.

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
