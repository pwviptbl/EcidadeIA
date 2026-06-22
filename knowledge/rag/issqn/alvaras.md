## issqn.alvaras

Mapeia as regras de negócio para emissão, consulta e controle de Alvarás de Funcionamento e Vistoria das inscrições municipais.

---

### Regras de Negócio e Raciocínio Tributário (Alvarás)

1. **Tipos de Alvará e Finalidades:**
   - **Alvará de Funcionamento/Localização:** Autoriza o estabelecimento a exercer suas atividades comerciais, industriais ou prestação de serviços no território municipal.
   - **Alvará Sanitário / Licença Ambiental:** Exigido para setores específicos (alimentício, saúde, químico) e depende de vistorias técnicas.
   - O e-Cidade classifica estes tipos na tabela `isstipoalvara`. O Agente deve buscar o nome descritivo (`q98_descricao`) para identificar a finalidade específica.

2. **Regras de Geração de Taxa:**
   - Em `isstipoalvara`, o campo `q98_gerataxa` define se a emissão/renovação daquele tipo de alvará dispara automaticamente a cobrança de uma taxa municipal de vistoria/funcionamento.
   - Se `q98_gerataxa` for verdadeiro, a emissão do alvará gera um débito correspondente na conta corrente do contribuinte (arrecadação), que deve ser pago.

3. **Status de Validade (Situação):**
   - Os alvarás possuem uma situação representada em `issalvara.q123_situacao`.
   - Valores confirmados nos modelos: `1 = ativo` e `2 = inativo`.
   - Baixa altera o alvará para inativo; renovação e liberação alteram para ativo.
   - Cancelamento, vencimento e outras condições são registrados por movimentações e não devem ser inferidos apenas de `q123_situacao`.

4. **Inadimplência Tributária:**
   - A classe `db_issalvara_classe.php` não consulta `arrecad` nem implementa bloqueio por inadimplência.
   - Se o município bloquear emissão ou renovação por débitos, essa regra deve ser comprovada no serviço/tela responsável ou na legislação/configuração local.

---

### Conceitos & Relacionamentos Base
Para controlar e consultar os Alvarás vinculados às empresas:
- `issbase.q02_inscr = issalvara.q123_inscr`
- `issalvara.q123_isstipoalvara = isstipoalvara.q98_sequencial`

> **Regras de Negócio e Situação:** 
> - A data de emissão/criação do alvará é registrada em `q123_dtinclusao`.
> - O tipo do alvará (ex: Vistoria, Funcionamento, Provisório) está em `isstipoalvara.q98_descricao`.

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Quantos alvarás foram emitidos por tipo no exercício de 2025?
- **Descrição:** Conta e agrupa os alvarás gerados/emitidos no ano de 2025 pelo seu tipo descritivo.
- **Receita SQL:**
```sql
SELECT ta.q98_descricao as tipo_alvara, COUNT(a.q123_sequencial) as quantidade_emitida
FROM issqn.issalvara a
JOIN issqn.isstipoalvara ta ON a.q123_isstipoalvara = ta.q98_sequencial
WHERE EXTRACT(YEAR FROM a.q123_dtinclusao) = 2025
GROUP BY ta.q98_descricao
ORDER BY quantidade_emitida DESC;
```

#### 2. Quais alvarás ativos estão vinculados a uma determinada empresa (Inscrição)?
- **Descrição:** Retorna a listagem de alvarás de uma empresa específica com base no número da inscrição municipal.
- **Receita SQL:**
```sql
SELECT a.q123_sequencial as numero_alvara, ta.q98_descricao as tipo_alvara, a.q123_dtinclusao as data_emissao
FROM issqn.issalvara a
JOIN issqn.isstipoalvara ta ON a.q123_isstipoalvara = ta.q98_sequencial
WHERE a.q123_inscr = :inscricao
  AND a.q123_situacao = 1
ORDER BY a.q123_dtinclusao DESC;
```

---

## Consultas extraídas de `db_issalvara_classe.php`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_issalvara_classe.php`
- **Classe:** `cl_issalvara`
- **Tabela principal:** `issqn.issalvara`
- **Chave:** `q123_sequencial`
- **Inscrição municipal:** `q123_inscr`
- **Tipo de alvará:** `q123_isstipoalvara`
- **Data de criação/liberação:** `q123_dtinclusao`
- **Situação:** `q123_situacao`
- **Usuário:** `q123_usuario`
- **Geração automática:** `q123_geradoautomatico`
- **Grão:** Um alvará cadastrado para uma inscrição municipal.

### Leitura completa: `sql_query`

- **Objetivo:** Recuperar o alvará com empresa, contribuinte, tipo, grupo e template de documento.
- **Junções obrigatórias:**
  - `issbase.q02_inscr = issalvara.q123_inscr`
  - `cgm.z01_numcgm = issbase.q02_numcgm`
  - `isstipoalvara.q98_sequencial = issalvara.q123_isstipoalvara`
  - `db_documentotemplate.db82_sequencial = isstipoalvara.q98_documento`
  - `issgrupotipoalvara.q97_sequencial = isstipoalvara.q98_issgrupotipoalvara`
