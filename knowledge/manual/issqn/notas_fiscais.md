# Conceito de negocio: notas_fiscais_de_servico

## Identidade e escopo

- Nome humano: notas fiscais de servico vinculadas ao ISSQN.
- O que representa: conceito de negocio que reune fontes diferentes de notas declaradas e notas avulsas.
- Nao existe uma unica tabela que represente todas as notas fiscais de servico; o agente deve escolher a fonte conforme a pergunta.
- Para notas declaradas na apuracao mensal, usar `issqn.issvarnotas` com `issqn.issvar`.
- Para notas avulsas emitidas pelo municipio, usar `issqn.issnotaavulsa` com `issqn.issnotaavulsaservico`.
- Nao misturar as duas fontes na mesma contagem sem regra explicita de unificacao e deduplicacao.

## Fontes, graos e chaves

- `issqn.issvarnotas`: uma linha por nota declarada dentro de uma apuracao de ISS variavel.
- Chave tecnica da nota declarada: `q06_codigo` e `q06_seq`; `q06_nota` sozinho pode se repetir.
- `issqn.issvar`: uma linha de apuracao mensal, identificada por `q05_codigo`, com ano, mes e valor do imposto.
- `issqn.issnotaavulsa`: uma linha por nota avulsa, identificada por `q51_sequencial`.
- `issqn.issnotaavulsaservico`: uma linha por item de servico da nota avulsa, identificada por `q62_sequencial`.
- Uma nota avulsa pode possuir varios itens de servico; joins com itens multiplicam o cabecalho.

## Notas declaradas em `issvarnotas`

- Relacionamento: `issvarnotas.q06_codigo = issvar.q05_codigo`.
- Numero informado da nota: `issvarnotas.q06_nota`.
- Valor da nota declarada: `issvarnotas.q06_valor`.
- Competencia da declaracao: `issvar.q05_ano` e `issvar.q05_mes`.
- Valor de ISS devido na apuracao: `issvar.q05_valor`.
- Valor de ISS informado pelo contribuinte: `issvar.q05_vlrinf`.
- `issvar.q05_valor` pertence ao grao da apuracao, nao ao grao de cada nota.
- Ao relacionar apuracao e notas, agregar a quantidade e o valor das notas por `q06_codigo` antes de somar `q05_valor`, evitando repetir o ISS mensal para cada nota.

## Notas avulsas e cancelamentos

- Cabecalho: `issnotaavulsa.q51_sequencial`, `q51_numnota`, `q51_inscr` e `q51_dtemiss`.
- Itens: `issnotaavulsaservico.q62_issnotaavulsa = issnotaavulsa.q51_sequencial`.
- Valor total do item: `issnotaavulsaservico.q62_vlrtotal`.
- Base de calculo: `issnotaavulsaservico.q62_vlrbasecalc`.
- Valor de ISS do item: `issnotaavulsaservico.q62_vlrissqn`.
- Cancelamento: `issnotaavulsacanc.q63_issnotaavulsa = issnotaavulsa.q51_sequencial`.
- Para notas validas, excluir a nota quando existir registro correspondente em `issnotaavulsacanc`.
- A data `issnotaavulsacanc.q63_data` e data do cancelamento, nao data de emissao.

## Regras de contagem e valor

- Quantidade de notas declaradas: contar a chave composta `q06_codigo` e `q06_seq`, nao apenas `q06_nota`.
- Quantidade de notas avulsas: contar `DISTINCT issnotaavulsa.q51_sequencial` depois de excluir canceladas.
- Valor total das notas declaradas: somar `issvarnotas.q06_valor` no recorte de competencia.
- Valor total das notas avulsas: somar `issnotaavulsaservico.q62_vlrtotal` por nota valida.
- ISS das notas avulsas: somar `issnotaavulsaservico.q62_vlrissqn` por nota valida.
- ISS das notas declaradas: usar `issvar.q05_valor` como imposto devido da apuracao, somando cada `q05_codigo` uma unica vez.
- Nao tratar valor da nota como valor de ISS.
- Nao tratar ISS devido, ISS informado, ISS retido, ISS pago e ISS arrecadado como a mesma metrica.

## Competencia versus data de emissao

- Para notas declaradas em `issvarnotas`, o recorte temporal disponivel e a competencia em `issvar.q05_ano` e `q05_mes`.
- `issvarnotas` nao possui data individual de emissao da nota no catalogo atual.
- Para notas avulsas, usar `issnotaavulsa.q51_dtemiss` quando a pergunta pedir emissao em determinado periodo.
- `issnotaavulsa.q51_data` e data de inclusao e nao deve substituir automaticamente a data de emissao.
- Perguntas por competencia e por data de emissao podem produzir universos diferentes.
- Se o usuario disser apenas "em 2025", usar competencia para notas declaradas e data de emissao para notas avulsas, informando a semantica escolhida.

## Caminho da inscricao ate o CNAE

- Nota avulsa ate inscricao: `issnotaavulsa.q51_inscr = issbase.q02_inscr`.
- Apuracao declarada ate inscricao: `issvar.q05_numpre -> caixa.arreinscr.k00_numpre -> caixa.arreinscr.k00_inscr -> issbase.q02_inscr`.
- Inscricao ate atividade: `issbase.q02_inscr = tabativ.q07_inscr`.
- Atividade ate CNAE: `tabativ.q07_ativ = ativid.q03_ativ`.
- `ativid.q03_ativ = atividcnae.q74_ativid`.
- `atividcnae.q74_cnaeanalitica = cnaeanalitica.q72_sequencial`.
- `cnaeanalitica.q72_cnae = cnae.q71_sequencial`.
- Dimensoes de exibicao: `cnae.q71_estrutural` e `cnae.q71_descr`.

## Regra de atribuicao ao CNAE e riscos

- Regra preferencial: usar atividade ou CNAE registrado na propria nota quando a fonte municipal fornecer esse vinculo.
- O catalogo atual de `issvarnotas` e nota avulsa nao confirma CNAE diretamente gravado na nota.
- Nao relacionar uma nota a todas as atividades da inscricao; isso duplica quantidade, valor da nota e ISS.
- Sem CNAE na nota, usar a atividade principal somente como aproximacao cadastral explicitamente informada.
- Atividade principal: `ativprinc.q88_inscr = tabativ.q07_inscr` e `ativprinc.q88_seq = tabativ.q07_seq`.
- Depois da atividade principal, seguir `tabativ -> ativid -> atividcnae -> cnaeanalitica -> cnae`.
- Se nao houver atividade principal valida ou houver mais de um CNAE para a atividade, marcar a atribuicao como ambigua e nao distribuir valores automaticamente.
- Rankings por CNAE devem ordenar pela quantidade de notas e apresentar o ISS agregado no mesmo criterio de atribuicao, sem multiplicar fatos.
