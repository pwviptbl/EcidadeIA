# Tabela de negocio: `cadastro.setor`

## Identidade

- Nome humano: setor cadastral/imobiliario.
- O que representa: cada linha representa um setor usado como dimensao territorial/fiscal.
- Quando usar:
  - listar setores;
  - agrupar lotes ou matriculas por setor;
  - analisar aliquotas predial/territorial associadas ao setor;
  - verificar vinculos territoriais.
- Quando evitar:
  - para valor calculado de IPTU por matricula, usar `iptucalc`/`iptucalv`;
  - para bairro, usar `bairro`;
  - para zona de valor, usar tabela de zona quando a pergunta pedir zona.

## Grao e chaves

- Grao: uma linha por setor.
- Entidade principal: setor territorial/fiscal.
- Chave de negocio:
  - `j30_codi`
- Coluna temporal:
  - nao informada.

## Colunas principais

- `j30_codi`: codigo do setor.
- `j30_descr`: descricao do setor.
- `j30_alipre`: aliquota predial associada ao setor.
- `j30_aliter`: aliquota territorial associada ao setor.

## Filtros de negocio

- Setor por codigo: `j30_codi`.
- Setor por descricao: `j30_descr`.

## Regra de contagem

- Contar linhas de `setor` conta setores cadastrados.
- Para contar lotes por setor, cruzar com `lote` e contar `COUNT(DISTINCT lote.j34_idbql)`.
- Para contar matriculas por setor, cruzar `setor -> lote -> iptubase` e contar `COUNT(DISTINCT iptubase.j01_matric)`.

## Regra de agregacao

- Aliquotas do setor podem ser usadas como dimensao/parametro, mas nao explicam sozinhas o valor final do IPTU sem comparar calculos.

## Relacionamentos importantes

- `setor.j30_codi = lote.j34_setor`
- `setor.j30_codi = face.j37_setor`, quando `face` estiver no contexto.
- `setor.j30_codi` pode se relacionar com valores por zona/setor conforme catalogo local.

## Riscos de duplicidade

- Um setor possui varios lotes.
- Um lote pode estar ligado a mais de uma matricula.

## O que nao inferir

- Nao atribuir aumento de IPTU apenas ao setor sem consultar calculo/valores.
- Nao tratar setor como bairro.

## Cuidados

- `j30_codi` pode ter zeros a esquerda ou formato `char`; preservar codigo ao filtrar.
