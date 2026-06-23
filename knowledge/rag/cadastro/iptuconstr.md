## cadastro.iptuconstr

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptuconstr_classe.php`

Cadastro das construcoes vinculadas a uma matricula imobiliaria. A classe trata a construcao como entidade cadastral central do imovel edificado, com area, endereco de frente, datas de inclusao e demolicao, origem, pavimento e indicacao de construcao principal.

### Estrutura e interpretacao

- **Classe:** `cl_iptuconstr`
- **Tabela principal:** `iptuconstr`
- **Chave primaria:** `j39_matric`, `j39_idcons`
- **Grau basico:** uma linha por construcao vinculada a uma matricula

Campos de negocio confirmados:

- `j39_matric`: matricula do imovel
- `j39_idcons`: identificador da construcao dentro da matricula
- `j39_ano`: ano da construcao
- `j39_area`: area total da construcao em m2
- `j39_areap`: area privada da construcao
- `j39_dtlan`: data de inclusao da construcao no cadastro
- `j39_codigo`: logradouro para o qual a construcao faz frente
- `j39_numero`: numero do endereco
- `j39_compl`: complemento do endereco
- `j39_dtdemo`: data de demolicao
- `j39_codprotdemo`: processo de protocolo ligado a demolicao
- `j39_idaument`: origem da construcao
- `j39_idprinc`: indicador de construcao principal
- `j39_pavim`: pavimento
- `j39_obs`: observacoes livres

Campos relevantes vistos no catalogo, mas nao tratados neste trecho da classe:

- `j39_habite`
- `j39_areajirau`
- `j39_areajiraudeposito`
- `j39_areamezanino`

Interpretacao segura:

- A tabela representa o cadastro fisico da edificacao, nao o calculo tributario do exercicio.
- Uma mesma matricula pode possuir varias construcoes.
- `j39_dtdemo` distingue construcao ativa de historico de construcao demolida.

### Consulta: `sql_query`

- **Objetivo:** recuperar a construcao com enriquecimento do imovel, lote, contribuinte e logradouro.
- **Tabelas:** `iptuconstr`, `ruas`, `iptubase`, `lote`, `cgm`, `ruastipo`

```sql
select /* campos dinamicos */
  from iptuconstr
       inner join ruas
          on ruas.j14_codigo = iptuconstr.j39_codigo
       inner join iptubase
          on iptubase.j01_matric = iptuconstr.j39_matric
       inner join lote
          on lote.j34_idbql = iptubase.j01_idbql
       inner join cgm
          on cgm.z01_numcgm = iptubase.j01_numcgm
       left join ruastipo
          on ruastipo.j88_codigo = ruas.j14_tipo
 where iptuconstr.j39_matric = :matric
   and iptuconstr.j39_idcons = :idcons
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Esta e a consulta base para responder "que construcao e essa" com contexto cadastral do imovel.
- O resultado continua no grao de uma construcao por matricula.
- Como existe `left join` para `ruastipo`, a ausencia de tipo de rua nao elimina a linha.

### Consulta: `sql_query_file`

- **Objetivo:** ler apenas a tabela fisica `iptuconstr`.

```sql
select /* campos dinamicos */
  from iptuconstr
 where iptuconstr.j39_matric = :matric
   and iptuconstr.j39_idcons = :idcons
 order by /* ordenacao dinamica */
```

Uso seguro:

- validar persistencia do cadastro da construcao;
- comparar valores fisicos sem enriquecimento;
- servir de base para auditoria de inclusao, alteracao e exclusao.

### Consulta: `sql_query_proprietario_nome`

- **Objetivo:** recuperar a construcao com caracteristicas e proprietario nominal.
- **Tabelas:** `iptuconstr`, `carconstr`, `proprietario_nome`, `caracter`, `cargrup`

```sql
select /* campos dinamicos */
  from iptuconstr
       inner join carconstr
          on j39_matric = j48_matric
         and j39_idcons = j48_idcons
       inner join proprietario_nome
          on j48_matric = j01_matric
       inner join caracter
          on j48_caract = j31_codigo
       inner join cargrup
          on j31_grupo = j32_grupo
 where iptuconstr.j39_matric = :matric
   and iptuconstr.j39_idcons = :idcons
 order by /* ordenacao dinamica */
```