- **Filtro padrão:** `issalvara.q123_sequencial = :sequencial`.
- **Cuidados:** Todos os relacionamentos são internos. Alvará sem template, grupo, tipo, inscrição ou CGM válido não aparece.

```sql
SELECT /* campos dinâmicos */
FROM issalvara
JOIN issbase
  ON issbase.q02_inscr = issalvara.q123_inscr
JOIN isstipoalvara
  ON isstipoalvara.q98_sequencial = issalvara.q123_isstipoalvara
JOIN cgm
  ON cgm.z01_numcgm = issbase.q02_numcgm
JOIN db_documentotemplate
  ON db_documentotemplate.db82_sequencial = isstipoalvara.q98_documento
JOIN issgrupotipoalvara
  ON issgrupotipoalvara.q97_sequencial =
     isstipoalvara.q98_issgrupotipoalvara
WHERE issalvara.q123_sequencial = :sequencial;
```

### Leitura física: `sql_query_file`

- **Objetivo:** Consultar somente os campos de `issalvara`.
- **Filtro padrão:** `q123_sequencial = :sequencial`.
- **Uso recomendado:** Obter situação, inscrição, tipo, usuário ou indicador de geração automática sem exigir cadastros auxiliares.

### Elegibilidade para liberação: `sql_queryAlvara`

- **Objetivo:** Selecionar alvarás disponíveis para liberação.
- **Dados básicos:** `issalvara -> issbase -> cgm`.
- **Última movimentação:** Subconsulta em `issmovalvara`, ordenada por `q120_sequencial DESC`, limitada a uma linha.
- **Regra comprovada:** O alvará é elegível quando:
  - Não possui movimentação; ou
  - A última movimentação é `2` (baixa); ou
  - A última movimentação é `6` (cancelamento de liberação).
- **Departamento opcional:** Quando informado, exige vínculo do tipo de alvará em `isstipoalvaradepto.q99_depto`.
- **Campos derivados:**
  - `dl_tipo_alvara = q123_isstipoalvara`
  - `dl_ultima_movimentacao`
  - `dl_automatico = q123_geradoautomatico`
- **Cuidados:**
  - A consulta não filtra diretamente `q123_situacao`.
  - A elegibilidade é determinada pela última movimentação, não apenas pelo estado ativo/inativo.
  - O `ORDER BY q123_sequencial` interno não altera a escolha da última movimentação, que possui sua própria ordenação.

```sql
SELECT *
FROM (
  SELECT
    /* campos dinâmicos */,
    q123_isstipoalvara AS dl_tipo_alvara,
    (
      SELECT q120_isstipomovalvara
      FROM issmovalvara
      WHERE q120_issalvara = q123_sequencial
      ORDER BY q120_sequencial DESC
      LIMIT 1
    ) AS dl_ultima_movimentacao,
    q123_geradoautomatico AS dl_automatico
  FROM issalvara
  JOIN issbase ON issbase.q02_inscr = issalvara.q123_inscr
  JOIN cgm ON cgm.z01_numcgm = issbase.q02_numcgm
) AS x
WHERE dl_ultima_movimentacao IS NULL
   OR dl_ultima_movimentacao IN (2, 6);
```

### Seleção para baixa: `sql_queryBaixa`

- **Objetivo:** Consultar alvarás por inscrição/contribuinte, tipo, grupo, template e departamento responsável.
- **Junção adicional:** `isstipoalvaradepto.q99_isstipoalvara = issalvara.q123_isstipoalvara`.
- **Regra usada pela tela:** O consumidor acrescenta:
  - `q99_depto = DB_coddepto`
  - `q123_situacao = 1`
- **Resultado prático:** A tela de baixa seleciona alvarás ativos cujo tipo está vinculado ao departamento atual.
- **Cuidados:** O método isolado não fixa situação nem departamento; essas condições vêm de `func_issalvarabaixa.php`.

### Elegibilidade para renovação: `sql_queryConsultaRenovacao`

- **Objetivo:** Retornar alvarás ativos cujo tipo permite renovação e ainda não atingiu o limite configurado.
- **Condições fixas:**
  - `isstipoalvara.q98_permiterenovacao IS TRUE`
  - `issalvara.q123_situacao = 1`
- **Quantidade permitida:** `q98_quantrenovacao`.
- **Renovações líquidas:**

```sql
COUNT(movimentação 4) - COUNT(movimentação 8)
```

- **Códigos confirmados:**
  - `4` - renovação.
  - `8` - cancelamento de renovação.
- **Regra final:** `dl_Renovacoes < q98_quantrenovacao`.
- **Departamento:** A tela normalmente filtra `q99_depto = DB_coddepto`.
- **Grão:** Um alvará elegível; o `DISTINCT` remove duplicações causadas pelos joins com movimentação e departamento.
- **Cuidados:**
  - Renovação cancelada reduz a contagem líquida.
  - `q98_permiterenovacao` e `q98_quantrenovacao` pertencem ao tipo do alvará.
  - A consulta não verifica débitos tributários.

