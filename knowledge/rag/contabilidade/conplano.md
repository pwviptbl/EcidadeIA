## contabilidade.conplano

> Fonte de código: `/var/www/html/e-cidade-php74/classes/db_conplano_classe.php`

Representa o plano de contas contábil por exercício. A classe combina a conta estrutural com classificação, sistema contábil, conta reduzida, execução por exercício, contas correntes/bancárias e vínculos com o plano orçamentário.

### Resumo técnico

- **Classe:** `cl_conplano`
- **Tabela principal:** `conplano`
- **Chave composta:** `c60_codcon`, `c60_anousu`
- **Código estrutural:** `c60_estrut`
- **Descrição:** `c60_descr`
- **Finalidade:** `c60_finali`
- **Sistema:** `c60_codsis`
- **Classificação:** `c60_codcla`
- **Sistema de conta:** `c60_consistemaconta`
- **Identificador financeiro:** `c60_identificadorfinanceiro`
- **Natureza do saldo:** `c60_naturezasaldo`
- **Função:** `c60_funcao`
- **Saldo contínuo:** `c60_saldocontinuo`
- **Grão:** Uma conta estrutural em um exercício.

### Relacionamentos principais

- `conplano.c60_codcla = conclass.c51_codcla`
- `conplano.c60_codsis = consistema.c52_codsis`
- `(conplano.c60_codcon, conplano.c60_anousu) = (conplanoreduz.c61_codcon, conplanoreduz.c61_anousu)`
- `(conplanoreduz.c61_reduz, conplanoreduz.c61_anousu) = (conplanoexe.c62_reduz, conplanoexe.c62_anousu)`

`c60_codcon` não deve ser usado isoladamente entre exercícios. Os vínculos seguros incluem `c60_anousu`.

---

### Leitura física: `sql_query_file`

- **Objetivo:** Consultar somente `conplano`, sem exigir conta reduzida, classificação ou sistema.
- **Filtros padrão:**
  - `conplano.c60_codcon = :codigo`
  - `conplano.c60_anousu = :exercicio`
- **Grão:** Uma conta por exercício.
- **Uso recomendado:** Verificar existência de conta estrutural, inclusive contas sintéticas sem reduzido.

```sql
SELECT /* campos dinâmicos */
FROM conplano
WHERE conplano.c60_codcon = :codigo
  AND conplano.c60_anousu = :exercicio;
```

### Consulta operacional da sessão: `sql_query` e `sql_query2`

- **Objetivo:** Recuperar contas com classificação, sistema e conta reduzida.
- **Tabelas obrigatórias:** `conplano`, `conclass`, `consistema`, `conplanoreduz`.
- **Regra de sessão:** Ambas acrescentam obrigatoriamente:
  - `c60_anousu = DB_anousu`
  - `c61_instit = DB_instit`
- **Consequência:** Retornam apenas contas com reduzido da instituição e do exercício correntes.
- **Diferença:** `sql_query2` monta corretamente `AND c60_anousu = :exercicio` após o código; `sql_query` concatena um segundo `WHERE` quando código e exercício são informados juntos.
- **Cuidados:**
  - O exercício passado pelo chamador não permite consultar outro ano, pois o método também força `DB_anousu`.
  - Em `sql_query`, não passar simultaneamente código e exercício; a SQL resultante contém `WHERE ... WHERE ...`.
  - Contas sintéticas ou sem reduzido são excluídas pelos `INNER JOIN`.

```sql
SELECT /* campos dinâmicos */
FROM conplano
JOIN conclass
  ON conclass.c51_codcla = conplano.c60_codcla
JOIN consistema
  ON consistema.c52_codsis = conplano.c60_codsis
JOIN conplanoreduz
  ON conplanoreduz.c61_codcon = conplano.c60_codcon
 AND conplanoreduz.c61_anousu = conplano.c60_anousu
WHERE conplano.c60_anousu = :exercicio_sessao
  AND conplanoreduz.c61_instit = :instituicao_sessao;
```

### Consulta geral do plano: `sql_query_geral`

- **Objetivo:** Consultar a árvore contábil com classificação e sistema, preservando contas sem reduzido.
- **Conta reduzida:** `LEFT JOIN conplanoreduz`.
- **Filtro padrão:**
  - Se código e exercício forem informados, filtra pelos dois.
  - Sem ambos, usa `DB_anousu`.
  - `$dbwhere` substitui o filtro padrão.
- **Instituição:** A classe consulta se `db_config.prefeitura` é verdadeiro, mas os filtros por `c61_instit` estão comentados e não afetam a SQL.
- **Cuidados:**
  - Pode retornar reduzidos de várias instituições quando o chamador não filtra `c61_instit`.
  - Uma conta pode gerar várias linhas se possuir mais de um reduzido/instituição.
  - Para listar contas estruturais únicas, usar `DISTINCT` ou não selecionar campos de `conplanoreduz`.