Interpretacao segura:

- Use quando a pergunta depender do proprietario nominal ou das caracteristicas da construcao.
- O join com `proprietario_nome` ocorre pela matricula, entao o grao pode se multiplicar conforme caracteristicas e proprietarios associados.

### Consulta utilitaria: `sql_query_update_area`

- **Objetivo:** montar o `update` de area da construcao.

```sql
update iptuconstr
   set j39_area = :area
 where j39_matric = :matric
   and j39_idcons = :idcons
```

Uso seguro:

- rotina operacional de ajuste de area;
- nao e consulta analitica para RAG, mas explicita que `j39_area` e campo central de manutencao.

### Regras de manutencao observadas

1. `incluir()` exige `j39_area`, `j39_dtlan`, `j39_codigo`, `j39_numero`, `j39_idprinc` e `j39_pavim`.
2. `j39_areap` cai para `0` quando nao informado.
3. `j39_dtdemo` vira `null` quando nao informado.
4. `j39_idaument` cai para `0` quando nao informado.
5. A obrigatoriedade de `j39_ano` depende do parametro `cadastro.cfiptu.j18_validarano` do exercicio da sessao.
6. Inclusao, alteracao e exclusao registram auditoria em `db_acount*`.

### Exclusao em cascata observada

O metodo `excluirGeral()` tenta remover, antes da propria construcao:

- `iptucaleold`
- `carconstr`
- `constrcar`
- `iptucale`
- `constrescr`
- `issmatric`
- `iptuconstrdemo`
- `iptuconstrpontos`

Interpretacao segura:

- `iptuconstr` funciona como entidade-mestre de varias tabelas derivadas da construcao.
- Para entender impacto de remover ou alterar uma construcao, vale sempre olhar essas tabelas satelites.

### Relacionamentos de negocio confirmados no catalogo

- `iptuconstr.j39_codigo -> ruas.j14_codigo`
- `iptuconstr.j39_matric -> iptubase.j01_matric`
- Pela cadeia de `iptubase`, a construcao alcanca `lote`, `cgm` e o restante do cadastro do imovel.
- Pela cadeia de `ruas`, a construcao alcanca `ruastipo`, `ruasbairro`, `ruascep`, `ruashistorico`, `testada`, `testpri`, `lotenumero` e `logradcep`.
- Pela chave composta de construcao, a entidade se conecta semanticamente a `iptucale`, `iptuconstrdemo`, `iptuconstrhabite`, `iptuconstrpontos`, `iptucalcpadraoconstr` e correlatas.

Ambiguidade relevante:

- O catalogo monta varios joins compostos quebrados para a chave `j39_matric + j39_idcons`, repetindo colunas de forma incorreta.
- Para relacoes de construcao com tabelas como `iptucale` e `iptuconstrpontos`, prefira o padrao semantico visto na aplicacao: `matric -> matric` e `idcons -> idcons`.

### Que perguntas ela responde bem

- Quais construcoes existem para uma matricula?
- Qual e a construcao principal do imovel?
- Qual e a area cadastrada de cada construcao?
- Quais construcoes estao ativas e quais foram demolidas?
- Em qual logradouro e numero a construcao esta cadastrada?
- Que construcoes de uma matricula impactam o calculo do IPTU?

### Cuidados para consultas do agente

- Nao conte linhas de `iptuconstr` como quantidade de imoveis; linhas aqui contam construcoes.
- Para contar imoveis edificados, use `COUNT(DISTINCT j39_matric)`.
- Para analise corrente, normalmente filtre `j39_dtdemo IS NULL`.
- `j39_dtlan` e data de inclusao no cadastro, nao necessariamente a data real da construcao.
- `j39_ano` pode ser obrigatorio ou nao conforme configuracao de `cfiptu`; nao presuma completude historica.
- `j39_idprinc` ajuda a destacar a construcao principal, mas nao elimina a relevancia das demais para calculo ou cadastro.
- Para impacto tributario, combine `iptuconstr` com `iptucale`, `iptucalc` e `iptucalv`.
- Para perguntas sobre endereco consolidado do imovel, valide se a frente da construcao e o mesmo endereco dominante da matricula.
