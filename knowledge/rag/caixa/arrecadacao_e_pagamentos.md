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

---

### Conceito: tipo_e_grupo_debito
- **Descrição:** Classificação dos débitos por tipo específico (arretipo) e grupo geral (cadtipo).
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arretipo`, `caixa.cadtipo`
- **Junções:**
  - `arrecad.k00_tipo = arretipo.k00_tipo`
  - `arretipo.k03_tipo = cadtipo.k03_tipo`
- **Regras de Negócio e Raciocínio Logístico:**
  1. **Autonomia de Cadastro e Padronização:** O `cadtipo` representa o agrupador fiscal macro (ex: 1 = IPTU, 2 = ISSQN, 3 = Taxas, etc.), sendo fixo e padrão em todas as instalações do e-Cidade. Contudo, cada prefeitura possui seu próprio Código Tributário Municipal (CTM). Por isso, cada cliente cria seus próprios tipos derivados em `arretipo` (ex: "IPTU Comercial", "IPTU Residencial Alíquota Progressiva", "ISS Variável Sociedade Uniprofissional") vinculando-os ao respectivo `cadtipo` pai.
  2. **Agrupamentos Globais:** Para responder perguntas como *"Quanto arrecadamos de ISSQN?"*, a IA deve rastrear o grupo global `cadtipo.k03_tipo = 2` e somar os débitos dos tipos filhos vinculados, em vez de tentar adivinhar ou filtrar por nomes literais em `arretipo.k00_descr`, que mudam em cada município.

---

### Regra de Negócio: Ciclo de Vida do Débito e Fluxo de Caixa
Para raciocinar sobre adimplência, inadimplência e arrecadação geral, o Agente deve considerar as seguintes regras fundamentais de funcionamento do caixa:
1. **O Estado de "A Vencer" e "Vencido" (Em Aberto):**
   Todos os débitos gerados e não pagos residem na tabela `caixa.arrecad`. Um débito é identificado por um `k00_numpre` (número de arrecadação) e desmembrado em parcelas (`k00_numpar`). Se a data atual for maior que `k00_dtvenc` e o débito continuar em `arrecad`, ele é considerado inadimplente/vencido.
2. **O Estado de "Pago" (Quitado):**
   No exato momento em que um contribuinte paga um débito no banco ou tesouraria, o registro correspondente é **deletado** da tabela `caixa.arrecad` (sai do saldo devedor ativo) e uma cópia com os dados da quitação é **inserida** na tabela `caixa.arrepaga` (arrecadação realizada).
3. **Cálculo de Inadimplência:**
   Para saber o total calculado/lançado histórico, a soma deve considerar `calculado = (tudo que está em arrepaga) + (tudo que está em arrecad)`. A taxa de inadimplência atual é calculada dividindo `arrecad.k00_valor` (o que sobrou sem pagar) pelo `total_calculado`.
4. **Pagamentos Parciais:**
   Se um contribuinte paga apenas parte de uma parcela, o sistema liquida a parcela original em `arrecad`, joga o valor pago para `arrepaga`, e gera um novo desmembramento (normalmente uma parcela complementar ou resíduo) em `arrecad` com o saldo restante.

---

---

### Regras de Negócio e Receitas de IPTU
As regras de negócio específicas para apurações de valores calculados, lançados, arrecadados e inadimplência de IPTU foram consolidadas no arquivo dedicado:
- Para detalhes de IPTU, consulte: [iptu.md](file:///home/dbseller/Modelos/MVP/knowledge/rag/caixa/iptu.md)

