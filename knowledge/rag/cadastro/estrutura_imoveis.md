## cadastro.estrutura_imoveis

> Fonte manual: `knowledge/manual/cadastro/estrutura_imoveis.md`

Mapeia as características físicas, quantitativos estruturais e características de lotes e construções.

---

### Conceito: matricula_ativa
- **Descrição:** Imóvel ativo e vigente no cadastro imobiliário municipal.
- **Tabelas:** `cadastro.iptubase`
- **Filtro de Negócio:** `iptubase.j01_baixa IS NULL` (Matrículas ativas) ou `iptubase.j01_baixa IS NOT NULL` (Matrículas inativas/baixadas).
- **Regra de Contagem:** `COUNT(DISTINCT j01_matric)`.

---

### Conceito: construcao_ativa
- **Descrição:** Edificação cadastrada vinculada a uma matrícula imobiliária que não sofreu demolição.
- **Tabelas:** `cadastro.iptuconstr`
- **Filtro de Negócio:** `iptuconstr.j39_dtdemo IS NULL` (Construções ativas) ou `iptuconstr.j39_dtdemo IS NOT NULL` (Construções inativas/demolidas).
- **Regra de Contagem:** `COUNT(DISTINCT (j39_matric, j39_idcons))`.

---

### Receita: `soma_area_construida_ativa`
- **Descrição:** Soma da metragem quadrada total de edificações vigentes no município.
- **Tabelas:** `cadastro.iptuconstr`
- **Filtro de Negócio:** `iptuconstr.j39_dtdemo IS NULL` AND `COALESCE(iptuconstr.j39_area, 0) > 0`
- **Regra de Agregação:** `SUM(j39_area)`.

---

### Receita: `caracteristica_lote`
- **Descrição:** Filtra lotes com base em suas características territoriais (ex: "Piscina", "Esquina").
- **Tabelas:** `cadastro.carlote`, `cadastro.caracter`, `cadastro.lote`
- **Junções:**
  - `carlote.j35_caract = caracter.j31_codigo`
  - `carlote.j35_idbql = lote.j34_idbql`
- **Filtro Recomendado:** `caracter.j31_descr ILIKE '%Piscina%'`
- **Regra de Contagem:** `COUNT(DISTINCT lote.j34_idbql)`.

---

### Receita: `caracteristica_construcao`
- **Descrição:** Filtra construções/edificações com base em características estruturais (ex: padrão construtivo "Luxo").
- **Tabelas:** `cadastro.carconstr`, `cadastro.caracter`, `cadastro.iptuconstr`
- **Junções:**
  - `carconstr.j48_caract = caracter.j31_codigo`
  - `carconstr.j48_matric = iptuconstr.j39_matric` e `carconstr.j48_idcons = iptuconstr.j39_idcons`
- **Filtro Recomendado:** `caracter.j31_descr ILIKE '%Luxo%'`
- **Filtro Opcional:** `iptuconstr.j39_dtdemo IS NULL` (Apenas construções ativas).
- **Regra de Contagem:** `COUNT(DISTINCT (j48_matric, j48_idcons))`.