### Visão de plano de contas: `sql_vs_planocontas`

- **Fonte:** View `vs_planocontas`.
- **Campos, filtro e ordenação:** Dinâmicos.
- **Instituição:** O filtro por `c61_instit` está comentado.
- **Defeito observado:** Quando `c60_codcon` é informado sem `$dbwhere`, o método gera `WHERE conplano.c60_codcon = ...`, embora o `FROM` contenha apenas `vs_planocontas` e não declare alias `conplano`.
- **Uso seguro:** Fornecer `$dbwhere` com colunas realmente expostas pela view.

---

### Validação da hierarquia: `db_verifica_conplano`

- **Objetivo:** Impedir cadastro de conta estrutural cujo nível imediatamente superior não exista.
- **Funções auxiliares:**
  - `db_le_mae_conplano($estrutural, true)` retorna o nível.
  - `db_le_mae_conplano($estrutural, false)` retorna o estrutural pai.
- **Regra:**
  - Conta de nível 1 é válida sem pai.
  - Demais níveis exigem uma linha em `conplano` no mesmo exercício com `c60_estrut = :estrutural_pai`.
- **Resultado inválido:** `Procedimento abortado. Estrutural acima não encontrado!`

```sql
SELECT c60_estrut
FROM conplano
WHERE c60_anousu = :exercicio
  AND c60_estrut = :estrutural_pai;
```

### Validação de exclusão: `db_verifica_conplano_exclusao`

- **Objetivo:** Impedir exclusão de conta estrutural que possua contas descendentes.
- **Regra:**
  - Nível 9 é tratado como folha e pode ser excluído sem busca de descendente.
  - Para níveis 1 a 8, a classe busca contas com o mesmo prefixo e sufixo diferente de zeros.
  - A exclusão é abortada quando existir ao menos uma conta inferior no mesmo exercício.
- **Resultado bloqueado:** `Exclusão abortada. Existe uma conta de nível inferior cadastrada!`
- **Cuidados:** A regra depende de posições fixas e preenchimento com zeros em `c60_estrut`; não substituir por comparação textual genérica sem reproduzir a convenção estrutural.

---

### Contas reduzidas executáveis: `sql_query_reduz`

- **Objetivo:** Consultar contas reduzidas existentes na execução do exercício.
- **Tabelas obrigatórias:** `conplano`, `conplanoreduz`, `conplanoexe`, `conclass`, `consistema`.
- **Vínculos:**
  - Conta do plano com reduzido pelo código e exercício.
  - Reduzido com execução por `c61_reduz = c62_reduz` e mesmo exercício.
- **Filtros fixos:**
  - `c62_anousu = DB_anousu`
  - `c61_instit = DB_instit`
- **Grão:** Conta reduzida executável para a instituição no exercício da sessão.
- **Uso observado:** Pesquisa de contas para lançamentos, contrapartidas, encerramento e conta corrente.

```sql
SELECT /* campos dinâmicos */
FROM conplano
JOIN conplanoreduz
  ON conplanoreduz.c61_codcon = conplano.c60_codcon
 AND conplanoreduz.c61_anousu = conplano.c60_anousu
JOIN conplanoexe
  ON conplanoexe.c62_reduz = conplanoreduz.c61_reduz
 AND conplanoexe.c62_anousu = conplanoreduz.c61_anousu
JOIN conclass
  ON conclass.c51_codcla = conplano.c60_codcla
JOIN consistema
  ON consistema.c52_codsis = conplano.c60_codsis
WHERE conplanoexe.c62_anousu = :exercicio_sessao
  AND conplanoreduz.c61_instit = :instituicao_sessao;
```

### Conta reduzida ligada a elemento: `sql_query_ele`

- **Base:** `conplano -> conplanoreduz -> conplanoexe`.
- **Filtros fixos:** Exercício e instituição da sessão.
- **Regra condicional:**
  - Quando `USE_PCASP` é falso, exige também `orcelemento.o56_codele = conplano.c60_codcon` no mesmo exercício.
  - Quando `USE_PCASP` é verdadeiro, não faz o join com `orcelemento`.
- **Cuidados:** A semântica “elemento” é dependente do modo contábil. Não exigir vínculo direto com `orcelemento` em ambiente PCASP.

---

### Plano com vínculos auxiliares: `sql_query_planocontas`

- **Objetivo:** Consultar contas e possíveis vínculos com reduzido, conta corrente, fonte orçamentária e elemento.
- **Todos os vínculos auxiliares são `LEFT JOIN`:**
  - `conplanoreduz`
  - `conplanoconta`
  - `orcfontes`
  - `orcelemento`
- **Filtro padrão:** `conplano.c60_anousu = :exercicio`.
- **Instituição:** O filtro de `c61_instit` está comentado.
- **Grão:** Pode multiplicar uma conta por reduzidos, contas correntes, fontes ou elementos.
- **Cuidados:** Não contar contas nem somar dados sem controlar a cardinalidade dos vínculos opcionais.

