## issqn.atividades

Mapeia as regras de negócio para consulta, contagem e agrupamento de empresas (inscrições econômicas) por suas respectivas atividades (CNAE).

---

### Regras de Negócio e Raciocínio Tributário (Atividades e CNAE)

1. **Estado de Atividade da Empresa (Ativa vs Baixada):**
   - Uma empresa (`issbase`) possui um status global de atividade. Se `issbase.q02_dtbaix` estiver preenchido (não nulo), a empresa inteira foi baixada (está inativa) na data registrada.
   - Cada atividade individual vinculada à empresa (`tabativ`) possui seu próprio ciclo de vida. Uma atividade só está ativa para aquela empresa se `tabativ.q07_databx` for nulo E a data atual for igual ou posterior à data de início (`tabativ.q07_datain`).
   - É possível que uma empresa ativa possua atividades individuais inativas (baixadas), ou vice-versa (o que representaria uma inconsistência). Consultas sobre empresas ativas devem sempre filtrar `q02_dtbaix IS NULL` e `q07_databx IS NULL`.

2. **Hierarquia e Código Estrutural do CNAE:**
   - O código do CNAE (`cnae.q71_estrutural`) é estruturado em níveis (ex: '6201-5/01').
   - Filtros por "grupo de atividade" ou "setor" podem ser feitos usando correspondência parcial (`LIKE '62%'` ou `LIKE '6201%'`) no código estrutural.
   - O cadastro de CNAEs é analítico: associações diretas são feitas na tabela `cnaeanalitica`.

3. **Atividade Principal vs Secundária:**
   - Uma empresa pode exercer dezenas de atividades, mas perante o fisco municipal ela possui apenas **uma** Atividade Principal.
   - A atividade principal determina a alíquota padrão de ISSQN estimado ou o enquadramento fiscal principal da empresa.
   - Embora a tabela `tabativ` liste todas as atividades, a indicação de qual é a principal é registrada na tabela `issqn.ativprinc` (que associa a inscrição `q07_inscr` ao código correspondente).

4. **Enquadramento do MEI (Microempreendedor Individual):**
   - Nem todas as atividades econômicas são permitidas para o regime de MEI. O sistema controla essa permissão pelo flag `cnae.q71_permitemei = true`.
   - Empresas enquadradas como MEI têm tributação fixa unificada nacionalmente e geralmente são isentas de ISSQN próprio municipal (recolhem via DAS-MEI), o que altera as regras de cobrança de taxas de alvará de funcionamento no e-Cidade.

---

### Conceitos & Relacionamentos Base
Para vincular uma empresa/inscrição (`issqn.issbase`) aos seus códigos CNAE:
- `issbase.q02_inscr = tabativ.q07_inscr`
- `tabativ.q07_ativ = ativid.q03_ativ`
- `ativid.q03_ativ = atividcnae.q74_ativid`
- `atividcnae.q74_cnaeanalitica = cnaeanalitica.q72_sequencial`
- `cnaeanalitica.q72_cnae = cnae.q71_sequencial`

> **Rigor de Status:** Uma atividade é considerada ativa para a empresa se a data de baixa `tabativ.q07_databx` for nula. A empresa inteira é considerada ativa se `issbase.q02_dtbaix` for nula.

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Quantas empresas ativas estão cadastradas em um determinado código CNAE?
- **Descrição:** Conta as inscrições municipais ativas que exercem um CNAE específico (filtrado pelo código estrutural).
- **Receita SQL:**
```sql
SELECT COUNT(DISTINCT i.q02_inscr) as total_empresas
FROM issqn.issbase i
JOIN issqn.tabativ ta ON i.q02_inscr = ta.q07_inscr
JOIN issqn.ativid a ON ta.q07_ativ = a.q03_ativ
JOIN issqn.atividcnae ac ON a.q03_ativ = ac.q74_ativid
JOIN issqn.cnaeanalitica ca ON ac.q74_cnaeanalitica = ca.q72_sequencial
JOIN issqn.cnae c ON ca.q72_cnae = c.q71_sequencial
WHERE i.q02_dtbaix IS NULL
  AND ta.q07_databx IS NULL
  AND c.q71_estrutural = :codigo_cnae;
```

#### 2. Quais são as atividades (CNAEs) mais comuns entre as empresas ativas do município?
- **Descrição:** Retorna os CNAEs com o maior número de empresas ativas vinculadas, ordenados do maior para o menor.
- **Receita SQL:**
```sql
SELECT c.q71_estrutural as cnae, c.q71_descr as descricao, COUNT(DISTINCT i.q02_inscr) as total_empresas
FROM issqn.issbase i
JOIN issqn.tabativ ta ON i.q02_inscr = ta.q07_inscr
JOIN issqn.ativid a ON ta.q07_ativ = a.q03_ativ
JOIN issqn.atividcnae ac ON a.q03_ativ = ac.q74_ativid
JOIN issqn.cnaeanalitica ca ON ac.q74_cnaeanalitica = ca.q72_sequencial
JOIN issqn.cnae c ON ca.q72_cnae = c.q71_sequencial
WHERE i.q02_dtbaix IS NULL
  AND ta.q07_databx IS NULL
GROUP BY c.q71_estrutural, c.q71_descr
ORDER BY total_empresas DESC
LIMIT 10;
```

#### 3. Listar as atividades de uma empresa específica (por Inscrição ou CPF/CNPJ via CGM)
- **Descrição:** Retorna todas as atividades ativas vinculadas a uma empresa usando o número de inscrição municipal.
- **Receita SQL:**
```sql
SELECT c.q71_estrutural as cnae, c.q71_descr as descricao, ta.q07_datain as data_inicio
FROM issqn.issbase i
JOIN issqn.tabativ ta ON i.q02_inscr = ta.q07_inscr
JOIN issqn.ativid a ON ta.q07_ativ = a.q03_ativ
JOIN issqn.atividcnae ac ON a.q03_ativ = ac.q74_ativid
JOIN issqn.cnaeanalitica ca ON ac.q74_cnaeanalitica = ca.q72_sequencial
JOIN issqn.cnae c ON ca.q72_cnae = c.q71_sequencial
WHERE i.q02_inscr = :inscricao
  AND ta.q07_databx IS NULL;
```
