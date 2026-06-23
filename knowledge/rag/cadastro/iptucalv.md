## cadastro.iptucalv

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptucalv_classe.php`

Detalhamento dos valores calculados para uma matricula no exercicio, separados por receita e historico de calculo. E a tabela que materializa os componentes monetarios do calculo, como IPTU, taxa de lixo e outros itens vinculados ao imovel.

### Estrutura e interpretacao

- **Classe:** `cl_iptucalv`
- **Tabela principal:** `iptucalv`
- **Chave de negocio observada:** `j21_anousu`, `j21_matric`, `j21_receit`, `j21_codhis`
- **Grau basico:** uma linha por exercicio, matricula, receita e historico de calculo

Campos de negocio confirmados:

- `j21_anousu`: exercicio do calculo
- `j21_matric`: matricula do imovel
- `j21_receit`: codigo da receita associada ao valor calculado
- `j21_valor`: valor calculado para aquela receita
- `j21_quant`: quantidade usada no item calculado
- `j21_codhis`: historico de calculo que originou o valor

Interpretacao segura:

- A tabela representa componentes monetarios do calculo, nao o cadastro fisico do imovel.
- Uma mesma matricula pode ter varias linhas no mesmo exercicio por possuir varias receitas e historicos.
- Para somas financeiras, o agrupamento minimo seguro costuma ser `j21_anousu`, `j21_matric` e `j21_receit`.

### Consulta: `sql_query`

- **Objetivo:** leitura basica da tabela `iptucalv`.

```sql
select /* campos dinamicos */
  from iptucalv
 where /* dbwhere dinamico, se informado */
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Apesar do nome, esta consulta nao enriquece os dados com outras tabelas.
- Ela e equivalente, na pratica, a `sql_query_file`.
- Se o agente precisar de descricao de receita, historico ou dados da matricula, os joins devem ser montados fora desse metodo.

### Consulta: `sql_query_file`

- **Objetivo:** leitura fisica direta da tabela `iptucalv`.

```sql
select /* campos dinamicos */
  from iptucalv
 where /* dbwhere dinamico, se informado */
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar persistencia de itens calculados;
- montar filtros livres por exercicio, matricula, receita e historico;
- servir de base para somas controladas sem joins desnecessarios.

### Consulta: `sql_query_hist`

- **Objetivo aparente:** ler `iptucalv` com `iptucalh`.
- **Comportamento observado na classe:** o join com `iptucalh` e montado e logo depois sobrescrito, entao a consulta final volta a ser apenas sobre `iptucalv`.

Trecho efetivo:

```sql
select /* campos dinamicos */
  from iptucalv
 where /* dbwhere dinamico, se informado */
 order by /* ordenacao dinamica */
