## licitacao.itens_licitacao

Mapeia as consultas e regras de negocio dos itens de licitacao (`liclicitem`) e seus vinculos com processo de compras, solicitacao, julgamento, fornecedor, dotacao e acordos.

---

### Conceito: item_licitacao

- **Fonte principal:** `/var/www/html/e-cidade-php74/classes/db_liclicitem_classe.php`
- **Tabela central:** `liclicitem`
- **Chave primaria:** `l21_codigo`
- **Campos estruturantes:**
  - `l21_codliclicita` - cabecalho da licitacao em `liclicita`
  - `l21_codpcprocitem` - item do processo de compras em `pcprocitem`
- **Grau base:** Uma linha por item vinculado a uma licitacao.

`liclicitem` e a ponte entre a licitacao formal (`liclicita`) e o item originado no processo de compras (`pcprocitem`). A partir dela o sistema expande para:

- solicitacao e item solicitado;
- material, unidade e elemento;
- cotacoes/orcamentos de fornecedores;
- julgamento vencedor;
- dotacao e reserva;
- autorizacao de empenho;
- acordos posteriores.

#### Consulta: `sql_query`

- **Objetivo:** Retornar a visao base do item da licitacao com processo, solicitacao, usuario criador e configuracao do tipo de compra.
- **Tabelas:** `liclicitem`, `pcprocitem`, `liclicita`, `solicitem`, `pcproc`, `db_usuarios`, `cflicita`, `liclocal`, `liccomissao`, `solicitatipo`, `pctipocompra`
- **Juncoes principais:**
  - `pcprocitem.pc81_codprocitem = liclicitem.l21_codpcprocitem`
  - `liclicita.l20_codigo = liclicitem.l21_codliclicita`
  - `solicitem.pc11_codigo = pcprocitem.pc81_solicitem`
  - `pcproc.pc80_codproc = pcprocitem.pc81_codproc`
  - `db_usuarios.id_usuario = liclicita.l20_id_usucria`
  - `cflicita.l03_codigo = liclicita.l20_codtipocom`
  - `liclocal.l26_codigo = liclicita.l20_liclocal`
  - `liccomissao.l30_codigo = liclicita.l20_liccomissao`
- **Filtros:** aceita `l21_codigo` direto ou `dbwhere` arbitrario.
- **Cuidados:** `solicitatipo` e `pctipocompra` entram por `left join`; nem toda solicitacao precisa expor esse cadastro complementar.

#### Consulta: `sql_query_anulados`

- **Objetivo:** Expor itens com contexto suficiente para analise de anulacao, incluindo situacao da licitacao e registro em `liclicitemanu`.
- **Tabelas adicionais:** `solicita`, `db_depart`, `solicitemunid`, `matunid`, `solicitempcmater`, `pcmater`, `solicitemele`, `liclicitemanu`, `licsituacao`
- **Regra de negocio:** A consulta nao filtra apenas anulados; ela prepara o caminho para identificar anulacoes por existencia de registro em `liclicitemanu` e pela situacao da licitacao.
- **Cuidados:** para responder "item anulado", nao basta usar a consulta sem filtro; explicite a condicao sobre `liclicitemanu` ou o status desejado.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler somente `liclicitem`.
- **Uso pratico:** auditoria de chaves e base segura para reconstituir joins manualmente sem risco de multiplicacao adicional.

#### Consulta: `sql_query_inf`

- **Objetivo:** Montar a visao mais rica do item da licitacao, incluindo fornecedor orcado, julgamento, material, classificacao, autorizacao de empenho, empenho e dotacao.
- **Tabelas:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `db_depart`, `liclicita`, `cflicita`, `pctipocompra`, `solicitemunid`, `matunid`, `pcorcamitemlic`, `pcorcamval`, `pcorcamjulg`, `pcorcamforne`, `pcorcamfornelic`, `liclicitatipoempresa`, `cgm`, `db_usuarios`, `solicitempcmater`, `pcmater`, `pcsubgrupo`, `pctipo`, `solicitemele`, `orcelemento`, `empautitempcprocitem`, `empautitem`, `empautoriza`, `empempaut`, `empempenho`, `pcdotac`
- **Parametro adicional:** `lTrazerApenasVencedor`
- **Regra comprovada de vencedor:** quando `lTrazerApenasVencedor = true`, aplica `pcorcamjulg.pc24_pontuacao = 1`.
- **Regras de negocio:**
  - O caminho de compras e julgamento parte de `liclicitem -> pcorcamitemlic -> pcorcamval -> pcorcamjulg`.
  - O fornecedor do item vem de `pcorcamforne` e chega ao CGM por `pc21_numcgm = z01_numcgm`.
  - O caminho de empenho parte de `pcprocitem -> empautitempcprocitem -> empautitem -> empautoriza` e pode chegar ao numero do empenho em `empempenho`.
  - O elemento orcamentario da solicitacao usa `solicitemele.pc18_codele = orcelemento.o56_codele` no exercicio da sessao `DB_anousu`.
