## issqn.issbase

> Fonte de código: `/var/www/html/e-cidade-php74/classes/db_issbase_classe.php`

Cadastro base das inscrições municipais do módulo ISSQN. Relaciona a inscrição ao CGM, datas de cadastro/início/baixa, atividades, sócios, setor fiscal, enquadramentos e processos.

### Resumo técnico

- **Classe:** `cl_issbase`
- **Tabela principal:** `issbase`
- **Chave:** `q02_inscr`
- **CGM:** `q02_numcgm`
- **Inscrição textual:** `q02_inscmu`
- **Tipo de licença:** `q02_tiplic`
- **Data de cadastro:** `q02_dtcada`
- **Data de início:** `q02_dtinic`
- **Data de baixa:** `q02_dtbaix`
- **Capital social:** `q02_capit`
- **CEP:** `q02_cep`
- **Registro/data/protocolo da Junta Comercial:** `q02_regjuc`, `q02_dtjunta`, `q02_protocolojuntacomercial`
- **Últimas alterações:** `q02_ultalt`, `q02_dtalt`
- **Grão:** Uma inscrição municipal.
- **Regra de atividade da inscrição:** `q02_dtbaix IS NULL`.

### Leitura cadastral: `sql_query` e `sql_query_file`

- **`sql_query`:** Liga obrigatoriamente `cgm` e opcionalmente `issveiculo`.
- **`sql_query_file`:** Lê somente `issbase`.
- **Filtro padrão:** `issbase.q02_inscr = :inscricao`.
- **Cuidados:**
  - `sql_query` pode gerar mais de uma linha por inscrição quando houver vários veículos.
  - Para contar inscrições, usar `COUNT(DISTINCT q02_inscr)`.

```sql
SELECT /* campos dinâmicos */
FROM issbase
JOIN cgm
  ON cgm.z01_numcgm = issbase.q02_numcgm
LEFT JOIN issveiculo
  ON issveiculo.q172_issbase = issbase.q02_inscr
WHERE issbase.q02_inscr = :inscricao;
```

### View de empresa: `empresa_query` e `empresa_query_file`

- **Fonte:** View `empresa`.
- **Filtro padrão:** `empresa.q02_inscr = :inscricao`.
- **Uso observado:** Consultas fiscais, financeiras e de endereço/nome da empresa.
- **Cuidados:** A classe não define a SQL interna da view. Não inferir seus joins ou grão somente pelos campos expostos.

---

### Atividades da inscrição: `sql_query_atividades`

- **Caminho:** `issbase -> cgm` e `issbase -> tabativ`.
- **Vínculo:** `tabativ.q07_inscr = issbase.q02_inscr`.
- **Grão:** Atividade vinculada à inscrição.
- **Cuidados:** O método não filtra atividade ativa; aplicar `q07_databx IS NULL` e, quando relevante, `q07_datafi IS NULL`.

### Atividade de serviço variável: `sql_queryAtividadeServico`

- **Objetivo:** Confirmar se uma inscrição ativa possui atividade de serviço com cálculo variável.
- **Condições fixas:**
  - `issbase.q02_dtbaix IS NULL`
  - `tabativ.q07_databx IS NULL`
  - `tipcalc.q81_tipo = 1`
  - `cadcalc.q85_var IS TRUE`
  - `issbase.q02_inscr = :inscricao`
- **Caminho:** `issbase -> tabativ -> ativid -> ativtipo -> tipcalc -> cadcalc`.
- **Retorno:** `DISTINCT q02_inscr`.
- **Cuidados:** O método não filtra `tabativ.q07_datafi`; sua regra difere de `sql_query_aliquota`.

```sql
SELECT DISTINCT q02_inscr
FROM issbase
JOIN tabativ ON tabativ.q07_inscr = issbase.q02_inscr
JOIN ativid ON ativid.q03_ativ = tabativ.q07_ativ
JOIN ativtipo ON ativtipo.q80_ativ = ativid.q03_ativ
JOIN tipcalc ON tipcalc.q81_codigo = ativtipo.q80_tipcal
JOIN cadcalc ON cadcalc.q85_codigo = tipcalc.q81_cadcalc
WHERE issbase.q02_dtbaix IS NULL
  AND tabativ.q07_databx IS NULL
  AND tipcalc.q81_tipo = 1
  AND cadcalc.q85_var IS TRUE
  AND issbase.q02_inscr = :inscricao;
```

### Alíquota/cálculo variável: `sql_query_aliquota`

