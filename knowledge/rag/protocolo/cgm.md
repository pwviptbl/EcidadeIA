# CGM - Cadastro Geral do Município

> Fonte principal: `/var/www/html/e-cidade-php74/classes/db_cgm_classe.php`
>
> Classe: `cl_cgm`
>
> Tabela principal: `protocolo.cgm`

## Visão geral

O CGM é o cadastro central de pessoas físicas e jurídicas utilizado por vários módulos do e-Cidade. A chave da entidade é `z01_numcgm`.

Cada registro representa uma pessoa ou entidade cadastrada no município. O nome e o documento não devem ser tratados como chaves únicas sem validação, pois podem existir homônimos, documentos sem formatação uniforme ou registros duplicados.

Campos relevantes:

| Campo | Significado |
|---|---|
| `z01_numcgm` | Código único do CGM |
| `z01_nome` | Nome ou razão social |
| `z01_nomefanta` | Nome fantasia |
| `z01_nomecomple` | Nome completo |
| `z01_cgccpf` | CPF ou CNPJ armazenado no cadastro principal |
| `z01_cadast` | Data de cadastramento |
| `z01_ultalt` | Data da última alteração |
| `z01_dtnasc` | Data de nascimento |
| `z01_dtfalecimento` | Data de falecimento |
| `z01_ender`, `z01_numero`, `z01_compl` | Endereço textual do cadastro principal |
| `z01_bairro`, `z01_munic`, `z01_uf`, `z01_cep` | Localização textual do cadastro principal |
| `z01_endcon`, `z01_numcon`, `z01_comcon` | Endereço de contato/comercial |
| `z01_baicon`, `z01_muncon`, `z01_ufcon`, `z01_cepcon` | Localização de contato/comercial |

Não foi identificada na classe uma regra genérica de “CGM ativo”. `z01_dtfalecimento` é uma informação específica de pessoa física e não equivale, isoladamente, a um status cadastral geral.

## Consulta cadastral básica

### Método `sql_query`

Retorna os dados do CGM e, quando existente, sua extensão de pessoa física.

```sql
select <campos>
  from cgm
       left join cgmfisico
         on cgmfisico.z04_numcgm = cgm.z01_numcgm
 where cgm.z01_numcgm = <codigo_cgm>
```

Regras:

- O `left join` preserva pessoas jurídicas e CGMs que não tenham registro em `cgmfisico`.
- Sem o código do CGM, o método aceita uma condição livre recebida pelo parâmetro `$sWhere`.
- A granularidade esperada é um registro por CGM, desde que `cgmfisico` tenha no máximo um registro por `z04_numcgm`.

### Método `sql_query_file`

Consulta somente a tabela `cgm`, sem extensões cadastrais.

```sql
select <campos>
  from cgm
 where z01_numcgm = <codigo_cgm>
```

É a consulta mais direta quando os dados necessários estão integralmente no cadastro principal.

## Identificação por CPF e CNPJ

### Método `sql_query_cpf`

Retorna somente CGMs vinculados à tabela de CPF.

```sql
select <campos>
  from cgm
       inner join db_cgmcpf
          on db_cgmcpf.z01_numcgm = cgm.z01_numcgm
       left join cgmfisico
         on cgmfisico.z04_numcgm = cgm.z01_numcgm
 where cgm.z01_numcgm = <codigo_cgm>
```

### Método `sql_query_cgc`

Retorna somente CGMs vinculados à tabela de CNPJ/CGC.

```sql
select <campos>
  from cgm
       inner join db_cgmcgc
          on db_cgmcgc.z01_numcgm = cgm.z01_numcgm
 where cgm.z01_numcgm = <codigo_cgm>
```

Regras de uso:

- `db_cgmcpf` é usada pela classe como marcador de CGM com CPF.
- `db_cgmcgc` é usada pela classe como marcador de CGM com CNPJ/CGC.
- O campo comum `z01_cgccpf` pode conter CPF ou CNPJ. Antes de comparar documentos, normalize pontuação e confirme o tipo de pessoa.
- CPF, CNPJ, identidade, endereço, telefone e e-mail são dados pessoais. Consultas e respostas do agente devem retornar apenas os campos necessários.

## Pesquisa por nome

### Método `sqlnome`

Pesquisa CGMs cujo nome começa pelo texto informado.

```sql
select <campos>
  from cgm
       left join cgmfisico
         on cgmfisico.z04_numcgm = cgm.z01_numcgm
 where to_ascii(upper(z01_nome)) like to_ascii(upper('<nome>%'))
 order by to_ascii(z01_nome)
```

O SQL real converte o parâmetro para maiúsculas no PHP antes de montar a condição.

Filtros adicionais do método:

| Valor de `$filtro` | Regra |
|---|---|
| `1` | Usa `inner join db_cgmcpf`, restringindo a CGMs com CPF |
| `2` | Usa `inner join db_cgmcgc`, restringindo a CGMs com CNPJ/CGC |
| Outro | Não restringe pelo tipo de documento |

Cuidados:

- A pesquisa é por prefixo, não por trecho em qualquer posição.
- `to_ascii` reduz diferenças de acentuação, e `upper` reduz diferenças de caixa.
- Nome não identifica uma pessoa de forma única. Sempre confirme pelo código do CGM e, quando autorizado, pelo documento.
- O método legado concatena o valor diretamente no SQL. Em novas consultas, use parâmetros vinculados.

### Método `sqlCodnome`

Lista código e nome dos CGMs, podendo restringir pelo código:

```sql
select <campos>
  from cgm
 where z01_numcgm = <codigo_cgm>
 order by z01_nome
```

## Endereços do CGM

A classe expõe três modelos distintos de consulta de endereço. Eles não devem ser misturados sem considerar a origem dos dados.

### Endereço textual do cadastro principal

Os campos `z01_ender`, `z01_numero`, `z01_compl`, `z01_bairro`, `z01_munic`, `z01_uf` e `z01_cep` ficam diretamente em `cgm`.

Existe ainda um conjunto de contato/comercial nos campos `z01_endcon`, `z01_numcon`, `z01_comcon`, `z01_baicon`, `z01_muncon`, `z01_ufcon` e `z01_cepcon`.

### Método `sql_query_ender`: vínculos legados de rua e bairro

```sql
select <campos>
  from cgm
       left join db_cgmbairro
         on db_cgmbairro.z01_numcgm = cgm.z01_numcgm
       left join bairro
         on bairro.j13_codi = db_cgmbairro.j13_codi
       left join db_cgmruas
         on db_cgmruas.z01_numcgm = cgm.z01_numcgm
       left join ruas
         on ruas.j14_codigo = db_cgmruas.j14_codigo
 where cgm.z01_numcgm = <codigo_cgm>
```

Regras:

- Os `left joins` preservam o CGM mesmo sem rua ou bairro vinculados.
- Havendo mais de um vínculo em `db_cgmbairro` ou `db_cgmruas`, a consulta pode multiplicar linhas.
- Este modelo é diferente da cadeia normalizada baseada em `cgmendereco`.

### Método `sql_query_endereco`: endereços normalizados

```sql
select <campos>
  from cgm
       left join cgmendereco
         on cgmendereco.z07_numcgm = cgm.z01_numcgm
       left join endereco
         on endereco.db76_sequencial = cgmendereco.z07_endereco
       left join cadenderlocal
         on cadenderlocal.db75_sequencial = endereco.db76_cadenderlocal
       left join cadenderbairrocadenderrua
         on cadenderbairrocadenderrua.db87_sequencial =
            cadenderlocal.db75_cadenderbairrocadenderrua
       left join cadenderrua
         on cadenderrua.db74_sequencial =
            cadenderbairrocadenderrua.db87_cadenderrua
       left join cadenderbairro
         on cadenderbairro.db73_sequencial =
            cadenderbairrocadenderrua.db87_cadenderbairro
 where cgm.z01_numcgm = <codigo_cgm>
```

Granularidade:

- Um CGM pode possuir vários registros em `cgmendereco`.
- A consulta pode retornar mais de uma linha por CGM.
- Para contagem de pessoas, conte `distinct cgm.z01_numcgm`, não as linhas resultantes dos endereços.

### Método `sql_query_endereco_licitacon`: endereço principal para LicitaCon

O método escolhe um único endereço principal do CGM:

```sql
left join cgmendereco
  on cgmendereco.z07_sequencial = (
       select z07_sequencial
         from cgmendereco
        where z07_numcgm = cgm.z01_numcgm
          and z07_tipo = 'P'
        order by z07_sequencial
        limit 1
     )
```

Depois, percorre `endereco`, `cadenderlocal`, `cadenderrua`, `cadenderbairro`, `cadendermunicipio` e `cadendermunicipiosistema`.

Regra específica:

```sql
cadendermunicipiosistema.db125_db_sistemaexterno = 4
```

Interpretação:

- Somente endereços com tipo `P` são candidatos.
- Se houver mais de um principal, vence o menor `z07_sequencial`, não necessariamente o endereço alterado mais recentemente.
- O código `4` identifica o sistema externo exigido por essa integração conforme o SQL da classe.
- Os relacionamentos são `left join`, portanto o CGM continua aparecendo mesmo sem endereço principal ou mapeamento externo.

## Relações com outros módulos

### Método `sql_query_ordemcompra`

Retorna CGMs vinculados a ordens de compra de materiais.

```sql
select <campos>
  from cgm
       left join db_cgmbairro
         on db_cgmbairro.z01_numcgm = cgm.z01_numcgm
       left join db_cgmcgc
         on db_cgmcgc.z01_numcgm = cgm.z01_numcgm
       left join db_cgmcpf
         on db_cgmcpf.z01_numcgm = cgm.z01_numcgm
       left join db_cgmruas
         on db_cgmruas.z01_numcgm = cgm.z01_numcgm
       inner join matordem
          on matordem.m51_numcgm = cgm.z01_numcgm
 where cgm.z01_numcgm = <codigo_cgm>
```

