# e-Cidade — Cadastro Imobiliário

## Tabela principal: `ruas`

| Campo | Tipo inferido | Descrição |
|---|---:|---|
| `j14_codigo` | int | Código do logradouro/rua. Chave principal lógica da tabela. |
| `j14_nome` | string/null | Nome do logradouro. |
| `j14_tipo` | int/null | Tipo do logradouro, normalmente relacionado à tabela `ruastipo`. |
| `j14_rural` | bool/null | Indicador se a rua/logradouro é rural. |
| `j14_lei` | string/null | Lei vinculada ao logradouro. |
| `j14_dtlei` | string/date/null | Data da lei vinculada ao logradouro. |
| `j14_bairro` | string/null | Bairro informado no cadastro da rua. Atenção: pode não ser o mesmo vínculo normalizado usado em `ruasbairro`. |
| `j14_obs` | string/null | Observações do logradouro. |

## Relacionamentos extraídos

### `ruascep`

Usado no scope `joinCep()`.

| Relação | Condição |
|---|---|
| `ruas` → `ruascep` | `ruascep.j29_codigo = ruas.j14_codigo` |

Campos relevantes inferidos pelo uso:

| Campo | Descrição |
|---|---|
| `j29_codigo` | Código do logradouro vinculado ao CEP. |
| `j29_cep` | CEP do logradouro. |

## Scopes / métodos de consulta

### `scopeNome(Builder $query, $nome)`

Filtra a rua pelo nome normalizado, removendo acentos/caracteres especiais e comparando em caixa alta.

Regra SQL equivalente:


Parâmetro:

| Parâmetro | Uso |
|---|---|
| `:nome_normalizado` | Nome sem acentos/caracteres especiais e em maiúsculas. |

### `scopeJoinCep(Builder $query)`

Adiciona join com a tabela `ruascep`.

SQL equivalente:


### `scopeCep(Builder $query, $cep)`

Filtra pelo CEP após o join com `ruascep`.

SQL equivalente:


## Queries SQL prontas

### 1. Buscar rua pelo código


### 2. Buscar rua pelo nome normalizado


Uso recomendado: aplicar no parâmetro a mesma normalização usada pela aplicação (`DBString::removerCaracteresEspeciaisAcentos`) antes da consulta.

### 3. Buscar rua por CEP


### 4. Buscar rua por nome e CEP


### 5. Listar CEPs de uma rua


## Filtros seguros e recomendados

| Necessidade | Filtro recomendado |
|---|---|
| Rua por código | `ruas.j14_codigo = :codigo_rua` |
| Rua por nome exato normalizado | `upper(to_ascii(j14_nome)) = upper(to_ascii(:nome_rua))` |
| Rua por CEP | `join ruascep` + `ruascep.j29_cep = :cep` |
| Rua rural/urbana | `j14_rural = true/false` |

## Cuidados de uso

- O model não declara `$primaryKey`; no Eloquent, o padrão seria `id`. Para operações de escrita ou busca por chave, é recomendável configurar explicitamente `protected $primaryKey = 'j14_codigo';` caso esse model seja usado para persistência direta.
- O model não declara `public $timestamps = false`; se a tabela `ruas` não possuir `created_at` e `updated_at`, isso deve ser configurado para evitar erro em operações de escrita.
- O scope `cep()` depende do join com `ruascep`; usar `Ruas::cep($cep)` sem `joinCep()` pode gerar SQL inválido por ausência da tabela/alias `ruascep`.
- A busca por nome usa comparação exata após normalização. Não é busca parcial. Para autocomplete ou pesquisa flexível, usar `like`/`ilike` com normalização adequada.
- O campo `j14_bairro` aparece no PHPDoc como string, mas em outras classes do cadastro imobiliário o relacionamento normalizado de rua/bairro pode ocorrer por tabelas auxiliares, como `ruasbairro`. Validar antes de assumir vínculo direto.

## Perguntas que esta referência ajuda a responder

- Qual tabela armazena logradouros/ruas?
- Como buscar uma rua pelo nome ignorando acentos?
- Como relacionar rua com CEP?
- Qual campo representa o código da rua?
- Como listar CEPs vinculados a uma rua?
