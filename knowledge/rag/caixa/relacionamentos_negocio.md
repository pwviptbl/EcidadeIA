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

### Receita: `calculo_taxa_inadimplencia_iptu`

**Descrição:** Para calcular a inadimplência de IPTU, débitos em aberto ou comparar o que falta pagar.
**Regra de Negócio Crucial:**
- **Débitos em Aberto (Não Pagos)** ficam na tabela `caixa.arrecad`. Se o débito está nesta tabela, significa que ele **ainda não foi pago**. O total inadimplente é a soma de `caixa.arrecad.k00_valor`.
- **Débitos Pagos** ficam na tabela `caixa.arrepaga` (após o pagamento, o débito sai da `arrecad`).
- **Valor Base Lançado/Calculado** deve ser obtido através da tabela `cadastro.iptucalv` (usando o campo `j21_valor`), que guarda o imposto total originalmente calculado.
- **Cálculo da Taxa:** O percentual de inadimplência deve ser baseado na proporção do total em aberto (`caixa.arrecad`) contra o total calculado (`cadastro.iptucalv`).
**Tabelas Envolvidas:** `cadastro.bairro`, `cadastro.iptubase`, `cadastro.iptucalv`, `cadastro.iptunump`, `caixa.arrecad`
**Passo a passo (Joins):**
1. Junte os imóveis e bairros (`cadastro.bairro` -> `cadastro.lote` -> `cadastro.iptubase`).
2. Junte com `cadastro.iptucalv` (`j01_matric = j21_matric`) e filtre pelo ano desejado (`j21_anousu = YYYY`). A soma de `j21_valor` será o "Total Calculado".
3. Junte com `cadastro.iptunump` (`j01_matric = j20_matric` e `j20_anousu = YYYY`).
4. Para obter a dívida pendente, faça um LEFT JOIN de `cadastro.iptunump` com `caixa.arrecad` (`j20_numpre = k00_numpre`).
5. A soma de `caixa.arrecad.k00_valor` representará o "Total Inadimplente/Em Aberto".
6. Cuidado com multiplicações de JOIN: como o parcelamento gera múltiplos registros em `iptunump`/`arrecad`, prefira calcular o Total Lançado (`iptucalv`) e o Total Aberto (`arrecad`) de forma segura usando subqueries ou garantindo que o `j21_valor` não seja somado repetidas vezes para a mesma matrícula.
