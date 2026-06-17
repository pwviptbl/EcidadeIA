## caixa.inadimplencia_iptu

> Fonte manual: `knowledge/manual/caixa/inadimplencia_iptu.md`

### Receita: `calculo_taxa_inadimplencia_iptu`

**Descrição:** Para calcular a inadimplência de IPTU, débitos em aberto ou comparar o que falta pagar.
**Regra de Negócio Crucial:**
- **Débitos em Aberto (Não Pagos)** ficam na tabela `caixa.arrecad`. Se o débito está nesta tabela, significa que ele **ainda não foi pago**. O total inadimplente é a soma de `caixa.arrecad.k00_valor`.
- **Débitos Pagos** ficam na tabela `caixa.arrepaga` (após o pagamento, o débito sai da `arrecad`).
- **Valor Base Lançado/Calculado** deve ser obtido através da tabela `cadastro.iptucalv` (usando o campo `j21_valor`), que guarda o imposto total originalmente calculado.
- **Cálculo da Taxa:** O percentual de inadimplência DEVE ser baseado na soma dos valores financeiros (R$), e NUNCA pela quantidade de carnês (`COUNT`). Exemplo: `(SUM(valor_aberto) / SUM(valor_lancado)) * 100`.
- **Atenção ao Efeito Multiplicador (Fan-out das Parcelas):** A tabela `arrecad` contém múltiplas parcelas para um mesmo débito (ex: 10 parcelas). Se você usar `COUNT()` após um `LEFT JOIN`, um imóvel com 10 parcelas atrasadas pesará 10 vezes mais na estatística, e um pagamento parcial ignorará as parcelas pagas, arruinando o percentual. SEMPRE agregue os valores financeiros (`SUM`) usando CTEs separadas antes de juntar as tabelas.

**Tabelas Envolvidas:** `cadastro.bairro`, `cadastro.iptubase`, `cadastro.iptucalv`, `cadastro.iptunump`, `caixa.arrecad`

**Passo a passo (Joins):**
1. Junte os imóveis e bairros (`cadastro.bairro` -> `cadastro.lote` -> `cadastro.iptubase`).
2. Junte com `cadastro.iptucalv` (`j01_matric = j21_matric`) e filtre pelo ano desejado (`j21_anousu = YYYY`). A soma de `j21_valor` será o "Total Calculado".
3. Junte com `cadastro.iptunump` (`j01_matric = j20_matric` e `j20_anousu = YYYY`).
4. Para obter a dívida pendente, faça um LEFT JOIN de `cadastro.iptunump` com `caixa.arrecad` (`j20_numpre = k00_numpre`).
5. A soma de `caixa.arrecad.k00_valor` representará o "Total Inadimplente/Em Aberto".
6. Cuidado com multiplicações de JOIN: calcule o Total Lançado (agregando `iptucalv`) e o Total Aberto (agregando `arrecad`) em CTEs independentes agrupadas por matrícula ou bairro ANTES de fazer o JOIN final. Nunca faça JOIN direto sem agregar antes, caso contrário o `j21_valor` será somado repetidas vezes.