- **Cuidados:**
  - E a consulta mais propensa a multiplicacao de linhas, porque o mesmo item pode ter varios fornecedores orcados, varios registros de julgamento, varias dotacoes ou varios vinculos de autorizacao.
  - Para somar valores do item, defina antes se o grao desejado e `l21_codigo`, `orcamento do fornecedor`, `autorizacao` ou `empenho`.

#### Consulta: `sql_query_inf_forne`

- **Objetivo:** Retornar uma variante resumida do item com foco em autorizacao de empenho.
- **Tabelas principais:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `db_depart`, `liclicita`, `cflicita`, `pctipocompra`, `empautitempcprocitem`, `empautitem`, `empautoriza`
- **Cuidados:** apesar do nome sugerir fornecedor, esta variante observada nao percorre `pcorcamforne` nem `cgm`; ela e mais uma visao de item com cadeia de autorizacao.

#### Consulta: `sql_query_orc`

- **Objetivo:** Relacionar o item da licitacao a dotacao e orgao orcamentario da solicitacao.
- **Tabelas:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `db_depart`, `db_usuarios`, `pcdotac`, `orcdotacao`, `orcorgao`
- **Juncoes chave:**
  - `solicitem.pc11_codigo = pcdotac.pc13_codigo`
  - `pcdotac.(pc13_coddot, pc13_anousu) = orcdotacao.(o58_coddot, o58_anousu)`
  - `orcdotacao.(o58_orgao, o58_anousu) = orcorgao.(o40_orgao, o40_anousu)`
- **Regra de negocio:** a dotacao do item nao esta em `liclicitem`; ela vem da solicitacao original e do vinculo em `pcdotac`.

#### Consulta: `sql_query_proc`

- **Objetivo:** Expor o item da licitacao no contexto do processo de compras e de seus lotes.
- **Tabelas adicionais:** `processocompraloteitem`, `processocompralote`
- **Regra:** o lote do processo e opcional, por isso entra em `left join`.

#### Consulta: `sql_query_sol`

- **Objetivo:** Expor o item com o contexto mais completo da solicitacao, incluindo protocolo de processo, lote e eventual vinculo com abertura de registro de preco.
- **Tabelas adicionais:** `solicitaprotprocesso`, `processocompraloteitem`, `processocompralote`, `solicitavinculo aberturaregistropreco`
- **Regra de negocio:** o alias `aberturaregistropreco` mostra que a mesma solicitacao pode ter sido aberta a partir de um vinculo pai/filho para registro de preco.

#### Consulta: `sql_query_soljulg`

- **Objetivo:** Retornar o item com o fornecedor vencedor confirmado e eventual vinculo a acordo.
- **Tabelas principais:** `liclicita`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `db_depart`, `db_usuarios`, `pcorcamitemlic`, `pcorcamval`, `pcorcamjulg`, `pcorcamforne`, `cgm`, `cflicita`, `acordoliclicitem`
- **Regra comprovada:** sempre aplica `pc24_pontuacao = 1`, portanto devolve apenas o julgamento vencedor.
- **Cuidados:** a presença de `acordoliclicitem` por `left join` mostra que o item vencedor pode ou nao ter gerado acordo posterior.

#### Consulta: `sql_query_dotacao_reserva`

- **Objetivo:** Relacionar o item a dotacao da solicitacao e, se existir, a reserva orcamentaria correspondente.
- **Tabelas:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `pcdotac`, `orcreservasol`, `orcreserva`
- **Juncoes:**
  - `solicitem.pc11_codigo = pcdotac.pc13_codigo`
  - `pcdotac.pc13_sequencial = orcreservasol.o82_pcdotac`
  - `orcreservasol.o82_codres = orcreserva.o80_codres`
- **Regra:** a reserva e opcional; o item pode ter dotacao sem reserva formal ainda registrada.

#### Consulta: `sql_query_portal_transparencia`

- **Objetivo:** Preparar a visao do item para publicacao no portal, incluindo vencedor, classificacao do material, elemento e atributos dinamicos da licitacao.
- **Tabelas adicionais:** `liclicitacadattdinamicovalorgrupo`, `db_cadattdinamicoatributosvalor`
- **Regra de vencedor observada:** o julgamento e amarrado com `pcorcamjulg.pc24_pontuacao = 1`, depois o valor do fornecedor e recuperado em `pcorcamval`.
- **Regra de exercicio do elemento:** `orcelemento.o56_anousu = extract(year from pc10_data)`, ou seja, o elemento vem do ano da solicitacao, nao da sessao.
- **Cuidados:** os atributos dinamicos entram em `inner join`; se a licitacao nao tiver esse cadastro, ela nao aparece nessa receita.

#### Consulta: `sql_query_licitacao_compilacao`

- **Objetivo:** Receita enxuta para compilar informacoes basicas de item, processo, solicitacao e licitacao.
- **Tabelas:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `liclicita`
- **Uso pratico:** boa base para relatorios sinteticos e compilacoes sem expandir julgamento, fornecedor ou dotacao.

#### Consulta: `sql_query_acordos`

