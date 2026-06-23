## cadastro.iptutaxacalv

> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptutaxacalv_classe.php`

Tabela de calculo de taxa de iptu. Esta classe nao se comporta como um CRUD simples: o destaque real e a consulta analitica que consolida valores por exercicio e receita.

### Estrutura e interpretacao

- **Classe:** `cl_iptutaxacalv`
- **Tabela principal:** `iptutaxacalv`
- **Grau basico:** uma linha por calculo de taxa, identificada por `j152_codigo`
- **Uso de negocio:** fatos monetarios de taxa vinculada ao IPTU, com origem no calculo e referencia a receita, historico e numeracao da taxa

Campos de negocio confirmados:

- `j152_codigo`: identificador da linha
- `j152_iptutaxanump`: referencia para a numeracao/base da taxa
- `j152_codhis`: historico de calculo
- `j152_receit`: receita usada no calculo
- `j152_valor`: valor calculado
- `j152_quant`: quantidade do item calculado

Interpretacao segura:

- A tabela guarda itens calculados de taxa, nao o cadastro fisico do imovel.
- O grao minimo seguro e a linha individual de calculo.
- Para agregacoes financeiras, a unidade natural e por exercicio, receita e origem do calculo.

### Relacionamentos de negocio confirmados no catalogo

- `iptutaxacalv.j152_iptutaxanump -> iptutaxanump.j151_codigo`
- `iptutaxacalv.j152_codhis -> iptucalh.j17_codhis`
- `iptutaxacalv.j152_receit -> tabrec.k02_codigo`

### Consultas da classe

Esta classe nao expoe leitura basica em `sql_query` ou `sql_query_file`. O unico metodo relevante e a consulta consolidada abaixo.

### Consulta: `sql_queryValoresCalculoIptu`

- **Objetivo:** consolidar por ano os valores calculados de taxa e seu estado financeiro, separando calculado, isento, cancelado, compensado, pago, a pagar, importado e quantidade.
- **Grão do resultado:** ano de calculo + codigo de receita + descricao da receita
- **Tabelas principais:** `iptutaxacalv`, `iptutaxanump`, `iptucadtaxaexe`, `iptucalhconf`, `iptuisen`, `isenexe`, `tipoisen`, `arrecant`, `cancdebitosreg`, `cancdebitosprocreg`, `abatimentoutilizacaodestino`, `abatimentoutilizacao`, `abatimento`, `arreckey`, `abatimentoarreckey`, `arreold`, `divold`, `diverimportaold`, `diversos`, `issvar`, `iptucalv`, `iptunump`, `tabrec`

Leitura funcional:

- `valor_calculado`: soma dos valores positivos de taxa calculada.
- `valor_isento`: soma dos valores negativos tratados como isencao.
- `valor_cancelado`: soma de valores cancelados.
- `valor_compensado`: soma de valores compensados por abatimento ou mecanismo equivalente.
- `valor_pago`: soma de valores efetivamente pagos.
- `valor_a_pagar`: saldo pendente depois dos movimentos financeiros.
- `valor_importado`: valor trazido de rotinas legadas de importacao/arrecadacao antiga.
- `quantidade`: total de quantidade associada aos itens de calculo.

Interpretacao segura:

- O metodo e analitico e serve para visao consolidada de taxa por exercicio.
- Ele cruza calculo tributario com arrecadacao, cancelamento, isencao, compensacao e importacao legada.
- E apropriado para relatorios, paineis e conferencias de fechamento, nao para detalhamento de uma linha isolada.

### Cuidados

- O SQL da classe tem trechos legados e merece leitura critica antes de ser usado como regra canonica.
- Ha um trecho com `<> null` para testar valor importado de `arreold`; isso e semanticamente incorreto em SQL e deveria ser `is not null`.
- Se o agente precisar de detalhamento de uma matricula ou de uma taxa especifica, a consulta consolidada nao e suficiente sozinha.

### Perguntas que ela responde bem

- Qual foi o total calculado de taxa de iptu por exercicio?
- Quanto ficou isento, cancelado, compensado, pago ou a pagar?
- Qual e o peso das importacoes legadas no consolidado anual?

### Relacoes com outras visoes

- A tabela entra no consolidado unificado de valores de calculo junto com `iptucalv`.
- Ela e consumida por rotinas de emissao, comparacao, relatorios e logica de cadastro tributario que precisam somar IPTU + taxas.
- Para reconciliar valor de taxa com a numeracao da base, a cadeia pratica e `iptutaxacalv -> iptutaxanump -> iptucadtaxaexe`.
