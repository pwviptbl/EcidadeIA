# ITBI legado vinculado à matrícula imobiliária

> Fonte principal: `/var/www/html/e-cidade-php74/classes/db_db_itbi_classe.php`
>
> Classe: `cl_db_itbi`
>
> Tabela principal: `db_itbi`

## Escopo da entidade

`db_itbi` é um cadastro legado de ITBI vinculado diretamente à matrícula do imóvel. Ele armazena, na mesma linha, dados do imóvel, comprador, transação, avaliação, pagamento e liberação.

Esta tabela não é a mesma entidade que `itbi.itbi`, cuja chave encontrada em outros documentos é `it01_guia`. Não combine registros das duas tabelas apenas pela semelhança do nome.

Identificadores observados:

| Campo | Uso na classe |
|---|---|
| `matricula` | Chave usada nas consultas, alterações e exclusões |
| `id_itbi` | Número sequencial denominado “Guia” |
| `numpre` | Número do débito na arrecadação |

A manutenção da classe trata `matricula` como chave do registro. `id_itbi` é gerado pela sequência `db_itbi_id_itbi_seq` e também é usado por uma tela para localizar a observação da guia.

## Campos relevantes

### Imóvel

| Campo | Significado definido pela classe |
|---|---|
| `matricula` | Matrícula imobiliária |
| `areaterreno` | Área do terreno |
| `areaedificada` | Área edificada |
| `caracteristicas` | Características |
| `mfrente` | Medida da frente |
| `mladodireito` | Medida do lado direito |
| `mfundos` | Medida dos fundos |
| `mladoesquerdo` | Medida do lado esquerdo |

### Comprador

| Campo | Significado definido pela classe |
|---|---|
| `nomecomprador` | Nome do comprador |
| `cgccpfcomprador` | CPF ou CNPJ do comprador |
| `enderecocomprador` | Endereço |
| `numerocomprador` | Número |
| `complcomprador` | Complemento |
| `bairrocomprador` | Bairro |
| `municipiocomprador` | Município |
| `ufcomprador` | UF |
| `cepcomprador` | CEP |
| `cxpostcomprador` | Caixa postal |
| `email` | E-mail |

Os dados do comprador são textuais e não possuem, nesta classe, vínculo com `cgm`. Nome e CPF/CNPJ não devem ser usados como chave sem normalização e validação.

### Transação, avaliação e arrecadação

| Campo | Significado definido pela classe |
|---|---|
| `tipotransacao` | Tipo textual da transação |
| `valortransacao` | Valor da transação |
| `aliquota` | Alíquota |
| `valoravaliacao` | Valor avaliado |
| `valoravterr` | Valor da avaliação do terreno |
| `valoravconst` | Valor da avaliação da construção/prédio |
| `valorpagamento` | Valor pago |
| `numpre` | Número na arrecadação |
| `datavencimento` | Data de vencimento |
| `datasolicitacao` | Data da solicitação |

### Liberação

| Campo | Significado definido pela classe |
|---|---|
| `liberado` | Indicador numérico denominado “Liberado” |
| `libpref` | Campo numérico denominado “Liberação da Prefeitura” |
| `dataliber` | Data da liberação |
| `obsliber` | Observação da liberação |
| `loginn` | Login associado |
| `obs` | Observação geral |

A classe não define o domínio dos valores de `liberado` ou `libpref`. Não interprete `0`, `1` ou outros valores como estado específico sem evidência de uma rotina consumidora.

## Obrigatoriedades da inclusão

O método `incluir` exige:

- matrícula;
- áreas do terreno e edificada;
- nome, CPF/CNPJ e endereço básico do comprador;
- município, bairro, CEP e UF do comprador;
- tipo e valor da transação;
- características e quatro medidas do imóvel;
- observação;
- indicador de liberação;
- vencimento;
- alíquota;
- guia;
- data, valor e observação da liberação;
- valor pago;
- login;
- número da arrecadação;
- data da solicitação;
- liberação da prefeitura;
- valores avaliados do terreno e da construção;
- número do endereço do comprador.

`email`, complemento e caixa postal não aparecem entre as validações obrigatórias.

### Inconsistência na geração da guia

O método primeiro valida `$this->id_itbi`, mas depois testa a variável local `$id_itbi`, que não é parâmetro nem foi inicializada:

```php
if ($id_itbi == "" || $id_itbi == null) {
    select nextval('db_itbi_id_itbi_seq')
}
```

Consequência observável:

- o caminho tende a gerar `id_itbi` pela sequência, independentemente do valor existente em `$this->id_itbi`;
- o ramo que tenta aceitar um número informado não é alcançado de forma confiável;
- a validação prévia de `id_itbi` é contraditória com a geração automática posterior.

## Consulta direta do cadastro

### Consultas: `sql_query` e `sql_query_file`

Os dois métodos geram a mesma consulta:

```sql
select /* campos dinâmicos */
  from db_itbi
 where db_itbi.matricula = :matricula
 order by /* ordenação dinâmica */
```

Não há diferença de joins ou semântica entre eles.

Regras:

- O filtro padrão é a matrícula.
- Uma condição livre substitui o filtro pela matrícula.
- Os métodos não filtram guia, pagamento, vencimento ou situação automaticamente.
- A tela `cad3_consultaitbi003.php` usa a existência de registro em `db_itbi` para validar que a matrícula possui esse cadastro legado.