- **Objetivo:** Listar acordos vinculados ao item da licitacao.
- **Tabelas:** `liclicitem`, `acordoliclicitem`, `acordoitem`, `acordoposicao`, `acordo`, `liclicita`
- **Regra de negocio:** o item de licitacao pode desdobrar acordos por meio do encadeamento `acordoliclicitem -> acordoitem -> acordoposicao -> acordo`.

#### Consulta: `sql_query_valor_estimado`

- **Objetivo:** Recuperar o caminho do valor estimado/orcado do item no processo.
- **Tabelas:** `liclicitem`, `pcprocitem`, `pcproc`, `solicitem`, `solicita`, `liclicita`, `pcorcamitemproc`, `pcorcamitem`, `pcorcamval`, `pcorcamforne`, `pcorcamjulg`, `liclicitemlote`
- **Regra:** usa o caminho `l21_codpcprocitem -> pcorcamitemproc -> pcorcamitem -> pcorcamval`.
- **Cuidados:** como tudo entra por `left join`, um item pode existir sem valor estimado completo ou sem lote associado.

#### Consulta: `sql_query_item_licitacon`

- **Objetivo:** Preparar o item para integracao LicitaCon.
- **Tabelas principais:** `liclicitem`, `pcorcamitemlic`, `pcorcamitem`, `pcorcamjulg`, `pcorcamval`, `pcorcamforne`, `cgm`, `pcprocitem`, `solicitem`, `solicitempcmater`, `pcmater`, `solicitemunid`, `matunid`, `liclicita`, `cflicita`, `pctipocompratribunal`, `liclicitaencerramentolicitacon`, `liclicitemlote`, `liclicitacadattdinamicovalorgrupo`
- **Regra comprovada de vencedor:** `pc24_pontuacao = 1`.
- **Regra de negocio:** a classificacao para tribunal depende do tipo de compra em `pctipocompratribunal`, e o encerramento do envio pode existir ou nao em `liclicitaencerramentolicitacon`.

#### Consulta: `sql_itens_fornecedores`

- **Objetivo:** Listar licitacoes com fornecedor vencedor, excluindo aquelas que ja geraram autorizacao de empenho ativa.
- **Estrutura:** usa duas CTEs, `cte_licitacoes` e `cte_licitacao_autoriza`.
- **Regras comprovadas:**
  - na CTE principal, o vencedor e filtrado por `pcorcamjulg.pc24_pontuacao = 1`;
  - a licitacao e restringida a `liclicita.l20_instit = db_getsession('DB_instit')`;
  - a CTE de autorizacao considera apenas `empautoriza.e54_anulad is null`;
  - o resultado final mantem apenas `where cla.l20_codigo is null`.
- **Regra de negocio:** a consulta procura itens/licitacoes vencedores que ainda nao foram convertidos em autorizacao ativa de empenho.
- **Cuidados:** o metodo ignora os parametros `l21_codigo`, `ordem` e usa `dbwhere` como obrigatorio dentro da primeira CTE.

#### Consulta: `sql_itens_fornecedores_licitacao`

- **Objetivo:** Variacao da consulta anterior mais enxuta, ainda focada em licitacoes vencedoras sem autorizacao ativa.
- **Diferença principal:** remove varios joins auxiliares do item e preserva o nucleo vencedor + autorizacao.
- **Cuidados:** vale a mesma regra de exclusao por autorizacao nao anulada e a mesma dependencia do `dbwhere` informado.

#### Consulta: `sql_itens_solicita_pai`

- **Objetivo:** Recuperar itens de licitacao a partir da solicitacao pai vinculada.
- **Tabelas:** `liclicitem`, `pcprocitem`, `solicitem`, `solicitavinculo`
- **Regra:** usa `solicitavinculo.pc53_solicitafilho = solicitem.pc11_numero`, permitindo subir da solicitacao filha para o contexto pai.
- **Cuidado importante:** se `where` ou `campos` vierem vazios, o metodo retorna string vazia em vez de SQL.

#### Consulta: `sqlItensSemVencedor`

- **Objetivo:** Identificar itens da licitacao ainda sem vencedor marcado.
- **Tabelas:** `liclicitem`, `pcorcamitemlic`, `pcorcamitem`, `pcorcamjulg`
- **Regra comprovada:** o join do vencedor usa `pc24_pontuacao = 1`.
- **Como usar:** filtre `pc24_orcamitem is null` ou equivalente no `where` para encontrar itens sem vencedor efetivo.
- **Cuidados:** o metodo por si so nao exclui vencedores; ele apenas monta o caminho via `left join`.

#### Cuidados para consultas do agente

- O grao mais seguro para contagem de itens e `liclicitem.l21_codigo`.
- Quase todas as consultas que passam por `pcorcamval`, `pcorcamjulg` e `pcorcamforne` podem multiplicar o item por fornecedor/orcamento.
- A regra de vencedor observada na classe e consistente: `pcorcamjulg.pc24_pontuacao = 1`.
- Dotacao, reserva, autorizacao e empenho nao sao atributos nativos do item; eles entram por vinculos laterais da solicitacao e do processo.
- Consultas de portal e LicitaCon adicionam exigencias extras de cadastro dinamico e classificacao de tribunal; nao reutilize essas receitas como base neutra para analise geral.
