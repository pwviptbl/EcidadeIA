## issqn.cadastro_mobiliario_e_servicos

> Fonte manual: Nenhuma manual fornecida.

Mapeia a estrutura do Cadastro Mobiliário Municipal (ISSQN/Alvarás), incluindo o vínculo de empresas a contribuintes (CGM), suas atividades econômicas (CNAE) e as apurações de ISSQN Variável.

---

### Conceito: cadastro_mobiliario
- **Descrição:** Cadastro base de empresas e atividades econômicas (alvarás) vinculadas a um contribuinte (CGM).
- **Tabelas:** `issqn.issbase`, `protocolo.cgm`
- **Junção:**
  - `issbase.q02_numcgm = cgm.z01_numcgm`
- **Campos importantes:**
  - `q02_inscr`: Inscrição Municipal (Chave Primária).
  - `q02_numcgm`: Identificador do Contribuinte (CGM).
  - `q02_dtcada`: Data de cadastramento da inscrição.
  - `q02_dtbaix`: Data de baixa da inscrição (se nula, a inscrição está ativa).

---

### Conceito: atividades_e_cnae
- **Descrição:** Vínculo de uma inscrição municipal com as suas atividades econômicas e códigos CNAE correspondentes.
- **Tabelas:** `issqn.issbase`, `issqn.tabativ`, `issqn.ativid`, `issqn.atividcnae`, `issqn.cnaeanalitica`, `issqn.cnae`
- **Junções:**
  - `issbase.q02_inscr = tabativ.q07_inscr`
  - `tabativ.q07_ativ = ativid.q03_ativ`
  - `ativid.q03_ativ = atividcnae.q74_ativid`
  - `atividcnae.q74_cnaeanalitica = cnaeanalitica.q72_sequencial`
  - `cnaeanalitica.q72_cnae = cnae.q71_sequencial`
- **Campos importantes:**
  - `tabativ.q07_databx`: Data de baixa da atividade específica (se nula, a atividade está ativa para a empresa).
  - `cnae.q71_estrutural`: Código estruturado do CNAE (ex: '6201-5/01').
  - `cnae.q71_descr`: Descrição da atividade CNAE.

---

### Conceito: lancamento_iss_variavel
- **Descrição:** Registros mensais de faturamento bruto e imposto devido informados ou calculados para empresas sob regime de ISSQN variável.
- **Tabelas:** `issqn.issbase`, `caixa.arreinscr`, `issqn.issvar`
- **Junções:**
  - `issbase.q02_inscr = arreinscr.k00_inscr`
  - `arreinscr.k00_numpre = issvar.q05_numpre`
- **Campos importantes:**
  - `issvar.q05_ano`: Ano da competência do imposto.
  - `issvar.q05_mes`: Mês da competência do imposto.
  - `issvar.q05_bruto`: Valor bruto de faturamento informado.
  - `issvar.q05_aliq`: Alíquota aplicada.
  - `issvar.q05_valor`: Valor do imposto devido calculado.
  - `issvar.q05_vlrinf`: Valor informado de imposto pelo contribuinte.
