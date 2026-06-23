## cadastro.iptucale

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptucale_classe.php`

Registro do valor venal calculado para cada construcao de uma matricula em determinado exercicio. A classe guarda a area edificada considerada no calculo, o valor do metro quadrado, a pontuacao processada e o valor venal resultante por edificacao.

### Estrutura e interpretacao

- **Classe:** `cl_iptucale`
- **Tabela principal:** `iptucale`
- **Chave primaria:** `j22_anousu`, `j22_matric`, `j22_idcons`
- **Grau basico:** uma linha por exercicio, matricula e construcao calculada

Campos de negocio confirmados:

- `j22_anousu`: exercicio do calculo
- `j22_matric`: matricula do imovel
- `j22_idcons`: identificador da construcao dentro da matricula
- `j22_areaed`: area construida usada no calculo
- `j22_vm2`: valor do metro quadrado adotado no calculo da construcao
- `j22_pontos`: pontuacao processada da construcao
- `j22_valor`: valor venal calculado para a edificacao

Interpretacao segura:

- A tabela detalha o calculo da parte edificada; nao representa o calculo consolidado do imovel inteiro.
- Uma mesma matricula pode gerar varias linhas no mesmo exercicio, uma para cada construcao.
- Para valor venal edificado total do imovel, some `j22_valor` por `j22_anousu` e `j22_matric`.

### Consulta: `sql_query`

- **Objetivo:** recuperar o calculo da construcao com enriquecimento do cadastro fisico da construcao, logradouro e base do imovel.
- **Tabelas:** `iptucale`, `iptuconstr`, `ruas`, `iptubase`

```sql
select /* campos dinamicos */
  from iptucale
       inner join iptuconstr
          on iptuconstr.j39_matric = iptucale.j22_matric
         and iptuconstr.j39_idcons = iptucale.j22_idcons
       inner join ruas
          on ruas.j14_codigo = iptuconstr.j39_codigo
       inner join iptubase
          on iptubase.j01_matric = iptuconstr.j39_matric
       inner join ruas as a
          on a.j14_codigo = iptuconstr.j39_codigo
       inner join iptubase as b
          on b.j01_matric = iptuconstr.j39_matric
 where iptucale.j22_anousu = :anousu
   and iptucale.j22_matric = :matric
   and iptucale.j22_idcons = :idcons
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- O join funcional e o primeiro com `iptuconstr` por matricula e construcao; ele amarra o calculo ao cadastro da edificacao.
- Os joins repetidos com `ruas as a` e `iptubase as b` nao mudam o grao do resultado, mas ampliam o risco de confusao quando se usa `*`.
- Esta consulta continua no grao da construcao calculada, desde que os filtros respeitem a chave completa.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `iptucale`.

```sql
select /* campos dinamicos */
  from iptucale
 where iptucale.j22_anousu = :anousu
   and iptucale.j22_matric = :matric
   and iptucale.j22_idcons = :idcons
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar existencia do calculo da construcao;
- inspecionar somente os campos gravados na tabela;
- evitar efeitos colaterais dos joins duplicados de `sql_query`.

### Regras de manutencao observadas

1. `incluir()` exige `j22_areaed`, `j22_vm2`, `j22_pontos` e `j22_valor`.
2. A chave primaria e informada externamente; a classe nao usa sequence.
3. `j22_anousu`, `j22_matric` e `j22_idcons` sao obrigatorios para inclusao e exclusao.
4. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.
5. `alterar()` e `excluir()` operam pela chave completa ou por `dbwhere` informado externamente.

### Relacionamentos de negocio confirmados no catalogo

- A intencao do catalogo e ligar `iptucale` a `iptuconstr` pela combinacao de matricula e construcao.
- Pela propria classe, o join confiavel e `iptucale.j22_matric = iptuconstr.j39_matric` e `iptucale.j22_idcons = iptuconstr.j39_idcons`.
- Pela cadeia de `iptuconstr`, o calculo alcanca `ruas` e `iptubase`.
- A partir desses caminhos, a construcao calculada pode ser enriquecida com contexto territorial e cadastral do imovel.

Ambiguidade relevante:

- O bloco de relacionamento em `catalog/cadastro_extraido.json` para `cadastro.iptucale` esta inconsistente, repetindo colunas e montando joins compostos incorretos.
- Para esta entidade, prefira os joins observados na classe PHP e trate o catalogo apenas como indicativo de vizinhanca semantica.

### Cuidados para consultas do agente

- Nao conte linhas de `iptucale` como quantidade de imoveis; linhas aqui contam construcoes calculadas.
- Para contar imoveis com edificacao calculada em um exercicio, use `COUNT(DISTINCT j22_matric)`.
- `j22_valor` e valor venal da edificacao, nao o valor final do IPTU lancado.
- `j22_areaed` pode divergir da area atual do cadastro fisico, porque representa a area usada no calculo daquele exercicio.
- Para explicar variacao entre anos, compare a mesma chave `j22_matric + j22_idcons` em exercicios diferentes.
- Para consolidado do imovel, combine com `iptucalc`; para valor final por receita ou imposto, combine com `iptucalv` ou tabelas equivalentes.
