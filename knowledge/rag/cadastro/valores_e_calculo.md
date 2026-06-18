## cadastro.valores_e_calculo

> Fonte manual: `knowledge/manual/cadastro/valores_e_calculo.md`

Mapeia as regras relativas ao cálculo do IPTU, taxas correlatas e comparações anuais.

---

### Conceito: iptu_calculado
- **Descrição:** Valor final classificado como imposto territorial urbano (IPTU) gerado no cálculo de um exercício.
- **Tabelas:** `cadastro.iptucalv`, `cadastro.iptucalh`
- **Junções:**
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- **Filtro de Negócio (Rigor Tributário):**
  - É obrigatório filtrar `iptucalh.j17_descr = 'IPTU'` usando igualdade para isolar o imposto.
  - Filtrar pelo ano na coluna `iptucalv.j21_anousu = :ano`.
- **Vínculo Territorial (Bairro/Lote/Matrícula):** Para cruzar o IPTU calculado com os bairros territoriais, use o caminho:
  1. `cadastro.bairro -> cadastro.lote` (`bairro.j13_codi = lote.j34_bairro`)
  2. `cadastro.lote -> cadastro.iptubase` (`lote.j34_idbql = iptubase.j01_idbql`)
  3. `cadastro.iptubase -> cadastro.iptucalv` (`iptubase.j01_matric = iptucalv.j21_matric`)
- **Regra de Agregação:** `SUM(j21_valor)`.

---

### Receita: `taxas_acessorias_calculadas`
- **Descrição:** Soma valores de taxas associadas lançadas no carnê (como taxa de lixo ou taxa de expediente), excluindo o IPTU principal.
- **Tabelas:** `cadastro.iptucalv`, `cadastro.iptucalh`
- **Junções:**
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- **Filtro de Negócio:**
  - Excluir o IPTU: `iptucalh.j17_descr <> 'IPTU'`
  - Filtrar pelo ano na coluna `iptucalv.j21_anousu = :ano`.
- **Regra de Agregação:** `SUM(j21_valor)`.

---

### Receita: `top_imoveis_maior_iptu`
- **Descrição:** Lista ou rankeia os imóveis que possuem as maiores cobranças de IPTU em determinado ano.
- **Tabelas:** `cadastro.iptucalv`, `cadastro.iptucalh`
- **Junções:**
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
- **Filtro de Negócio:**
  - `iptucalh.j17_descr = 'IPTU'`
  - `iptucalv.j21_anousu = :ano`
- **Regra de Ordenação:** `SUM(j21_valor) DESC` agrupando por `j21_matric`.

---

### Conceito: comparacao_iptu_entre_exercicios
- **Descrição:** Análise da variação do IPTU calculado entre dois exercícios e fatores explicativos do cadastro.
- **Tabelas:** `cadastro.iptucalv`, `cadastro.iptucalh`, `cadastro.iptucalc`
- **Junções:**
  - `iptucalv.j21_codhis = iptucalh.j17_codhis`
  - `iptucalv.j21_matric = iptucalc.j23_matric` AND `iptucalv.j21_anousu = iptucalc.j23_anousu`
- **Explicadores de Fatores em `iptucalc`:**
  - `j23_vlrter` (Valor do terreno)
  - `j23_areaed` (Área edificada)
  - `j23_vlrisen` (Valor isento)
  - `j23_aliq` (Alíquota aplicada)