```sql
SELECT DISTINCT /* campos */, dl_Renovacoes
FROM (
  SELECT
    /* campos */,
    q98_quantrenovacao,
    (
      SELECT COUNT(*)
      FROM issmovalvara
      WHERE q120_issalvara = q123_sequencial
        AND q120_isstipomovalvara = 4
    ) - (
      SELECT COUNT(*)
      FROM issmovalvara
      WHERE q120_issalvara = q123_sequencial
        AND q120_isstipomovalvara = 8
    ) AS dl_Renovacoes
  FROM issalvara
  JOIN issbase ON issbase.q02_inscr = issalvara.q123_inscr
  JOIN cgm ON cgm.z01_numcgm = issbase.q02_numcgm
  JOIN isstipoalvara
    ON isstipoalvara.q98_sequencial = issalvara.q123_isstipoalvara
  LEFT JOIN issmovalvara
    ON issmovalvara.q120_issalvara = issalvara.q123_sequencial
  LEFT JOIN isstipoalvaradepto
    ON isstipoalvaradepto.q99_isstipoalvara =
       issalvara.q123_isstipoalvara
  WHERE q98_permiterenovacao IS TRUE
    AND issalvara.q123_situacao = 1
) AS x
WHERE dl_Renovacoes < q98_quantrenovacao;
```

### Elegibilidade para cancelamento: `sql_queryConsultaCancelamento`

- **Objetivo:** Selecionar alvarás com uma movimentação efetiva que possa ser cancelada.
- **Dados:** `issalvara`, `issbase`, `cgm`, `isstipoalvara` e `isstipoalvaradepto`.
- **Última movimentação considerada:** A subconsulta ignora movimentações de cancelamento:
  - `3` - cancelamento.
  - `5` - transformação.
  - `6` - cancelamento de liberação.
  - `7` - cancelamento de baixa.
  - `8` - cancelamento de renovação.
- **Regra final:** `cod_ult_mov IS NOT NULL`.
- **Interpretação:** Precisa existir ao menos uma movimentação não pertencente ao conjunto excluído; a tela pode então cancelar a última movimentação considerada válida.
- **Departamento:** O consumidor acrescenta `q99_depto = DB_coddepto`.
- **Cuidados:**
  - A lista exclui também o código `5`, que o modelo nomeia como transformação. Portanto, esta consulta não considera transformação como movimento cancelável neste fluxo.
  - Não existe filtro fixo de `q123_situacao`.
  - O `sWhere` é aplicado fora da subconsulta e deve usar colunas expostas por `x`.

```sql
SELECT /* campos */
FROM (
  SELECT *,
    (
      SELECT q120_isstipomovalvara
      FROM issmovalvara
      WHERE q120_issalvara = q123_sequencial
        AND q120_isstipomovalvara NOT IN (3, 5, 6, 7, 8)
      ORDER BY q120_sequencial DESC
      LIMIT 1
    ) AS cod_ult_mov
  FROM issalvara
  JOIN issbase ON issbase.q02_inscr = issalvara.q123_inscr
  JOIN cgm ON cgm.z01_numcgm = issbase.q02_numcgm
  JOIN isstipoalvara
    ON isstipoalvara.q98_sequencial = issalvara.q123_isstipoalvara
  JOIN isstipoalvaradepto
    ON isstipoalvaradepto.q99_isstipoalvara =
       isstipoalvara.q98_sequencial
) AS x
WHERE cod_ult_mov IS NOT NULL;
```

### Movimentações confirmadas

- `2` - baixa.
- `3` - cancelamento.
- `4` - renovação.
- `5` - transformação.
- `6` - cancelamento de liberação.
- `7` - cancelamento de baixa.
- `8` - cancelamento de renovação.

O código `1` aparece em relatórios como movimentação relevante e é compatível com liberação, mas seu nome não é declarado nas constantes lidas desta classe. Tratar como liberação somente com a evidência do modelo de movimentação correspondente.

### Cuidados gerais

- `q123_situacao = 1` significa ativo e `2` significa inativo.
- Baixa e renovação atualizam a situação, mas o histórico completo está em `issmovalvara`.
- Para saber a ação mais recente, ordenar `issmovalvara.q120_sequencial DESC`.
- Um tipo pode estar ligado a mais de um departamento, multiplicando linhas.
- A existência de template é obrigatória em `sql_query` e `sql_queryBaixa`, mas não nas consultas de liberação, renovação e cancelamento.
- `q123_dtinclusao` é data de criação/liberação do cadastro, não data de cada movimentação.
- `q123_geradoautomatico` diferencia geração automática de fluxo manual, sem definir sozinho validade ou situação.
- A geração de taxa está configurada em `isstipoalvara.q98_gerataxa`, mas esta classe não gera nem consulta o débito.
