# Tabela de negocio: `cadastro.caracter`

## Identidade

- Nome humano: cadastro mestre de caracteristicas.
- O que representa: cada linha representa uma caracteristica cadastrada para uso em lote, construcao, face de quadra ou outro contexto parametrizado.
- Quando usar:
  - obter descricao textual da caracteristica;
  - interpretar pontuacao e grupo;
  - classificar caracteristicas por tipo usando `cargrup`;
  - listar caracteristicas cadastradas.
- Quando evitar:
  - para contar uso real em construcoes, usar `carconstr`;
  - para contar uso real em lotes, usar `carlote`;
  - para contar uso real em faces, usar `carface`.

## Grao e chaves

- Grao: uma linha por caracteristica cadastrada.
- Entidade principal: caracteristica mestre.
- Chave de negocio:
  - `j31_codigo`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j31_codigo`: codigo da caracteristica.
- `j31_descr`: descricao textual da caracteristica.
- `j31_grupo`: grupo da caracteristica.
- `j31_pontos`: pontuacao atribuida, quando aplicavel.

## Dimensoes relacionadas

- Grupo da caracteristica: `caracter.j31_grupo -> cargrup.j32_grupo`.
- Tipo de aplicacao: `cargrup.j32_tipo`, quando documentado no municipio.

## Filtros de negocio

- Caracteristica especifica: `j31_codigo`.
- Busca por descricao: `j31_descr`.
- Grupo: `j31_grupo`.
- Caracteristicas de construcao: cruzar com `cargrup` e aplicar tipo de construcao.
- Caracteristicas de lote: cruzar com `cargrup` e aplicar tipo de lote.
- Caracteristicas de face: cruzar com `cargrup` e aplicar tipo de face.

## Regra de contagem

- Contar linhas de `caracter` conta caracteristicas cadastradas, nao uso real.
- Para contar uso em construcoes, usar `carconstr`.
- Para contar uso em lotes, usar `carlote`.
- Para contar uso por grupo, cruzar com `cargrup`.

## Regra de agregacao

- Agrupar por codigo quando houver risco de descricoes repetidas.
- Agrupar por descricao apenas quando a pergunta for explicitamente textual e a duplicidade nao comprometer o resultado.

## Relacionamentos importantes

- `caracter.j31_grupo = cargrup.j32_grupo`
- `caracter.j31_codigo = carconstr.j48_caract`
- `caracter.j31_codigo = carlote.j35_caract`
- `caracter.j31_codigo = carface.j47_caract`, quando `carface` estiver no contexto.

## Riscos de duplicidade

- Descricoes podem ser abreviadas, genericas ou repetidas.
- O mesmo conceito humano pode ser parametrizado de forma diferente por municipio.

## O que nao inferir

- Nao inferir uso real de caracteristica a partir do cadastro mestre.
- Nao inferir tipo de aplicacao sem olhar `cargrup`.
- Nao inferir regra de calculo completa apenas por pontuacao.

## Cuidados

- `j31_pontos` pode influenciar calculo, mas nao explica sozinho a formula.
- Caracteristicas sao dinamicas e variam por municipio.
