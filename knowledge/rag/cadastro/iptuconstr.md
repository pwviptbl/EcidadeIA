## cadastro.iptuconstr



> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptuconstr`



### Resumo tecnico

- Descricao: Cadastro das construções vinculadas a uma matrícula imobiliária. Registra as edificações medidas ou cadastradas pelo município, com área, endereço da frente, datas de lançamento, demolição, habite-se, pavimento e identificação da construção principal.
- Chave primaria: j39_matric, j39_idcons
- Chave de negocio: j39_matric, j39_idcons
- Coluna de tempo: j39_dtlan
- Grao: Uma linha por construção vinculada a uma matrícula.
- Recomendada: sim
- Significado da contagem: Conta construções cadastradas por matrícula. Para contar construções ativas, aplicar `j39_dtdemo IS NULL`. Para contar imóveis com construção, usar `COUNT(DISTINCT j39_matric)`.
- Candidatas a chave de negocio: j39_matric, j39_idcons
- Candidatas a coluna de tempo: j39_ano, j39_dtdemo, j39_dtlan

### Relacionamentos

- `j39_codigo` -> `cadastro.ruas` (j14_codigo) [iptuconstr_codigo_fk]
- `j39_matric` -> `cadastro.iptubase` (j01_matric) [iptuconstr_matric_fk]

### Filtros padrao

- Matrícula específica `j39_matric = :matricula`
- Construção específica `j39_matric = :matricula AND j39_idcons = :idcons`
- Construções ativas `j39_dtdemo IS NULL`
- Construções demolidas `j39_dtdemo IS NOT NULL`
- Construção principal `j39_idprinc IS TRUE`
- Construções com área positiva `COALESCE(j39_area, 0) > 0`
- Construções sem área informada `COALESCE(j39_area, 0) = 0`
- Construções lançadas em período `j39_dtlan BETWEEN :data_inicio AND :data_fim`
- Construções demolidas em período `j39_dtdemo BETWEEN :data_inicio AND :data_fim`
- Construções por ano de edificação `j39_ano = :ano`
- Construções com habite-se `j39_habite IS NOT NULL`
- Construções sem habite-se `j39_habite IS NULL`
- Construções por logradouro `j39_codigo = :codigo_logradouro`

### Cuidados / riscos

- Uma matrícula pode possuir várias construções. Contar linhas conta construções, não imóveis.
- Para contar imóveis com construção, usar `COUNT(DISTINCT j39_matric)`.
- Para somar área construída ativa, aplicar `j39_dtdemo IS NULL`.
- Construções demolidas podem permanecer na tabela para histórico e não devem ser misturadas com construções ativas em análises correntes.
- `j39_area`, `j39_areap`, `j39_areajirau`, `j39_areajiraudeposito` e `j39_areamezanino` podem ter regras diferentes de uso no cálculo. Não somar tudo sem validar a regra municipal.
- `j39_dtlan` é data de lançamento no cadastro, não necessariamente data real da construção.
- `j39_ano` pode ter preenchimento incompleto, estimado ou herdado de cadastro anterior.
- `j39_habite` pode não conter todo o histórico de habite-se; existe tabela própria para detalhamento.
- `j39_idprinc` pode ajudar a identificar construção principal, mas não deve excluir automaticamente as demais construções da análise.
- Para análise de impacto do IPTU, a área cadastrada em `iptuconstr` deve ser comparada com a área usada no cálculo do exercício.
- Para comparação 2026 x 2027, cuidado com construções incluídas, demolidas ou alteradas entre os exercícios.
- Para explicar aumento de IPTU, cruzar com `iptucalc`, `iptucale`, `iptucalv` e características da construção.
- Para análises por localização, cruzar com `ruas`, `iptubase`, `lote`, bairro, setor e zona.
- Para evitar inferência errada por IA, usar as foreign keys documentadas antes de criar joins apenas por semelhança de nomes.
