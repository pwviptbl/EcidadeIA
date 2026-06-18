## cadastro.isencao_iptu

> Fonte manual: `knowledge/manual/cadastro/isencao_iptu.md`

### Receita: `calculo_isencao_iptu_bairro`

**Descrição:** Como identificar isenções de IPTU concedidas, e cruzar com os bairros.
**Regra de Negócio Crucial:**
- **Isenções Calculadas:** As isenções de IPTU são registradas no momento do cálculo do imposto, que fica na tabela `cadastro.iptucalc`.
- **Filtro de Isenção:** Para saber se houve isenção, você deve verificar a coluna `j23_vlrisen` (Valor da Isenção). O filtro deve ser `j23_vlrisen > 0` (ou `COALESCE(j23_vlrisen, 0) > 0`).
- **Ano da Isenção:** Sempre filtre pelo ano solicitado na coluna `j23_anousu` da tabela `iptucalc`.
- **Cruzamento Cadastral:** Para achar as isenções de um bairro específico, você deve seguir o caminho:
  1. `cadastro.bairro` (filtre pelo nome do bairro em `j13_descr` usando `ILIKE '%Nome%'`).
  2. Faça JOIN com `cadastro.lote` (`bairro.j13_codi = lote.j34_bairro`).
  3. Faça JOIN com `cadastro.iptubase` (`lote.j34_idbql = iptubase.j01_idbql`).
  4. Faça JOIN com `cadastro.iptucalc` (`iptubase.j01_matric = iptucalc.j23_matric`).

**Atenção:** Nunca tente usar a tabela `information_schema.columns` para descobrir colunas, consulte apenas as documentações no RAG. Quando o usuário perguntar "quais são as isenções", você pode fazer um `COUNT(iptucalc.j23_matric)` para contar quantos imóveis tiveram isenção e um `SUM(iptucalc.j23_vlrisen)` para ver o valor total isentado naquele bairro e ano.
