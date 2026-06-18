## cadastro.bairros_e_logradouros

> Fonte manual: `knowledge/manual/cadastro/bairros_e_logradouros.md`

Mapeia as relações territoriais dos imóveis, logradouros e bairros do município.

---

### Conceito: bairro_do_imovel
- **Descrição:** Vínculo geográfico/cadastral do lote do imóvel com seu bairro correspondente.
- **Tabelas:** `cadastro.bairro`, `cadastro.lote`, `cadastro.iptubase`
- **Junções:**
  - `bairro.j13_codi = lote.j34_bairro`
  - `lote.j34_idbql = iptubase.j01_idbql`
- **Filtro Recomendado:** Buscar bairro por nome em `bairro.j13_descr` (ex: `ILIKE '%Icaraí%'`).

---

### Conceito: ruas_do_bairro
- **Descrição:** Ruas e logradouros mapeados em cada bairro territorial.
- **Tabelas:** `cadastro.bairro`, `cadastro.ruasbairro`, `cadastro.ruas`
- **Junções:**
  - `bairro.j13_codi = ruasbairro.j16_bairro`
  - `ruasbairro.j16_lograd = ruas.j14_codigo`
- **Regra de Contagem:** Para contar logradouros distintos por bairro, usar `COUNT(DISTINCT ruas.j14_codigo)`.
- **Exemplo SQL:**
  ```sql
  SELECT r.j14_codigo, r.j14_nome
  FROM cadastro.bairro b
  JOIN cadastro.ruasbairro rb ON b.j13_codi = rb.j16_bairro
  JOIN cadastro.ruas r ON rb.j16_lograd = r.j14_codigo
  WHERE b.j13_descr ILIKE '%Icaraí%';
  ```