Para localizar pela guia:

```sql
select *
  from db_itbi
 where id_itbi = :guia
```

Esse padrão é observado em `pre4_liberaitbi002.php`, que recupera `obs` pelo número da guia.

## Consulta do ITBI com o cadastro imobiliário

### Consulta: `sql_query_itbi`

- **Objetivo:** Recuperar o ITBI legado junto dos dados cadastrais do imóvel e do proprietário.
- **Grão esperado:** Uma linha por matrícula e registro de histórico anterior associado.

```sql
select /* campos dinâmicos */
  from iptubase
       inner join lote
          on lote.j34_idbql = iptubase.j01_idbql
       inner join cgm
          on cgm.z01_numcgm = iptubase.j01_numcgm
       inner join bairro
          on bairro.j13_codi = lote.j34_bairro
       inner join setor
          on setor.j30_codi = lote.j34_setor
       left join iptuant
         on iptuant.j40_matric = iptubase.j01_matric
       inner join db_itbi
          on db_itbi.matricula = iptubase.j01_matric
 where iptubase.j01_matric = :matricula
 order by /* ordenação dinâmica */
```

Relacionamentos:

- `iptubase` fornece a matrícula, o identificador do lote e o CGM do cadastro imobiliário.
- `lote` fornece bairro e setor.
- `cgm` representa o contribuinte relacionado em `iptubase.j01_numcgm`.
- `db_itbi` restringe a imóveis que possuem o cadastro legado de ITBI.
- `iptuant` é opcional.

Cuidados:

- Todos os relacionamentos, exceto `iptuant`, são obrigatórios.
- A ausência de bairro, setor, lote, CGM ou `db_itbi` exclui a matrícula do resultado.
- `iptuant` pode gerar mais de uma linha para a mesma matrícula se houver vários registros históricos.
- Os joins de `bairro` e `setor` usam apenas seus códigos. Se esses códigos não forem globalmente únicos no banco, a consulta pode multiplicar ou associar registros de outro contexto.
- O CGM relacionado é o registrado no cadastro imobiliário, não o comprador textual de `db_itbi`.

## Consulta ampliada usada pelas telas

As telas `cad3_consultaitbi002.php` e `cad3_consultaitbi003.php` estendem a consulta com:

```sql
inner join testpri
        on testpri.j49_idbql = iptubase.j01_idbql
inner join ruas
        on ruas.j14_codigo = testpri.j49_codigo
```

Essa extensão permite pesquisar ou exibir a rua principal do imóvel.

Como `testpri` pode possuir cardinalidade própria, a tela usa campos específicos ou espera um único resultado. Para contar matrículas, use `count(distinct iptubase.j01_matric)`.

## Relação com o ITBI atual

Existem no mesmo sistema tabelas como:

- `itbi.itbi`;
- `itbimatric`;
- `itbinome`;
- `itbicgm`;
- `itbitransacao`;
- `itbiavalia`;
- `itbinumpre`;
- `averbaguiaitbi`.

A classe `cl_db_itbi` não relaciona essas tabelas. Seu único vínculo de negócio explícito é com a matrícula de `iptubase`.

Portanto:

- não use `db_itbi.id_itbi = itbi.it01_guia` sem confirmar uma relação física ou regra adicional;
- não use `db_itbi.numpre` como substituto automático de `itbinumpre`;
- não combine compradores textuais de `db_itbi` com adquirentes/transmitentes das tabelas atuais sem uma chave comprovada.

## Cardinalidade e contagens

- A manutenção da classe pressupõe consulta e exclusão por matrícula.
- `id_itbi` funciona como número de guia, mas não é usado como chave de alteração/exclusão.
- `sql_query_itbi` pode multiplicar linhas por histórico de `iptuant` ou por extensões adicionadas pelas telas.
- Para quantidade de imóveis com ITBI legado:

```sql
select count(distinct db_itbi.matricula)
  from db_itbi
```

- Para quantidade de guias:

```sql
select count(distinct db_itbi.id_itbi)
  from db_itbi
```

Essas contagens só serão equivalentes se houver exatamente uma guia por matrícula. A classe sugere essa expectativa na manutenção, mas não comprova a restrição física do banco.

## Recomendações para consultas do agente

- Declare explicitamente que `db_itbi` é o cadastro legado vinculado à matrícula.
- Use `matricula` para relacionar com `iptubase.j01_matric`.
- Use `id_itbi` quando a pergunta citar o número da guia desse cadastro.
- Use `numpre` apenas para relacionar com arrecadação depois de validar tipo e formato do campo.
- Não derive situação de pagamento somente de `valorpagamento`; confirme o débito nas tabelas de arrecadação.
- Não derive liberação somente pelo nome dos campos `liberado` e `libpref`; o domínio dos valores não está definido na classe.
- Diferencie o proprietário/CGM de `iptubase` do comprador textual armazenado em `db_itbi`.
- Para contagens após joins, use `distinct matricula` ou `distinct id_itbi` conforme a pergunta.
- CPF/CNPJ, nome, endereço e e-mail são dados pessoais. Retorne somente os campos necessários.
- Campos, filtros e ordenações são concatenados pelo legado. Novas consultas devem utilizar parâmetros vinculados e allowlist de colunas.
