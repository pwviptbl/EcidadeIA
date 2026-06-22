# Instituições e parâmetros municipais

> Fonte principal: `/var/www/html/e-cidade-php74/classes/db_db_config_classe.php`
>
> Classe: `cl_db_config`
>
> Tabela principal: `db_config`

## Visão geral

`db_config` armazena a identificação e os parâmetros de cada instituição configurada no e-Cidade. A chave é `codigo`.

Uma linha representa uma instituição, como prefeitura, câmara, entidade previdenciária ou outro órgão configurado. A descrição exata do tipo deve ser obtida em `db_tipoinstit`; não deve ser inferida apenas pelo código.

Campos relevantes:

| Campo | Significado definido pela classe |
|---|---|
| `codigo` | Código da instituição |
| `nomeinst` | Nome da instituição |
| `nomeinstabrev` | Nome abreviado para relatórios |
| `numcgm` | CGM vinculado à instituição |
| `db21_tipoinstit` | Código do tipo de instituição |
| `db21_ativo` | Indicador cadastral denominado “Ativo” |
| `prefeitura` | Indicador de prefeitura |
| `cgc` | CNPJ/CGC da instituição |
| `munic`, `uf`, `cep` | Município, UF e CEP |
| `ender`, `numero`, `bairro`, `db21_compl` | Endereço institucional |
| `dtcont` | Data da contabilidade |
| `db21_criacao` | Data de criação da instituição |
| `db21_datalimite` | Data limite de validade da instituição |
| `db21_regracgmiss` | Regra de CGM para ISS |
| `db21_regracgmiptu` | Regra de CGM para IPTU |
| `db21_usasisagua` | Indica uso do sistema de água |
| `db21_codigomunicipoestado` | Código estadual do município |
| `db21_codtj` | Código do município no Tribunal de Justiça |
| `db21_codsiconfi` | Código SICONFI |
| `db21_possui_rpps` | Indica existência de RPPS |
| `db21_unidade_gestora_rpps` | Indica unidade gestora do RPPS |

Cuidados:

- A classe não define o domínio dos valores de `db21_ativo`; não interprete números específicos como ativo ou inativo sem consultar a regra consumidora.
- `db21_tipoinstit` é uma chave para `db_tipoinstit`, não uma descrição.
- CNPJ, endereço, telefone e e-mail são dados institucionais que ainda podem exigir controle de exposição.

## Consulta completa da instituição

### Consulta: `sql_query`

- **Objetivo:** Recuperar a instituição, seu CGM e a descrição de seu tipo.
- **Grão do resultado:** Uma linha por instituição, se os relacionamentos forem únicos.
- **Junções:**
  - `cgm.z01_numcgm = db_config.numcgm`
  - `db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit`

```sql
select /* campos dinâmicos */
  from db_config
       inner join cgm
          on cgm.z01_numcgm = db_config.numcgm
       inner join db_tipoinstit
          on db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit
 where db_config.codigo = :codigo
 order by /* ordenação dinâmica */
```

Regras:

- Os dois relacionamentos são obrigatórios devido ao `inner join`.
- Uma instituição sem CGM ou sem tipo correspondente não aparece nessa consulta.
- Quando `$dbwhere` é informado, ele substitui o filtro pelo código.

### Consulta: `sql_query_file`

Consulta somente `db_config`, sem exigir CGM ou tipo:

```sql
select /* campos dinâmicos */
  from db_config
 where db_config.codigo = :codigo
 order by /* ordenação dinâmica */
```

É a opção adequada para recuperar parâmetros diretamente da instituição.

## Parâmetros da instituição corrente

### Consulta: `getParametrosInstituicao`

```sql
select *
  from db_config
 where codigo = :instituicao
```

Regras:

- Quando o código não é informado, o método usa `DB_instit` da sessão.
- Retorna o primeiro registro como objeto ou `false` quando não encontra a instituição.
- O método é utilizado por relatórios e rotinas que precisam de nome, logo e regras tributárias da instituição.
- A consulta pressupõe que `codigo` identifica uma única instituição.

Para consultas do agente, informe explicitamente a instituição sempre que o contexto não garantir qual sessão está sendo usada.

## Instituições permitidas ao usuário

### Consulta: `sql_query_usu`

- **Objetivo:** Listar instituições relacionadas a um usuário.
- **Grão do resultado:** Uma linha por vínculo entre usuário e instituição.
- **Junção:** `db_userinst.id_instit = db_config.codigo`.

```sql
select /* campos dinâmicos */
  from db_config
       inner join db_userinst
          on db_userinst.id_instit = db_config.codigo
 where db_userinst.id_usuario = :usuario
 order by /* ordenação dinâmica */
```

Regras:

- O método não filtra o usuário automaticamente; o consumidor deve informar a condição sobre `db_userinst.id_usuario`.
- É usado em seletores de instituição acessíveis ao usuário.
- Para contar instituições, prefira `count(distinct db_config.codigo)` caso existam vínculos duplicados.
- Não use apenas a existência em `db_config` para concluir que um usuário possui acesso à instituição.

## Tipo de instituição

### Consulta: `sql_query_tipoinstit`

Sem condição livre, a intenção do método é relacionar:

