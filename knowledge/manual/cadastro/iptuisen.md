# Tabela de negocio: `cadastro.iptuisen`

## Identidade

- Nome humano: isencoes de IPTU da matricula.
- O que representa: cada linha registra uma isencao vinculada a uma matricula, com tipo, vigencia, percentual e historico.
- Quando usar:
  - listar isencoes de uma matricula;
  - analisar periodo de vigencia de isencao;
  - identificar tipo e percentual de isencao;
  - explicar reducoes no calculo quando houver vinculo com exercicio/isencao.
- Quando evitar:
  - para valor final calculado do IPTU, usar `iptucalv`;
  - para valor de isencao aplicado no calculo principal, verificar tambem `iptucalc.j23_vlrisen`;
  - para pagamento/arrecadacao, usar tabelas financeiras.

## Grao e chaves

- Grao: uma linha por registro de isencao.
- Entidade principal: isencao de matricula.
- Chave de negocio:
  - `j46_codigo`
- Coluna temporal:
  - `j46_dtini`
  - `j46_dtfim`
  - `j46_dtinc`

## Colunas principais

- `j46_codigo`: codigo da isencao.
- `j46_matric`: matricula.
- `j46_tipo`: tipo de isencao.
- `j46_dtini`: data inicial de vigencia.
- `j46_dtfim`: data final de vigencia.
- `j46_perc`: percentual da isencao.
- `j46_dtinc`: data de inclusao.
- `j46_hist`: historico/justificativa.
- `j46_arealo`: area de lote associada ao contexto da isencao.

## Filtros de negocio

- Matricula: `j46_matric`.
- Tipo de isencao: `j46_tipo`.
- Vigencia por data: usar `j46_dtini` e `j46_dtfim`.
- Isencoes sem fim informado: `j46_dtfim IS NULL`.

## Regra de contagem

- Contar linhas de `iptuisen` conta registros de isencao.
- Para contar matriculas com isencao, usar `COUNT(DISTINCT j46_matric)`.
- Para contar tipos de isencao, agrupar por `j46_tipo`.

## Regra de agregacao

- Percentual de isencao nao deve ser somado sem regra especifica.
- Para impacto financeiro, comparar com valores calculados em `iptucalc`/`iptucalv`.

## Relacionamentos importantes

- `iptuisen.j46_matric = iptubase.j01_matric`
- `iptuisen.j46_tipo = tipoisen.j45_tipo`
- `iptuisen.j46_codigo = isenexe.j47_codigo`, quando analisar exercicio de isencao.
- `iptuisen.j46_codigo = isentaxa.j56_codigo`, quando envolver taxas isentas.

## Riscos de duplicidade

- Uma matricula pode ter varias isencoes.
- Uma isencao pode ter exercicios associados em outra tabela.
- Join com taxas ou exercicios pode multiplicar registros.

## O que nao inferir

- Nao inferir valor economico da isencao apenas pelo percentual.
- Nao assumir isencao vigente sem avaliar datas e exercicio.
- Nao confundir `j46_codigo` com tipo de isencao.

## Cuidados

- `j46_dtfim` nulo pode representar ausencia de fim de vigencia.
- `j46_perc` zero nao prova ausencia de beneficio sem olhar tipo e regra local.