- **Caminho:** `tabativ -> ativtipo -> tipcalc -> cadcalc`.
- **Condições padrão:**
  - `cadcalc.q85_var IS TRUE`
  - `tabativ.q07_datafi IS NULL`
  - `tabativ.q07_databx IS NULL`
  - `tabativ.q07_inscr = :inscricao`
- **Objetivo observado:** Buscar configuração/alíquota de atividade variável.
- **Defeito:** Quando `$dbwhere` é informado, o método substitui toda a cláusula padrão por `AND $dbwhere`, produzindo SQL sem `WHERE`.
- **Uso seguro:** Não fornecer `$dbwhere`; filtrar pela inscrição e pelos critérios fixos.

### Consulta genérica de atividade/alíquota: `sql_query_atividade_aliquota`

- **Mesmos joins:** `tabativ`, `ativtipo`, `tipcalc`, `cadcalc`.
- **Diferença:** Não fixa atividade ativa nem cálculo variável; todos os critérios dependem dos parâmetros.
- **Cuidados:** Para reproduzir `sql_query_aliquota`, informar explicitamente `q85_var IS TRUE`, `q07_datafi IS NULL` e `q07_databx IS NULL`.

---

### Inscrições relacionadas a um CGM: `sqlinscricoes_nome`

- **Objetivo:** Retornar inscrições em que o CGM é titular/autônomo ou sócio.
- **Bloco titular:**
  - `issbase.q02_numcgm = cgm.z01_numcgm`
  - Classifica como `EMPRESA` quando existe em `db_cgmcgc`.
  - Caso contrário classifica como `AUTONOMO`.
- **Bloco sócio:**
  - `socios.q95_cgmpri = issbase.q02_numcgm`
  - `socios.q95_numcgm = :cgm_pesquisado`
  - Classifica como `SOCIO`.
- **Combinação:** `UNION`, removendo duplicações idênticas.
- **Cuidados:** O parâmetro se chama `$pesquisaPorNome`, mas é comparado numericamente com CGM, não com nome.

### Sócios da inscrição: `sqlinscricoes_socios`

- **Caminho:** `issbase -> socios -> cgm` do sócio e CGM da empresa.
- **Qualificação:** `LEFT JOIN qualificacaosocio`.
- **Filtros alternativos:**
  - Por inscrição: `q02_inscr = :inscricao`.
  - Senão, por CGM titular: `q02_numcgm = :cgm`.
- **Tipo padrão:** `socios.q95_tipo = 1`.
- **Join configurável:** O parâmetro `$innerleft` escolhe `INNER JOIN` ou `LEFT OUTER JOIN` com `socios`.
- **Cuidados:**
  - Com `LEFT JOIN` e filtro padrão `q95_tipo = 1`, inscrições sem sócio continuam excluídas pelo `WHERE`.
  - Para listar todos os tipos, passar `$tipo = null`.

---

### Inscrições por setor fiscal: `sql_query_setorfiscal`

- **Caminho:** `issbase -> cgm -> isssetorfiscal`.
- **Filtro:** `isssetorfiscal.q177_setorfiscal = :setor`.
- **Grão:** Vínculo da inscrição com setor fiscal.
- **Cuidados:** A consulta não filtra inscrição ativa.

### Vínculo sanitário pelo CGM: `sql_query_cgm_sanitario`

- **Caminho:** `issbase LEFT JOIN sanitarioinscr`.
- **Filtro quando informado:** `q02_numcgm = :cgm AND y18_codsani IS NOT NULL`.
- **Observação:** O parâmetro é chamado `$inscricao`, mas o método filtra CGM.
- **Grão:** Inscrição com cadastro sanitário vinculado.
- **Cuidados:** Sem parâmetro, retorna todas as inscrições, inclusive sem vínculo sanitário.

### Inscrição ativa por CGM: `sql_queryInscricaoAtivaCgm`

- **Regra comprovada:** `q02_dtbaix IS NULL`.
- **Filtro:** `cgm.z01_numcgm = :cgm`.
- **Ordenação:** `q02_inscr`.
- **Cuidados:** Um CGM pode possuir mais de uma inscrição ativa; não assumir resultado único.

```sql
SELECT *
FROM issbase
JOIN cgm ON cgm.z01_numcgm = issbase.q02_numcgm
WHERE issbase.q02_dtbaix IS NULL
  AND cgm.z01_numcgm = :cgm
ORDER BY issbase.q02_inscr;
```

---

### MEI: `sql_query_mei`

- **Intenção:** Relacionar `issbase.q02_numcgm` com `meicgm.q115_numcgm`.
- **Estado desta versão:** O método monta `$sSql`, mas não executa `return`.
- **Defeitos adicionais:**
  - Quando `$dbWhere` é informado, concatena `$sWhere` consigo mesmo em vez de usar `$dbWhere`.
  - Pode gerar `...q02_inscr = valorand...` sem espaço.