```

Cuidados:

- Nao assuma que `sql_query_hist()` traz dados de `iptucalh`; no codigo atual isso nao acontece.
- Se a analise depender do historico, faca o join explicitamente por `iptucalv.j21_codhis = iptucalh.j17_codhis`.

### Consulta: `sql_queryValoresCalculoIptu`

- **Objetivo:** consolidar por ano e receita os valores calculados, isentos, cancelados, compensados, pagos, a pagar e importados.
- **Tabelas principais:** `iptucalv`, `tabrec`, `iptunump`, `iptucalhconf`, `iptuisen`, `isenexe`, `tipoisen`, `arrecant`, `arrecad`, `arrepaga`, `cancdebitosreg`, `cancdebitosprocreg`, `abatimentoutilizacaodestino`, `abatimentoutilizacao`, `abatimento`, `arreckey`, `abatimentoarreckey`, `arreold`, `divold`, `diverimportaold`, `diversos`, `issvar`

Interpretacao segura:

- Este metodo e analitico e trabalha no grao de receita por exercicio.
- Ele mistura calculo tributario com estado de arrecadacao, cancelamento, compensacao e importacao.
- E adequado para paineis consolidados, nao para leitura detalhada de uma matricula isolada.

### Consulta: `sql_queryIptuDiversos`

- **Objetivo:** consolidar receitas de diversos para um exercicio e tipo de arrecadacao, separando calculado, pago, cancelado, a pagar e compensado.
- **Tabelas principais:** `arrecad`, `arrecant`, `arrepaga`, `cancdebitosreg`, `cancdebitosprocreg`, `tabrec`, `diversos`, `arreckey`, `abatimentoarreckey`, `abatimento`, `abatimentoutilizacaodestino`, `abatimentoutilizacao`

Interpretacao segura:

- Este metodo nao le `iptucalv` diretamente; ele e um consolidado financeiro paralelo usado pela mesma classe.
- Use quando a pergunta for sobre diversos vinculados ao fluxo de arrecadacao, nao sobre o item bruto calculado em `iptucalv`.

### Consulta: `sql_query_taxa`

- **Objetivo:** unificar valores vindos de `iptucalv` com valores de `iptutaxacalv` para uma matricula e exercicio.
- **Tabelas:** `iptucalv`, `iptutaxacalv`, `iptutaxanump`, `iptucadtaxaexe`

```sql
select /* campos dinamicos */
  from (
        select j21_valor
          from iptucalv
         where j21_anousu = :anousu
           and j21_matric = :matric
        union
        select j152_valor as j21_valor
          from iptutaxacalv
               inner join iptutaxanump on j151_codigo = j152_iptutaxanump
               inner join iptucadtaxaexe on j08_iptucadtaxaexe = j151_iptucadtaxaexe
         where j08_anousu = :anousu
           and j151_matric = :matric
       ) calv
 where /* dbwhere dinamico, se informado */
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- O metodo serve para olhar valores de taxas num conjunto unificado, mas perde varias dimensoes do item original.
- Como o `union` retorna basicamente `j21_valor`, ele nao preserva receita, historico nem origem detalhada do valor.

### Regras de manutencao observadas

1. `incluir()` exige `j21_anousu`, `j21_matric`, `j21_receit`, `j21_valor`, `j21_quant` e `j21_codhis`.
2. A classe nao usa sequence; os identificadores sao informados externamente.
3. `alterar()` e `excluir()` dependem de `dbwhere` ou de um filtro externo, porque os metodos basicos nao montam chave composta automaticamente.
4. Diferente de outras classes legadas, aqui nao aparece bloco de auditoria `db_acount*` em inclusao, alteracao ou exclusao.

### Relacionamentos de negocio confirmados no catalogo

- `iptucalv.j21_codhis -> iptucalh.j17_codhis`
- `iptucalv.j21_matric -> iptubase.j01_matric`
- `iptucalv.j21_receit -> caixa.tabrec.k02_codigo`
- Pela cadeia de `iptubase`, o calculo alcanca `lote`, `cgm`, `iptucalc`, `iptuconstr` e outras dimensoes cadastrais.
- Pela cadeia de `iptucalh`, o item se conecta a configuracoes como `iptucalhconf`, `cfiptu` e `iptucadtaxaexe`.

### Que perguntas ela responde bem

- Qual foi o valor calculado de IPTU em determinado exercicio?
- Qual foi o valor calculado de taxa de lixo em determinado exercicio?
- Qual foi o total calculado por matricula?
- Qual foi o total calculado por receita?
- Qual foi o total calculado por historico?

### Cuidados para consultas do agente

- Nao conte linhas de `iptucalv` como quantidade de imoveis; linhas aqui contam itens de valor por receita/historico.
- `j21_valor` e valor calculado do item, nao prova de pagamento nem de arrecadacao.
- Para somar IPTU corretamente, filtre as receitas que representam IPTU; sem isso a soma mistura taxas e outros componentes.
- Para comparar exercicios, compare por `j21_matric` e, quando necessario, tambem por `j21_receit` e `j21_codhis`.
- `j21_quant` pode mudar de significado conforme a receita ou historico; nao use esse campo como metrica universal sem validar o contexto.
- Para explicar por que o valor mudou, combine `iptucalv` com `iptucalc` e, se preciso, com `iptucale`.
- Para responder sobre pagamento, cancelamento, compensacao ou saldo, prefira os metodos analiticos da classe ou cruze com arrecadacao explicitamente.
