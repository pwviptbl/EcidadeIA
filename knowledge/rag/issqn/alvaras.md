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
   - A situação indica se o documento está ativo (regular/emitido), cancelado, vencido ou pendente de vistoria. Para relatórios de adimplência regulatória das empresas, a IA deve analisar essa situação junto ao cadastro base.

4. **Bloqueio por Inadimplência Tributária:**
   - De acordo com a maioria dos Códigos Tributários Municipais, a renovação ou emissão de nova via do Alvará de Funcionamento é **bloqueada** caso a inscrição municipal (`q02_inscr`) ou o contribuinte (`cgm`) possua débitos vencidos e não pagos (como ISS ou taxas de anos anteriores) na arrecadação (`caixa.arrecad`).

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
ORDER BY a.q123_dtinclusao DESC;
```