O `inner join matordem` restringe o resultado a CGMs que possuem vínculo com ordem de compra. Os vínculos de CPF, CNPJ, rua e bairro são opcionais.

### Método `sql_query_veic`

Relaciona o CGM com pessoal e motoristas:

```sql
select <campos>
  from cgm
       left join rhpessoal
         on rhpessoal.rh01_numcgm = cgm.z01_numcgm
       left join veicmotoristas
         on veicmotoristas.ve05_numcgm = cgm.z01_numcgm
```

Como ambos são `left join`, a consulta não retorna exclusivamente motoristas. Para exigir motorista cadastrado, é necessário filtrar um campo não nulo de `veicmotoristas`, como `ve05_numcgm is not null`.

O método também aceita joins adicionais por texto, o que exige cuidado com duplicação de linhas e segurança da montagem do SQL.

### Método `sql_matricula`

Retorna CGMs que possuem vínculo com o cadastro de pessoal:

```sql
select <campos>
  from cgm
       inner join rhpessoal
          on rhpessoal.rh01_numcgm = cgm.z01_numcgm
 where cgm.z01_numcgm = <codigo_cgm>
```

Apesar do nome `sql_matricula`, a regra principal é a existência de registro em `rhpessoal`. Uma pessoa pode possuir mais de um vínculo funcional, portanto a consulta pode retornar múltiplas linhas para o mesmo CGM.

## CGMs do município da instituição

### Método `sql_query_cgmmunicipio`

Seleciona CGMs cujo município textual corresponde ao município configurado para a instituição corrente:

```sql
select <campos>
  from cgm
       inner join db_config
          on upper(trim(fc_remove_acentos(cgm.z01_munic))) =
             upper(trim(fc_remove_acentos(db_config.munic)))
         and db_config.codigo = <instituicao_corrente>
```

Regras e limitações:

- A instituição é obtida da sessão pelo código `DB_instit`.
- A correspondência é feita pelo texto do município, ignorando caixa, espaços laterais e acentos.
- Não há comparação por código oficial de município.
- Variações de grafia, abreviações ou município vazio podem causar falsos negativos.

## Consulta por tipo de CGM

### Método `sql_query_cgmtipo`

Para pessoa física, a classe monta:

```sql
from cgm
inner join cgmfisico
        on cgm.z01_numcgm = cgmfisico.z04_numcgm
```

Os filtros por nome usam pesquisa por prefixo:

```sql
to_ascii(upper(z01_nome)) ilike to_ascii(upper('<nome>%'))
```

Defeito identificado no código legado:

- Para o tipo jurídico, o método inclui `cgmjuridico`, mas a condição referencia `cgmfisico.z08_numcgm`.
- Para a opção que combina físico e jurídico, o join de `cgmjuridico` também referencia `cgmfisico.z08_numcgm`.
- Nesses dois caminhos, o SQL gerado possui referência de alias/tabela incoerente e não deve ser reutilizado como modelo válido.

A intenção aparente é relacionar `cgm.z01_numcgm` com o campo correspondente de `cgmjuridico`, mas isso deve ser confirmado no esquema antes de corrigir ou produzir uma consulta nova.

Outro cuidado: filtros diferentes de nome são concatenados como `campo = valor`. Valores textuais precisam de tratamento e todas as consultas novas devem usar parâmetros vinculados.

## Campos completos para cadastro do CGM

### Método `sqlQueryCamposCadastroCgm`

Consulta campos escolhidos pelo chamador combinando:

```text
cgm
  -> cgmtipoempresa
  -> cgmjuridico
  -> cgmendereco
  -> endereco
  -> cadenderlocal
  -> cadenderbairrocadenderrua
  -> cadenderrua
  -> cadenderbairro
```

Todos os relacionamentos adicionais são opcionais por `left join`.

Regras:

- O filtro principal é `cgm.z01_numcgm = <codigo_cgm>`.
- A lista de campos é definida dinamicamente pelo chamador.
- A presença de vários endereços pode produzir várias linhas para o mesmo CGM.
- Não use a quantidade de linhas dessa consulta como quantidade de pessoas.

## Recomendações para consultas do agente

- Use `z01_numcgm` como identificador principal do CGM.
- Para busca nominal, aplique normalização de caixa e acentos, mas trate o resultado como lista de candidatos.
- Para contagens após joins com endereço, pessoal, motorista ou ordem de compra, use `count(distinct cgm.z01_numcgm)` quando a pergunta for sobre pessoas ou entidades.
- Diferencie o endereço textual de `cgm`, os vínculos legados de rua/bairro e o modelo normalizado de `cgmendereco`.
- Não assuma que o primeiro endereço retornado é principal. Para a regra LicitaCon, aplique explicitamente `z07_tipo = 'P'` e a ordenação definida.
- Não reutilize os caminhos jurídico e combinado de `sql_query_cgmtipo` sem corrigir e validar o join.
- Evite expor CPF, CNPJ, identidade, nascimento, falecimento, telefone, e-mail ou endereço completo quando a pergunta puder ser respondida sem esses dados.
- Nas consultas novas, substitua concatenação de valores por parâmetros vinculados.
