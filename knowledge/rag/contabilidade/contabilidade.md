## contabilidade.contabilidade

Mapeia as regras de negócio para análise do Plano de Contas (conplano), contas reduzidas (conplanoreduz) e lançamentos contábeis.

---

### Conceitos & Relacionamentos Base

1. **Plano de Contas (`conplano`):**
   - Mapeia toda a árvore contábil municipal do exercício.
   - `c60_anousu`: Ano/exercício do plano de contas.
   - `c60_codcon`: Código sequencial interno da conta.
   - `c60_descr`: Nome/descrição da conta contábil.
   - `c60_estrut`: Código estrutural formatado (ex: `1.1.1.1.1.01.00`).

2. **Contas Reduzidas (`conplanoreduz`):**
   - No dia a dia, a contabilidade utiliza "contas reduzidas" para simplificar lançamentos.
   - `c61_reduz`: O código reduzido da conta.
   - `c61_codcon`: Associa a conta reduzida ao código completo da conta contábil correspondente em `conplano`.
   - **Junção:** `conplanoreduz.c61_codcon = conplano.c60_codcon` AND `conplanoreduz.c61_anousu = conplano.c60_anousu`

---

### Perguntas de Negócio Frequentes & Receitas SQL

#### 1. Pesquisar contas do plano de contas por nome (termo parcial com busca resiliente a acentos)
- **Descrição:** Busca contas no plano de contas de um determinado ano que atendam ao critério textual.
- **Receita SQL:**
```sql
SELECT 
    c60_estrut as estrutural,
    c60_descr as descricao
FROM contabilidade.conplano
WHERE c60_anousu = :ano
  AND fc_semacento(c60_descr) ILIKE fc_semacento('%Caixa e Equivalentes%')
ORDER BY c60_estrut;
```

#### 2. Listar as contas reduzidas ativas e seus respectivos códigos estruturais completos
- **Descrição:** Retorna a listagem de códigos reduzidos utilizados no ano com seus respectivos estruturais e descrições do plano de contas.
- **Receita SQL:**
```sql
SELECT 
    r.c61_reduz as codigo_reduzido,
    p.c60_estrut as estrutural,
    p.c60_descr as descricao
FROM contabilidade.conplanoreduz r
JOIN contabilidade.conplano p ON r.c61_codcon = p.c60_codcon AND r.c61_anousu = p.c60_anousu
WHERE r.c61_anousu = :ano
ORDER BY r.c61_reduz;
```
