## orcamento.orcamento

Mapeia as regras de negócio para análise da receita prevista, despesa fixada e dotações orçamentárias (orcdotacao).

---

### Conceitos & Relacionamentos Base
A dotação orçamentária (`orcdotacao`) é a autorização de despesa pública associada a um determinado ano (exercício), órgão, elemento de despesa e função.

- **Dotação:** `orcamento.orcdotacao`
  - `o58_anousu`: Ano/exercício do orçamento.
  - `o58_coddot`: Código reduzido da dotação (Primary Key junto com `o58_anousu`).
  - `o58_valor`: Valor fixado da dotação (Orçamento inicial previsto para a despesa).
- **Órgão e Unidade:** `orcamento.orcorgao` e `orcamento.orcunidade`
  - `orcdotacao.o58_orgao = orcorgao.o40_orgao` E `orcdotacao.o58_anousu = orcorgao.o40_anousu`
  - `orcdotacao.o58_unidade = orcunidade.o41_unidade` E `orcdotacao.o58_orgao = orcunidade.o41_orgao` E `orcdotacao.o58_anousu = orcunidade.o41_anousu`
- **Elemento de Despesa:** `orcamento.orcelemento`
  - `orcdotacao.o58_codele = orcelemento.o56_codele` E `orcdotacao.o58_anousu = orcelemento.o56_anousu`

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Qual o orçamento total previsto (despesa fixada) para um exercício específico?
- **Descrição:** Retorna a soma de todas as dotações iniciais fixadas para um determinado ano.
- **Receita SQL:**
```sql
SELECT SUM(o58_valor) as total_orcamento
FROM orcamento.orcdotacao
WHERE o58_anousu = :ano;
```

#### 2. Quais órgãos possuem as maiores dotações orçamentárias previstas no ano?
- **Descrição:** Lista os órgãos governamentais (`orcorgao`) classificados pelo valor total sob sua gestão no ano.
- **Receita SQL:**
```sql
SELECT 
    org.o40_orgao as codigo_orgao, 
    org.o40_descr as nome_orgao, 
    SUM(dot.o58_valor) as valor_total_orcado
FROM orcamento.orcdotacao dot
JOIN orcamento.orcorgao org ON dot.o58_orgao = org.o40_orgao AND dot.o58_anousu = org.o40_anousu
WHERE dot.o58_anousu = :ano
GROUP BY org.o40_orgao, org.o40_descr
ORDER BY valor_total_orcado DESC;
```
