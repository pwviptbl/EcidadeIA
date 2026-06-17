## relacionamentos_negocio



> Fonte manual: `knowledge/manual/caixa/relacionamentos_negocio.md`



### Receita: `ligacao_iptu_arrecadacao`

**Descrição:** Liga as matrículas de IPTU (cadastro) com os débitos e pagamentos na arrecadação (caixa).
**Tabelas Envolvidas:** `cadastro.iptubase`, `cadastro.iptunump`, `caixa.arrecad`, `caixa.arrepaga`
**Passo a passo (Joins):**
1. O imóvel cadastrado está na `cadastro.iptubase`.
2. Os débitos desse imóvel vinculados a exercícios estão mapeados na tabela de junção `cadastro.iptunump` usando a chave `j01_matric = j20_matric`.
3. Os débitos (recibos) gerados no financeiro estão na `caixa.arrecad` e se ligam através do número da prestação (numpre): `cadastro.iptunump.j20_numpre = caixa.arrecad.k00_numpre`.
4. Os pagamentos efetivados estão na `caixa.arrepaga` e se ligam pelo número da prestação e parcela: `caixa.arrecad.k00_numpre = caixa.arrepaga.k00_numpre` AND `caixa.arrecad.k00_numpar = caixa.arrepaga.k00_numpar`.

### Receita: `comparacao_iptu_pago_vs_calculado`

**Descrição:** Para responder perguntas como "quanto arrecadamos vs quanto foi calculado" ou "efetivamente arrecadado (pago)".
**Perguntas comuns:**
- Qual o valor total efetivamente arrecadado (pago) de IPTU no bairro Icaraí no exercício de 2026?
- Quanto efetivamente arrecadamos em Icaraí?
**Tabelas Envolvidas:** `cadastro.bairro`, `cadastro.lote`, `cadastro.iptubase`, `cadastro.iptucalv`, `cadastro.iptunump`, `caixa.arrepaga`
**Passo a passo (Joins):**
1. Parta do `cadastro.bairro` e junte com `cadastro.lote` (`j13_codi = j34_bairro`).
2. Junte com `cadastro.iptubase` (`j34_idbql = j01_idbql`).
3. Para garantir que estamos tratando apenas de IPTU, junte a `cadastro.iptubase` com `cadastro.iptucalv` (`j01_matric = j21_matric`). E então junte `cadastro.iptucalv` com `cadastro.iptucalh` (`j21_codhis = j17_codhis`). NUNCA ligue `caixa.arrepaga` diretamente a `cadastro.iptucalh` (os históricos de caixa e cadastro são incompatíveis).
4. Para chegar aos pagamentos a partir da matrícula, junte `cadastro.iptubase` com `cadastro.iptunump` (`j01_matric = j20_matric`).
5. Junte `cadastro.iptunump` com `caixa.arrepaga` (`j20_numpre = k00_numpre`).
6. O valor efetivamente pago estará em `caixa.arrepaga.k00_valor`.
