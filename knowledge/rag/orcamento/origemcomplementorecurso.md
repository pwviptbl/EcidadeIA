## orcamento.origemcomplementorecurso

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_origemcomplementorecurso_classe.php`

Relaciona um recurso e seu complemento a uma origem de negócio específica. A classe é enxuta, baseada em `DAOBasica`, e expõe uma consulta principal para enriquecer a origem com o complemento da fonte e o tipo de recurso.

### Estrutura e interpretacao

- **Classe:** `cl_origemcomplementorecurso`
- **Tabela principal:** `origemcomplementorecurso`
- **Chave primaria:** `o206_sequencial`
- **Grau basico:** uma linha por vínculo entre origem, número de negócio, recurso e complemento

Campos de negocio confirmados:

- `o206_sequencial`: identificador sequencial do vínculo
- `o206_origem`: tipo de origem
- `o206_numero`: número da entidade/documento de origem
- `o206_recurso`: recurso vinculado em `orctiporec`
- `o206_complementorecurso`: complemento da fonte de recurso

Interpretacao segura:

- A tabela não descreve a receita/despesa em si; ela registra de onde veio a associação do complemento.
- `o206_origem` depende do cadastro `tipoorigemcomplementorecurso`.
- `o206_numero` é o identificador do objeto daquela origem no sistema.

### Consulta: `sql_query_complemento`

- **Objetivo:** recuperar o vínculo da origem com enriquecimento do complemento e do recurso.
- **Tabelas:** `origemcomplementorecurso`, `complementofonterecurso`, `orctiporec`

```sql
select /* campos dinamicos */
  from origemcomplementorecurso
       inner join complementofonterecurso
          on complementofonterecurso.o200_sequencial = origemcomplementorecurso.o206_complementorecurso
       inner join orctiporec
          on orctiporec.o15_codigo = origemcomplementorecurso.o206_recurso
 where /* filtro opcional */
```

Interpretacao segura:

- Esta é a única consulta especializada da classe e já entrega o contexto legado completo do recurso.
- Use quando a pergunta depender de "qual complemento de fonte foi usado" e "de qual origem esse vínculo veio".

### Relacionamentos de negocio confirmados no catalogo

- `origemcomplementorecurso.o206_origem -> tipoorigemcomplementorecurso.o168_sequencial`
- `origemcomplementorecurso.o206_recurso -> orctiporec.o15_codigo`

Interpretacao segura:

- O primeiro relacionamento responde "qual é o tipo da origem".
- O segundo ancora o vínculo no recurso orçamentário legado.

### Relacionamentos semanticos relevantes

- `origemcomplementorecurso -> fonterecurso` via `orctiporec`
- `origemcomplementorecurso -> orcdotacao` via `orctiporec`
- `origemcomplementorecurso -> orcdotacaocontr` via `orctiporec`

Interpretacao segura:

- Quando a análise sair da origem e precisar chegar em dotação ou fonte nova, o caminho natural passa por `orctiporec`.

### Regras de manutencao observadas

1. A classe herda de `DAOBasica` e não implementa manualmente `incluir/alterar/excluir`.
2. O comportamento operacional principal exposto no arquivo é a leitura por `sql_query_complemento`.

### Cuidados para consultas do agente

- Não confundir `o206_complementorecurso` com o recurso em si: ele representa o detalhamento/complemento.
- Para responder sobre a semântica da origem, normalmente será necessário cruzar `o206_origem` com `tipoorigemcomplementorecurso`.
- Para perguntas sobre fonte atual por exercício, pode ser necessário continuar o caminho de `orctiporec` até `fonterecurso`.