```sql
select /* campos dinâmicos */
  from db_config
       inner join db_tipoinstit
          on db_tipoinstit.db21_codtipo = db_config.db21_tipoinstit
 where db_config.codigo = :codigo
```

Comportamento legado importante:

- O join fica armazenado na mesma variável que recebe o filtro.
- Quando `$dbwhere` é informado, o código substitui essa variável por `where <condição>`.
- Nesse caminho, o SQL final não contém `db_tipoinstit`.
- Filtros e campos somente de `db_config` continuam funcionando, mas campos de `db_tipoinstit` tornam a consulta inválida.

Há consumidores que usam `db21_tipoinstit in (5,6)` para selecionar instituições de RPPS. Isso comprova o uso conjunto dos códigos `5` e `6` nesse contexto, mas não define individualmente a descrição de cada código.

## Código SIAFI do município

### Consulta: `sql_query_siafi`

- **Objetivo:** Obter dados do município SIAFI relacionado à instituição.
- **Junção:** `municipiosiafi.q110_cnpj = db_config.cgc`.

```sql
select /* campos dinâmicos */
  from db_config
       inner join municipiosiafi
          on municipiosiafi.q110_cnpj = db_config.cgc
 where db_config.codigo = :codigo
```

Regra confirmada:

- A associação é realizada pelo CNPJ da instituição, não pelo nome ou código do município.
- A geração de arquivo MEI usa essa consulta para obter `municipiosiafi.q110_codigo`.

Comportamento legado:

- Assim como em `sql_query_tipoinstit`, fornecer `$dbwhere` remove o join com `municipiosiafi`.
- Use o filtro por `codigo` ou reconstrua a consulta explicitamente quando precisar de condição adicional.

## Código TOM do município

### Consulta: `getCodigoTom`

- **Objetivo:** Obter o código municipal do sistema externo utilizado pela rotina.
- **Grão do resultado:** Um código de sistema para a instituição.

```sql
select cadendermunicipiosistema.db125_codigosistema
  from db_config
       inner join cadenderestado
          on trim(cadenderestado.db71_sigla) = db_config.uf
       inner join cadendermunicipio
          on cadendermunicipio.db72_cadenderestado =
             cadenderestado.db71_sequencial
         and trim(cadendermunicipio.db72_descricao) = db_config.munic
       inner join cadendermunicipiosistema
          on cadendermunicipiosistema.db125_cadendermunicipio =
             cadendermunicipio.db72_sequencial
         and cadendermunicipiosistema.db125_db_sistemaexterno = 5
 where db_config.codigo = :instituicao
```

Regras:

- Quando a instituição não é informada, usa `DB_instit` da sessão.
- A UF é comparada com `trim(db71_sigla)`.
- O município é comparado por texto com `trim(db72_descricao) = munic`.
- O sistema externo é fixado em `5`.
- O método é consumido pela geração de arquivo do Simples Nacional e trata o resultado como código TOM.
- Retorna `null` quando não encontra correspondência.

Cuidados:

- A comparação do município é textual e não remove acentos nem normaliza caixa.
- Divergências de grafia ou espaços em `db_config.munic` podem impedir a localização.
- A classe não demonstra que o sistema externo `5` representa TOM em todos os contextos; essa interpretação é confirmada pelo consumidor do método.

## Logradouro relacionado ao município

### Consulta: `sql_query_log`

A intenção do método é relacionar o município textual da instituição ao cadastro de localidades e logradouros:

```sql
select /* campos dinâmicos */
  from db_config
       inner join ceplocalidades
          on ceplocalidades.cp05_localidades = db_config.munic
       inner join ceplogradouros
          on ceplogradouros.cp06_codlocalidade =
             ceplocalidades.cp05_codlocalidades
 where db_config.codigo = :codigo
```

O método é usado na pesquisa de logradouros da manutenção de `db_config`.

Defeito de montagem:

- Quando `$dbwhere` é informado, ele substitui a variável que continha os joins.
- A tela consumidora informa filtros como `cp06_codlogradouro = ...` e `cp06_logradouro like ...`.
- Nesse caminho, o SQL passa a referenciar campos de `ceplogradouros` sem incluir a tabela, tornando a consulta inconsistente.

Não reutilize esse método como receita válida com `$dbwhere`. Para pesquisar logradouro, mantenha explicitamente os dois joins e adicione o filtro depois deles.

## Recomendações para consultas do agente

- Identifique a instituição por `db_config.codigo`.
- Use `DB_instit` apenas quando a pergunta estiver explicitamente no contexto da sessão atual.
- Para nome e classificação do tipo, relacione `db_tipoinstit` por `db21_codtipo`.
- Para permissões, relacione `db_userinst` e filtre `id_usuario`; não considere todas as instituições visíveis ao usuário.
- Para SIAFI, a relação confirmada é pelo CNPJ.
- Para TOM, aplique a cadeia de endereço e o sistema externo `5`.
- Não presuma que `db21_ativo`, `db21_tipoinstit` ou as regras de CGM possuem domínio universal sem consultar seus cadastros e consumidores.
- Em consultas novas, não concatene `$dbwhere`, campos ou ordenação recebidos do usuário. Use allowlist de colunas e parâmetros vinculados.