### Dados do plano PCASP: `sql_query_dados_plano`

- **Objetivo:** Recuperar conta PCASP, reduzido, classificação e eventual configuração de conta bancária.
- **Vínculos:**
  - `LEFT JOIN conplanoreduz`
  - `LEFT JOIN conplanocontabancaria` pelo exercício e reduzido
  - `INNER JOIN conclass`
- **Regra comprovada:** A conta é preservada sem reduzido ou conta bancária, mas exige classificação válida.
- **Instituição:** Não há filtro fixo; o filtro existente no código está comentado.

### Vínculo PCASP com orçamento analítico: `sql_query_pcasp_orcamento_analitico`

- **Objetivo:** Retornar contas PCASP que possuem vínculo com conta orçamentária marcada como analítica.
- **Caminho obrigatório:**
  - `conplano -> conplanoreduz`
  - `conplano -> conplanoconplanoorcamento`
  - `conplanoconplanoorcamento -> conplanoorcamento`
  - `conplanoorcamento -> conplanoorcamentoanalitica`
- **Regra comprovada:** Todos os joins são internos; somente contas com vínculo orçamentário analítico aparecem.
- **Chaves do vínculo:**
  - `c72_conplano = conplano.c60_codcon`
  - `c72_conplanoorcamento = conplanoorcamento.c60_codcon`
  - O exercício deve coincidir em todas as tabelas.
- **Uso observado:** Busca de reduzidos para regras de evento contábil.

```sql
SELECT /* campos dinâmicos */
FROM conplano
JOIN conplanoreduz
  ON conplanoreduz.c61_codcon = conplano.c60_codcon
 AND conplanoreduz.c61_anousu = conplano.c60_anousu
JOIN conplanoconplanoorcamento
  ON conplanoconplanoorcamento.c72_conplano = conplano.c60_codcon
 AND conplanoconplanoorcamento.c72_anousu = conplano.c60_anousu
JOIN conplanoorcamento
  ON conplanoorcamento.c60_codcon =
     conplanoconplanoorcamento.c72_conplanoorcamento
 AND conplanoorcamento.c60_anousu =
     conplanoconplanoorcamento.c72_anousu
JOIN conplanoorcamentoanalitica
  ON conplanoorcamentoanalitica.c61_codcon =
     conplanoorcamento.c60_codcon
 AND conplanoorcamentoanalitica.c61_anousu =
     conplanoorcamento.c60_anousu
WHERE conplano.c60_anousu = :exercicio;
```

### Dados bancários da conta: `sql_query_dados_banco`

- **Objetivo:** Consultar conta, classificação, sistema, reduzido, conta corrente contábil e configuração bancária.
- **Vínculos obrigatórios:** `conclass` e `consistema`.
- **Vínculos opcionais:**
  - `conplanoreduz`
  - `conplanoconta`
  - `conplanocontabancaria`
- **Filtro padrão:**
  - Código e exercício quando ambos são informados.
  - Caso contrário, exercício `DB_anousu`.
- **Instituição:** A classe consulta `db_config.prefeitura`, mas o filtro por instituição está comentado.
- **Uso observado:** Abertura de contas PCASP e relatórios contábeis.
- **Cuidados:** Uma conta pode gerar várias linhas por reduzido ou configuração bancária; filtrar `c61_instit` quando a resposta precisar ser institucional.

### Campos contábeis que exigem domínio externo

- `c60_consistemaconta`, `c60_identificadorfinanceiro` e `c60_naturezasaldo` são usados por relatórios e exportações, mas esta classe não define todos os significados possíveis.
- Evidência externa na base indica `c60_identificadorfinanceiro` com valores como `N`, `F` e `P`; não traduzir esses códigos sem consultar o domínio/regra da versão.
- `c60_saldocontinuo` participa da manutenção PCASP, mas esta classe não contém a regra de transferência de saldo.

### Cuidados gerais

- Sempre combinar código da conta com exercício.
- Para contas disponíveis à instituição, filtrar `conplanoreduz.c61_instit`.
- `INNER JOIN conplanoreduz` exclui contas sem reduzido; `LEFT JOIN` preserva contas sintéticas.
- Consultas com `conplanoexe` representam reduzidos presentes na execução do exercício.
- Não confundir plano contábil `conplano` com plano orçamentário `conplanoorcamento`.
- A árvore depende do formato posicional de `c60_estrut` e de segmentos preenchidos com zeros.
- Campos e ordenação são concatenados dinamicamente; `$dbwhere` substitui os filtros padrão em vários métodos.
- Em `atualizacampos`, `c60_saldocontinuo` é lido de `HTTP_POST_VARS["c60_funcao"]`, não de uma chave própria. Validar esse campo em fluxos de edição legados.
- Para visão geral e receitas simplificadas, consultar `knowledge/rag/contabilidade/contabilidade.md`.
