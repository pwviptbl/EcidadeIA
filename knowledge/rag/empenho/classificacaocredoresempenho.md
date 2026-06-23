## empenho.classificacaocredoresempenho

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_classificacaocredoresempenho_classe.php`

Ligacao entre um empenho e uma lista de classificacao de credores. A classe registra qual classificacao foi associada ao empenho e, opcionalmente, a justificativa dessa vinculacao.

### Estrutura e interpretacao

- **Classe:** `cl_classificacaocredoresempenho`
- **Tabela principal:** `classificacaocredoresempenho`
- **Chave primaria:** `cc31_sequencial`
- **Grau basico:** uma linha por vinculo entre um empenho e uma classificacao de credores

Campos de negocio confirmados:

- `cc31_sequencial`: identificador do vinculo
- `cc31_empempenho`: numero do empenho associado
- `cc31_classificacaocredores`: codigo da lista de classificacao de credores
- `cc31_justificativa`: texto livre justificando a classificacao

Interpretacao segura:

- A tabela nao descreve o empenho inteiro; ela descreve apenas sua classificacao no processo de credores.
- Um mesmo empenho pode aparecer em mais de um registro se houver mais de uma classificacao associada.
- A justificativa fica no proprio vinculo, nao no cadastro da classificacao.

### Consulta: `sql_query`

- **Objetivo:** recuperar o vinculo com enriquecimento do empenho, classificacao, credor, instituicao, dotacao, tipo de compra, tipo de empenho e caracteristica peculiar.
- **Tabelas:** `classificacaocredoresempenho`, `empempenho`, `classificacaocredores`, `cgm`, `db_config`, `orcdotacao`, `pctipocompra`, `emptipo`, `concarpeculiar`

```sql
select /* campos dinamicos */
  from classificacaocredoresempenho
       inner join empempenho
          on empempenho.e60_numemp = classificacaocredoresempenho.cc31_empempenho
       inner join classificacaocredores
          on classificacaocredores.cc30_codigo = classificacaocredoresempenho.cc31_classificacaocredores
       inner join cgm
          on cgm.z01_numcgm = empempenho.e60_numcgm
       inner join db_config
          on db_config.codigo = empempenho.e60_instit
       inner join orcdotacao
          on orcdotacao.o58_anousu = empempenho.e60_anousu
         and orcdotacao.o58_coddot = empempenho.e60_coddot
       inner join pctipocompra
          on pctipocompra.pc50_codcom = empempenho.e60_codcom
       inner join emptipo
          on emptipo.e41_codtipo = empempenho.e60_codtipo
       inner join concarpeculiar
          on concarpeculiar.c58_sequencial = empempenho.e60_concarpeculiar
 where classificacaocredoresempenho.cc31_sequencial = :sequencial
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta base para responder qual classificacao de credores foi aplicada a um empenho especifico.
- O resultado continua no grao do vinculo, mas com bastante contexto do empenho.
- O join com `concarpeculiar` e `inner join`; se algum empenho nao tiver essa caracteristica preenchida no banco, a consulta pode deixar de retornar a linha.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `classificacaocredoresempenho`.

```sql
select /* campos dinamicos */
  from classificacaocredoresempenho
 where classificacaocredoresempenho.cc31_sequencial = :sequencial
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar existencia do vinculo;
- inspecionar apenas os campos gravados na tabela;
- servir de base para auditoria de inclusao, alteracao e exclusao.

### Regras de manutencao observadas

1. `incluir()` exige `cc31_empempenho` e `cc31_classificacaocredores`.
2. Quando `cc31_sequencial` nao e informado, a classe usa a sequence `classificacaocredoresempenho_cc31_sequencial_seq`.
3. Se o codigo informado for maior que o ultimo valor da sequence, a inclusao e bloqueada.
4. `cc31_justificativa` e opcional na validacao da classe.
5. Inclusao, alteracao e exclusao registram auditoria em `db_acount*` quando a sessao nao estiver com `DB_desativar_account`.

### Relacionamentos de negocio confirmados no catalogo

- `classificacaocredoresempenho.cc31_empempenho -> empempenho.e60_numemp`
- `classificacaocredoresempenho.cc31_classificacaocredores -> classificacaocredores.cc30_codigo`
- Pela cadeia de `classificacaocredores`, o vinculo alcanca `classificacaocredoreselemento`, `classificacaocredoresevento`, `classificacaocredoresrecurso` e `classificacaocredorestipocompra`.
- Pela cadeia de `empempenho`, o vinculo alcanca trilhas como `empelemento`, `empanulado` e `empempaut`.

Interpretacao segura:

- O cadastro serve como ponto de amarracao entre o empenho e a malha de regras da classificacao de credores.
- Para entender por que uma classificacao existe, normalmente e preciso abrir a cadeia pela tabela `classificacaocredores` e seus desdobramentos.

### Cuidados para consultas do agente

- Nao trate esta tabela como cadastro mestre de classificacao; o mestre esta em `classificacaocredores`.
- Nao trate `cc31_empempenho` como identificador unico da tabela; a chave primaria real e `cc31_sequencial`.
- Se a pergunta for sobre regras da classificacao, complete a consulta com joins pela cadeia de `classificacaocredores`.
- Se a pergunta for sobre dados do empenho, complete pela cadeia de `empempenho`, mas preserve o grao do vinculo para nao duplicar linhas indevidamente.
- Como o metodo `sql_query` usa varios `inner joins`, prefira `sql_query_file` quando o objetivo for apenas confirmar persistencia fisica do registro.