- **Regra de uso:** Não tratar este método como consulta executável. Reconstituir manualmente:

```sql
SELECT /* campos */
FROM issbase
JOIN meicgm
  ON meicgm.q115_numcgm = issbase.q02_numcgm
WHERE issbase.q02_inscr = :inscricao;
```

### Simples Nacional: `sql_query_isscadsimples`

- **Intenção:** Relacionar inscrição com `isscadsimples.q38_inscr`.
- **Estado desta versão:** Não retorna `$sSql`.
- **Defeitos adicionais:**
  - O `INNER JOIN` foi montado sem a palavra `ON`.
  - `$dbWhere` não é incorporado corretamente.
- **Regra de uso:** Não executar a SQL gerada por este método; reconstruir o join com `ON isscadsimples.q38_inscr = issbase.q02_inscr`.

### Dados de cálculo: `sql_query_dados_calculo`

- **Intenção:** Consultar a inscrição com dados opcionais de `isscalc`.
- **Vínculo:** `isscalc.q01_inscr = issbase.q02_inscr`.
- **Estado desta versão:** O método não retorna `$sSql`.
- **Defeito de filtro:** `$dbWhere` não é incorporado corretamente.
- **SQL reconstruída:**

```sql
SELECT /* campos */
FROM issbase
LEFT JOIN isscalc
  ON isscalc.q01_inscr = issbase.q02_inscr
WHERE issbase.q02_inscr = :inscricao;
```

---

### Registro do Simples por competência: `sql_query_get_cgm_issarqsimplesreg`

- **Objetivo:** Encontrar inscrição vinculada a um registro de arquivo do Simples Nacional para determinado CGM.
- **Caminho:** `issbase -> cgm -> issarqsimplesregissbase -> issarqsimplesreg`.
- **Filtros:**
  - `z01_numcgm = :cgm`
  - `q134_issarqsimplesreg = :registro`
  - Inscrição sem baixa ou com baixa no primeiro dia da competência ou depois.
- **Competência:** `(q23_anousu || '-' || q23_mesusu || '-01')::date`.
- **Regra de vigência:** `q02_dtbaix >= início_da_competência OR q02_dtbaix IS NULL`.
- **Cuidados:** Essa condição considera inscrição baixada durante/depois do início do mês como válida para o registro.

### Processo protocolado da inscrição: `sql_query_processo`

- **Caminho:** `issbase -> issprocesso -> protprocesso`.
- **Vínculos:**
  - `issprocesso.q14_inscr = issbase.q02_inscr`
  - `protprocesso.p58_codproc = issprocesso.q14_proces`
- **Filtro:** `protprocesso.p58_codproc = :processo`.
- **Grão:** Vínculo entre inscrição e processo.

---

### Numeração contínua: `incluirNumeracaoContinua` e `getNumeroContinuo`

- **Objetivo:** Gerar inscrição sem saltos usando `issbasenumeracao`, em vez de depender apenas da sequence.
- **Fluxo:**
  1. Incrementa `issbasenumeracao.q133_numeracaoatual`.
  2. Lê o último registro por `q133_sequencial DESC`.
  3. Atribui o número a `q02_inscr`.
  4. Sincroniza `issbase_q02_inscr_seq` com `setval`.
- **Transação:** Abre transação apenas quando não existe uma transação externa.
- **Cuidados:**
  - O `UPDATE issbasenumeracao` não possui `WHERE`; todos os registros são incrementados.
  - Depois escolhe apenas o último registro. A configuração deve garantir a cardinalidade esperada.
  - Esta é regra de gravação, não consulta analítica.

### Cuidados gerais

- Inscrição ativa: `q02_dtbaix IS NULL`.
- Atividade ativa: normalmente `q07_databx IS NULL`; algumas consultas também exigem `q07_datafi IS NULL`.
- Um CGM pode possuir várias inscrições e uma inscrição pode possuir várias atividades, sócios ou veículos.
- Não contar linhas após joins sem usar `COUNT(DISTINCT q02_inscr)` quando a entidade for inscrição.
- `empresa` é uma view; validar sua definição antes de inferir origem dos campos.
- Os métodos `sql_query_mei`, `sql_query_isscadsimples` e `sql_query_dados_calculo` estão incompletos/defeituosos nesta versão.
- Para CNAE e atividade principal, complementar com `knowledge/rag/issqn/atividades.md`.
- Para visão conceitual, consultar `knowledge/rag/issqn/cadastro_mobiliario_e_servicos.md`.
