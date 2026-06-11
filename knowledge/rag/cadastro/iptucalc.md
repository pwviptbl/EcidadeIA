## cadastro.iptucalc



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptucalc`



### Resumo tecnico

- Descricao: Dados principais do cálculo de IPTU por exercício e matrícula. Registra valores e parâmetros gerados no momento do cálculo, como valor venal do terreno, áreas consideradas, alíquota, testada, isenção e tipo de imposto.
- Chave primaria: j23_anousu, j23_matric
- Chave de negocio: j23_anousu, j23_matric
- Coluna de tempo: j23_anousu
- Grao: Uma linha por exercício e matrícula calculada.
- Recomendada: sim
- Significado da contagem: Conta cálculos de IPTU por matrícula e exercício. Para contar imóveis calculados em um ano, usar `COUNT(DISTINCT j23_matric)` filtrando por `j23_anousu`.
- Candidatas a chave de negocio: j23_anousu, j23_matric
- Candidatas a coluna de tempo: j23_anousu

### Relacionamentos

- `j23_matric` -> `cadastro.iptubase` (j01_matric) [iptucalc_matric_fk]

### Filtros padrao

- Exercício específico `j23_anousu = :exercicio`
- Matrícula específica `j23_matric = :matricula`
- Comparação entre exercícios `j23_anousu IN (:exercicio_anterior, :exercicio_atual)`
- Tipo predial `j23_tipoim = 'P'`
- Tipo territorial `j23_tipoim = 'T'`
- Com isenção calculada `COALESCE(j23_vlrisen, 0) > 0`
- Sem isenção calculada `COALESCE(j23_vlrisen, 0) = 0`
- Valor venal territorial positivo `COALESCE(j23_vlrter, 0) > 0`
- Área edificada positiva `COALESCE(j23_areaed, 0) > 0`
- Área de lote positiva `COALESCE(j23_arealo, 0) > 0`

### Regra de negocio para enriquecer

- Representa o resultado principal do cálculo cadastral/tributário do IPTU por matrícula e exercício. Ela guarda os parâmetros e valores usados ou gerados no cálculo, permitindo explicar como o sistema chegou ao valor venal territorial, à alíquota, à classificação predial/territorial e à eventual isenção.

- Quando ela deve ser preferida sobre outras tabelas parecidas?

- Deve ser preferida quando a pergunta envolve cálculo de IPTU por exercício, comparação entre anos, valor venal do terreno, área considerada no cálculo, testada considerada, alíquota aplicada ou tipo predial/territorial.
- Deve ser usada como base para explicar variações entre exercícios, especialmente em análises de impacto do recadastramento.
- Não deve ser usada sozinha para dizer valor final lançado, dívida, pagamento, arrecadação ou parcelamento.
- Para valor final por imposto ou taxa, consultar tabelas detalhadas como `iptucalv`.
- Para cálculo por construção, consultar tabelas como `iptucale`.
- Para débito gerado/numpre, consultar tabelas como `iptunump` ou equivalentes.

### Cuidados / riscos

- A chave correta para análise é `j23_anousu + j23_matric`. Usar apenas `j23_matric` mistura exercícios diferentes.
- A tabela registra dados do cálculo, não necessariamente o estado cadastral atual.
- Para comparar 2026 x 2027, usar auto-join ou agregação por `j23_matric`, sempre separando os exercícios.
- Variações de valor podem ser causadas por múltiplos fatores: área, testada, valor do m², alíquota, tipo predial/territorial, isenção ou regra de cálculo.
- `j23_vlrter` é valor venal do terreno, não valor final do IPTU.
- `j23_vlrisen` é valor de isenção calculado, não prova isolada de benefício ativo.
- `j23_manual` pode conter informações úteis, mas por ser campo textual pode ter baixa padronização.
- Matrículas baixadas podem ter cálculo em algum exercício; validar situação na `iptubase` quando a análise for de imóveis ativos.
- Imóveis novos ou recadastrados podem aparecer em 2027 e não aparecer em 2026.
- Imóveis baixados, desmembrados, unificados ou alterados podem dificultar comparação direta entre exercícios.
- Para análise de impacto financeiro completa, cruzar com tabelas de valores finais do cálculo e/ou débito.
- Para análise territorial, cruzar com `lote`, `bairro`, `setor`, `zonas`, `testada` e demais tabelas cadastrais.
