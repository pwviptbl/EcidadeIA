# Tabela de negocio: `cadastro.iptuconstr`

## Identidade

- Nome humano: construcoes cadastradas da matricula.
- O que representa: cada linha representa uma construcao/edificacao vinculada a uma matricula imobiliaria.
- Quando usar:
  - contar construcoes cadastradas;
  - somar area construida cadastral;
  - filtrar construcoes ativas/demolidas;
  - relacionar construcao com caracteristicas ou calculo por edificacao.
- Quando evitar:
  - para valor venal calculado da construcao por exercicio, usar `cadastro.iptucale`;
  - para caracteristicas da construcao, usar `cadastro.carconstr`;
  - para valor final de IPTU, usar `cadastro.iptucalv`.

## Grao e chaves

- Grao: uma linha por matricula e identificador de construcao.
- Entidade principal: construcao dentro de uma matricula.
- Chave de negocio:
  - `j39_matric`
  - `j39_idcons`
- Coluna temporal:
  - `j39_dtlan`, data de lancamento cadastral;
  - `j39_dtdemo`, data de demolicao/baixa da construcao.

## Colunas principais

- `j39_matric`: matricula do imovel.
- `j39_idcons`: identificador da construcao dentro da matricula.
- `j39_area`: area da construcao conforme cadastro.
- `j39_areap`: area principal, conforme regra local.
- `j39_areajirau`: area de jirau.
- `j39_areajiraudeposito`: area de jirau/deposito.
- `j39_areamezanino`: area de mezanino.
- `j39_dtlan`: data de lancamento.
- `j39_dtdemo`: data de demolicao/baixa.
- `j39_ano`: ano de edificacao, quando preenchido.
- `j39_idprinc`: indicador de construcao principal, quando aplicavel.

## Metricas atomicas

- `area_construida`: `j39_area`, agregacao comum `sum`.
- `area_principal`: `j39_areap`, agregacao depende da regra municipal.
- `quantidade_construcoes`: contagem por `j39_matric, j39_idcons`.

## Filtros de negocio

- Construcoes ativas: `j39_dtdemo IS NULL`.
- Construcoes demolidas: `j39_dtdemo IS NOT NULL`.
- Matricula: `j39_matric`.
- Construcao especifica: `j39_matric` e `j39_idcons`.
- Ano da edificacao: `j39_ano`.

## Regra de contagem

- Para contar construcoes diretamente em `iptuconstr`, usar `COUNT(1)` quando o grao nao foi multiplicado.
- Se houver join com caracteristicas (`carconstr`), usar `COUNT(DISTINCT (j39_matric, j39_idcons))` ou agregar antes, porque uma construcao pode ter varias caracteristicas.
- Para contar imoveis com construcao, usar `COUNT(DISTINCT j39_matric)`.

## Regra de agregacao

- Para area construida ativa, aplicar `j39_dtdemo IS NULL`.
- Nao somar todas as colunas de area sem regra municipal; `j39_area`, `j39_areap`, jirau e mezanino podem ter usos diferentes.

## Relacionamentos importantes

- `iptuconstr.j39_matric = iptubase.j01_matric`
- `iptuconstr.j39_matric = carconstr.j48_matric` e `iptuconstr.j39_idcons = carconstr.j48_idcons`
- `iptuconstr.j39_matric = iptucale.j22_matric` e `iptuconstr.j39_idcons = iptucale.j22_idcons`

## Riscos de duplicidade

- Uma matricula pode ter varias construcoes.
- Uma construcao pode ter varias caracteristicas.
- Uma construcao pode ter calculos por exercicio em `iptucale`.

## O que nao inferir

- Nao inferir matricula ativa apenas porque a construcao esta ativa.
- Nao assumir que area cadastral atual e igual a area usada no calculo de um exercicio.
- Nao tratar construcao demolida como ativa em analises correntes.

## Cuidados

- Construcoes demolidas podem permanecer para historico.
- Para analise de calculo por ano, preferir `iptucale` ou `iptucalc` conforme a pergunta.
