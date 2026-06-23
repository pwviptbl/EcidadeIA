## empenho.empelemento

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_empelemento_classe.php`

Detalha o empenho por elemento de despesa. A classe registra, para cada empenho e elemento, os valores empenhado, liquidado, anulado e pago, e faz validacao interna para evitar pagamento acima do valor do empenho.

### Estrutura e interpretacao

- **Classe:** `cl_empelemento`
- **Tabela principal:** `empelemento`
- **Chave primaria composta:** `e64_numemp`, `e64_codele`
- **Grau basico:** uma linha por combinacao de empenho e elemento de despesa

Campos de negocio confirmados:

- `e64_numemp`: numero do empenho
- `e64_codele`: codigo do elemento de despesa
- `e64_vlremp`: valor empenhado no elemento
- `e64_vlrliq`: valor liquidado no elemento
- `e64_vlranu`: valor anulado no elemento
- `e64_vlrpag`: valor pago no elemento

Interpretacao segura:

- A tabela reparte o empenho por elemento orcamentario, nao por lancamento contabil.
- `e64_codele` deve ser interpretado junto de `orcelemento` no exercicio do empenho.
- Os valores representam o estado financeiro do elemento dentro daquele empenho.

### Consulta: `sql_query`

- **Objetivo:** recuperar o detalhamento por elemento com enriquecimento do empenho, elemento, CGM, instituicao, dotacao e tipo de empenho.
- **Tabelas:** `empelemento`, `empempenho`, `orcelemento`, `cgm`, `db_config`, `orcdotacao`, `emptipo`

```sql
select /* campos dinamicos */
  from empelemento
       inner join empempenho
          on empempenho.e60_numemp = empelemento.e64_numemp
       inner join orcelemento
          on orcelemento.o56_codele = empelemento.e64_codele
         and orcelemento.o56_anousu = empempenho.e60_anousu
       inner join cgm
          on cgm.z01_numcgm = empempenho.e60_numcgm
       inner join db_config
          on db_config.codigo = empempenho.e60_instit
       inner join orcdotacao
          on orcdotacao.o58_anousu = empempenho.e60_anousu
         and orcdotacao.o58_coddot = empempenho.e60_coddot
       inner join emptipo
          on emptipo.e41_codtipo = empempenho.e60_codtipo
 where empelemento.e64_numemp = :numemp
   and empelemento.e64_codele = :codele
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta principal para entender o elemento no contexto completo do empenho.
- O join do elemento depende do exercicio do empenho, o que evita resolver o codigo no ano errado.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `empelemento`.

```sql
select /* campos dinamicos */
  from empelemento
 where empelemento.e64_numemp = :numemp
   and empelemento.e64_codele = :codele
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar a linha base do elemento;
- ler somente os valores armazenados sem joins adicionais.

### Regra interna: `validarValorPago`

- **Objetivo:** impedir inconsistencias de pagamento acima do valor do empenho.
- **Tabelas usadas na validacao:** `empelemento`, `empempenho`, `orcelemento`, `cgm`, `db_config`, `orcdotacao`, `emptipo`

Regras observadas:

- a rotina compara `pago` com `vlr_empenho`;
- se `e64_vlrpag` superar o valor do empenho, a classe marca erro com a mensagem de que o empenho ja teve seu valor integral pago;
- a validacao e chamada apos `alterar()`.

Interpretacao segura:

- A classe protege o saldo do elemento no nivel do empenho.
- Em manutencoes ou backfills, alterar `e64_vlrpag` sem respeitar esta regra pode quebrar a consistencia esperada pelo legado.

### Regras de manutencao observadas

1. `incluir()` exige `e64_vlremp`, `e64_vlrliq`, `e64_vlranu` e `e64_vlrpag`.
2. `alterar()` aplica `SELECT ... FOR UPDATE` em `empelemento` por `e64_numemp` antes de atualizar, para serializar pagamentos e liquidacoes.
3. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.

### Relacionamentos de negocio confirmados no catalogo

- `empelemento.e64_numemp -> empempenho.e60_numemp`

Interpretacao segura:

- `empelemento` depende do empenho como entidade pai.
- O contexto orcamentario e institucional vem do caminho `empelemento -> empempenho -> orcdotacao`.

### Cuidados para consultas do agente

- Nao some `empelemento` com `empempenho` sem considerar que um mesmo empenho pode ter varios elementos.
- Para descricao textual do elemento, resolva `e64_codele` em `orcelemento` no ano do empenho.
- Quando a pergunta envolver saldos ou pagamentos, observe que a propria classe tenta impedir `e64_vlrpag > e64_vlremp`.
