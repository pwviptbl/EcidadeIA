## caixa.arrecadacao_e_pagamentos

> Fonte manual: `knowledge/manual/caixa/arrecadacao_e_pagamentos.md`

Mapeia as relações financeiras da arrecadação e caixa, incluindo os vínculos com contribuintes (CGM), imóveis (matrículas), empresas (inscrições), e as classificações de tipos e grupos de débitos.

---

### Conceito: vinculo_cgm
- **Descrição:** Vínculo base de débitos com o Cadastro Geral de Contribuintes (CGM) do contribuinte correspondente.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arrenumcgm`, `protocolo.cgm`
- **Junções:**
  - `arrecad.k00_numpre = arrenumcgm.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arrenumcgm.k00_numpre` (para pagamentos)
  - `arrenumcgm.k00_numcgm = cgm.z01_numcgm`

#### Detalhamento da tabela `arrenumcgm`

> Fonte: `/var/www/html/e-cidade-php74/classes/db_arrenumcgm_classe.php`
>
> Classe: `cl_arrenumcgm`

`arrenumcgm` é a tabela de vínculo entre um número de arrecadação e um CGM.

- **Chave primária composta:** `k00_numpre`, `k00_numcgm`.
- **Grão:** Uma linha por vínculo entre um débito identificado por `numpre` e um CGM.
- **Chave estrangeira confirmada:** `arrenumcgm.k00_numcgm = cgm.z01_numcgm`.
- **Coluna de tempo:** A tabela não possui data própria.

O relacionamento é potencialmente muitos-para-muitos:

- um CGM pode estar associado a vários `numpres`;
- um `numpre` pode estar associado a vários CGMs.

O recibo de ITBI, por exemplo, inclui o CGM devedor e pode incluir outros CGMs participantes no mesmo `numpre`. As rotinas de transferência de débito também podem manter o CGM de origem e adicionar o destino quando a opção de transferir a origem não é escolhida.

Portanto, `arrenumcgm` não garante que o CGM encontrado seja o único contribuinte ou o devedor principal.

#### Consulta: `sql_query`

- **Objetivo:** Recuperar os vínculos com os dados cadastrais dos CGMs.
- **Grão:** Uma linha por par `numpre` e CGM.

```sql
select /* campos dinâmicos */
  from arrenumcgm
       inner join cgm
          on cgm.z01_numcgm = arrenumcgm.k00_numcgm
 where arrenumcgm.k00_numcgm = :cgm
   and arrenumcgm.k00_numpre = :numpre
 order by /* ordenação dinâmica */
```

Regras:

- O CGM é obrigatório devido ao `inner join`.
- É possível filtrar somente pelo CGM, somente pelo `numpre` ou pelos dois.
- Para listar todos os CGMs de um débito, filtre apenas `k00_numpre`.
- Para listar todos os débitos vinculados a uma pessoa, filtre apenas `k00_numcgm`.
- A consulta não informa se o débito está aberto, pago, cancelado, suspenso ou inscrito em dívida.

#### Consulta: `sql_query_deb`

- **Objetivo:** Recuperar débitos abertos associados ao CGM.
- **Tabelas:** `arrenumcgm`, `cgm`, `arrecad`.

```sql
select /* campos dinâmicos */
  from arrenumcgm
       inner join cgm
          on cgm.z01_numcgm = arrenumcgm.k00_numcgm
       inner join arrecad
          on arrecad.k00_numpre = arrenumcgm.k00_numpre
 where arrenumcgm.k00_numcgm = :cgm
   and arrenumcgm.k00_numpre = :numpre
 order by /* ordenação dinâmica */
```

Cardinalidade:

- O join com `arrecad` usa somente `k00_numpre`.
- Como `arrecad` possui parcelas em `k00_numpar`, um vínculo de `arrenumcgm` pode gerar várias linhas, uma para cada parcela aberta.
- Uma linha do resultado representa uma combinação de CGM e parcela do débito, não apenas um CGM ou um `numpre`.
- Para contar débitos, use `count(distinct arrenumcgm.k00_numpre)`.
- Para contar parcelas abertas, use a combinação distinta de `arrecad.k00_numpre` e `arrecad.k00_numpar`.

O `inner join arrecad` restringe o resultado aos `numpres` ainda presentes na tabela de débitos abertos. Para pagamentos, relacione `arrenumcgm` a `arrepaga`; para outras situações, use a tabela de estado correspondente.

#### Consulta: `sql_query_file`

Consulta somente a tabela de vínculo:

```sql
select /* campos dinâmicos */
  from arrenumcgm
 where arrenumcgm.k00_numcgm = :cgm
   and arrenumcgm.k00_numpre = :numpre
```

É a forma mais direta para:

- confirmar se um vínculo específico existe;
- listar os CGMs de um `numpre`;
- listar os `numpres` de um CGM;
- evitar multiplicação por parcelas de `arrecad`.

#### Regra: `incluir_se_nao_existir`

O método consulta primeiro a chave composta:

```sql
select *
  from arrenumcgm
 where k00_numcgm = :cgm
   and k00_numpre = :numpre
```

Se não encontrar linha, insere o vínculo. Se já existir, não grava duplicidade e define o estado interno como sucesso.

Usos confirmados:

- emissão de recibo de ITBI;
- geração de vínculo para débitos de ISS e fiscalização;
- transferência de débito entre CGM, matrícula e inscrição;
- inclusão de todos os CGMs encontrados na origem cadastral de destino.

Essa regra evita duplicação do mesmo par, mas não impede vários CGMs diferentes no mesmo `numpre`.

#### Diferença entre `arrenumcgm.k00_numcgm` e `arrecad.k00_numcgm`

Algumas rotinas de transferência atualizam `arrecad.k00_numcgm` e também mantêm os vínculos em `arrenumcgm`.

Interpretação segura:

- `arrecad.k00_numcgm` é um campo único na parcela do débito aberto;
- `arrenumcgm` preserva uma coleção de CGMs relacionados ao `numpre`;
- as duas fontes podem divergir durante transferências, manutenção histórica ou quando há múltiplos envolvidos.

Quando a pergunta exigir o responsável principal da parcela, avalie `arrecad.k00_numcgm`. Quando exigir todos os CGMs relacionados ao débito, use `arrenumcgm`.

#### Cuidados para consultas do agente

- Filtre por instituição por meio de `arreinstit` ou da entidade financeira adequada; `arrenumcgm` não possui coluna de instituição.
- Não some valores após juntar um mesmo `numpre` a vários CGMs sem controlar duplicidade.
- Para total financeiro por CGM, defina se o valor deve ser atribuído integralmente a cada envolvido ou rateado. A tabela não possui percentual.
- Não use `arrenumcgm` isoladamente para concluir situação do débito.
- Para pagamentos, o join com `arrepaga` também pode multiplicar por parcela e movimento de pagamento.
- Nome e documento devem vir de `cgm`; `arrenumcgm` armazena somente os identificadores.
- Os métodos legados concatenam filtros, campos e ordenação. Novas consultas devem usar parâmetros vinculados e allowlist de colunas.

---

### Conceito: historico_origem_parcelamento
- **Descricao:** Historico do debito original que saiu do fluxo normal da arrecadacao e passou a ser tratado como origem de parcelamento ou divida.
- **Tabelas:** `caixa.arreold`, `protocolo.cgm`, `arrecadacao.histcalc`, `configuracao.tabrec`, `caixa.arretipo`, `configuracao.tabrecjm`, `configuracao.db_config`, `caixa.cadtipo`

#### Detalhamento da tabela `arreold`

> Fonte: `/var/www/html/e-cidade-php74/classes/db_arreold_classe.php`
>
> Classe: `cl_arreold`

`arreold` guarda uma copia historica do debito antigo.

Evidencias de uso no codigo:

- `db_arrecad_classe.php` copia linhas de `arrecad` para `arreold` e em seguida pode excluir o mesmo `numpre` de `arrecad`.
- `db_declaracaoquitacao_classe.php` rotula registros de `arreold` como `Parcelado Divida`.
- `db_certid_classe.php` e `db_termodiv_classe.php` usam `arreold` como origem do termo e da certidao do parcelamento.

Interpretacao segura:

- `arrecad` representa o debito aberto atual.
- `arreold` representa a origem historica daquele debito quando ele entrou em fluxo de parcelamento/divida.
- A tabela nao substitui `arrecad` para saldo atual nem `arrepaga` para quitacao.

Grau seguro do registro:

- uma linha por componente historico do debito antigo;
- na pratica, as rotinas consumidoras relacionam `arreold` por `k00_numpre`, `k00_numpar` e `k00_receit`;
- portanto, um mesmo `numpre` pode ter varias linhas por parcela e receita.

#### Consulta: `sql_query`

- **Objetivo:** Recuperar o debito historico antigo com enriquecimento de contribuinte, historico de calculo, receita, tipo e instituicao.
- **Grau do resultado:** Uma linha por componente historico de `arreold`, sujeito aos joins obrigatorios.

```sql
select /* campos dinamicos */
  from arreold
       inner join cgm
          on cgm.z01_numcgm = arreold.k00_numcgm
       inner join histcalc
          on histcalc.k01_codigo = arreold.k00_hist
       inner join tabrec
          on tabrec.k02_codigo = arreold.k00_receit
       inner join arretipo
          on arretipo.k00_tipo = arreold.k00_tipo
       inner join tabrecjm
          on tabrecjm.k02_codjm = tabrec.k02_codjm
       inner join db_config
          on db_config.codigo = arretipo.k00_instit
       inner join cadtipo
          on cadtipo.k03_tipo = arretipo.k03_tipo
 where arreold.oid = :oid
 order by /* ordenacao dinamica */
```

Regras observadas:

- O `inner join cgm` exige `k00_numcgm` valido.
- O tipo do debito vem de `arretipo`, e o grupo macro vem de `cadtipo`.
- A instituicao vem de `arretipo.k00_instit -> db_config.codigo`, nao de uma coluna propria em `arreold`.
- `tabrecjm` indica que a receita carrega configuracao de juros e multa por meio de `tabrec.k02_codjm`.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler apenas os campos fisicos de `arreold`, sem enriquecimento.

```sql
select /* campos dinamicos */
  from arreold
 where /* filtro dinamico opcional */
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar existencia de um debito historico antigo;
- listar origens antigas por `numpre`, `parcela` ou `receita`;
- evitar multiplicacao causada pelos joins de `sql_query`.

#### Consulta: `sql_query_getReceitasTipo`

- **Objetivo:** Descobrir receitas de origem de parcelamentos de `diversos` ainda vinculadas ao ultimo parcelamento ativo.
- **Tabelas:** `arreold`, `diversos`, `termodiver`, `termo`, `tabrec`, `arreinstit`, `arrecad`.
- **Parametros implicitos:** `DB_instit`.
- **Grau do resultado:** Uma linha distinta por descricao de receita e codigo de receita.

```sql
select distinct
       k02_descr,
       x.k00_receit
  from (
        select k02_descr,
               k00_receit,
               (
                 select riparcel
                   from fc_parc_origem_completo(termo.v07_numpre)
                  where riseq = 1
               ) as ultimo_parcelamento
          from arreold
               inner join diversos
                  on diversos.dv05_numpre = arreold.k00_numpre
               inner join termodiver
                  on termodiver.dv10_coddiver = diversos.dv05_coddiver
               inner join termo
                  on termo.v07_parcel = termodiver.dv10_parcel
               inner join tabrec
                  on tabrec.k02_codigo = arreold.k00_receit
               natural join arreinstit
         where arreinstit.k00_instit = :instituicao
       ) as x
       inner join termo
          on termo.v07_parcel = x.ultimo_parcelamento
       inner join arrecad
          on arrecad.k00_numpre = termo.v07_numpre
 where termo.v07_situacao = 1
```

Regras comprovadas:

- Parte apenas de debitos antigos de `diversos`.
- O filtro institucional usa `arreinstit` na etapa interna.
- A funcao `fc_parc_origem_completo(termo.v07_numpre)` identifica a cadeia de origem do parcelamento e seleciona apenas `riseq = 1`.
- A consulta externa exige que o ultimo parcelamento encontrado tenha termo com `v07_situacao = 1`.
- O `inner join arrecad` no `v07_numpre` restringe o resultado a parcelamentos cujo debito correspondente ainda esta no saldo aberto.

Cuidados:

- O metodo retorna somente `k02_descr` e `k00_receit`, entao nao serve para totalizar valores.
- `natural join arreinstit` depende de colunas homonimas e deve ser reescrito explicitamente em consultas novas.
- A semantica exata de `v07_situacao = 1` nao esta definida nesta classe; a interpretacao segura e apenas "situacao aceita pela rotina de parcelamento".
- A funcao `fc_parc_origem_completo` introduz logica adicional fora desta classe; aqui so e seguro afirmar que ela navega a origem do parcelamento.

#### Cuidados para consultas do agente

- Nao trate `arreold` como debito aberto atual; para saldo presente, confirme em `arrecad`.
- Nao trate `arreold` como pagamento; para quitacao, confirme em `arrepaga`.
- Para parcelamentos e divida, relacione tambem `termodiv`, `termo`, `divida` ou `arreoldcalc` conforme a pergunta.
- Se a pergunta for sobre valor atualizado, `arreold.k00_valor` e historico; juros, multa, correcao e desconto podem estar em `arreoldcalc`.
- Como a instituicao vem por `arretipo` ou `arreinstit` conforme a consulta, nao assuma um unico caminho sem validar o metodo usado.

---

### Conceito: vinculo_matricula
- **Descrição:** Vínculo base de débitos (como IPTU e taxas imobiliárias) com a matrícula do imóvel no Cadastro Imobiliário Municipal.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arrematric`, `cadastro.iptubase`
- **Junções:**
  - `arrecad.k00_numpre = arrematric.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arrematric.k00_numpre` (para pagamentos)
  - `arrematric.k00_matric = iptubase.j01_matric`

#### Detalhamento da tabela `arrematric`

> Fonte: `/var/www/html/e-cidade-php74/classes/db_arrematric_classe.php`
>
> Classe: `cl_arrematric`

`arrematric` vincula um numero de arrecadacao a uma matricula imobiliaria e registra um percentual associado ao debito.

- **Chave pratica observada:** `k00_numpre`, `k00_matric`.
- **Grau:** Uma linha por vinculo entre um `numpre` e uma matricula.
- **Percentual:** `k00_perc` representa o percentual da matricula em relacao ao debito.

Interpretacao segura:

- um `numpre` pode ter mais de uma matricula vinculada;
- uma matricula pode aparecer em varios `numpres`;
- quando existe mais de uma linha para o mesmo debito, o resultado deixa de ser "um debito por matricula" e passa a ser "um vinculo matricula x debito".

#### Consulta: `sql_query`

- **Objetivo:** Recuperar o vinculo da matricula com dados cadastrais do imovel, lote e CGM principal do cadastro imobiliario.
- **Tabelas:** `arrematric`, `iptubase`, `lote`, `cgm`.
- **Grau do resultado:** Uma linha por vinculo `numpre` x matricula.

```sql
select /* campos dinamicos */
  from arrematric
       inner join iptubase
          on iptubase.j01_matric = arrematric.k00_matric
       inner join lote
          on lote.j34_idbql = iptubase.j01_idbql
       inner join cgm
          on cgm.z01_numcgm = iptubase.j01_numcgm
 where arrematric.k00_numpre = :numpre
   and arrematric.k00_matric = :matricula
 order by /* ordenacao dinamica */
```

Regras observadas:

- O `inner join iptubase` exige que a matricula exista no cadastro imobiliario.
- O `inner join lote` enriquece a localizacao fiscal do imovel por `iptubase.j01_idbql`.
- O `inner join cgm` retorna o CGM principal do cadastro imobiliario por `iptubase.j01_numcgm`.
- A consulta nao informa situacao financeira do debito; ela so resolve o caminho `numpre -> matricula -> cadastro imobiliario`.

#### Consulta: `sql_query_div`

- **Objetivo:** Relacionar o vinculo da matricula a debitos que ja aparecem na divida e ainda possuem parcela em `arrecad`.
- **Tabelas:** `arrematric`, `divida`, `arrecad`, `arretipo`, `cadtipo`.

```sql
select /* campos dinamicos */
  from arrematric
       inner join divida
          on divida.v01_numpre = arrematric.k00_numpre
       inner join arrecad
          on arrecad.k00_numpre = divida.v01_numpre
         and arrecad.k00_numpar = divida.v01_numpar
       inner join arretipo
          on arretipo.k00_tipo = arrecad.k00_tipo
       inner join cadtipo
          on cadtipo.k03_tipo = arretipo.k03_tipo
 where arrematric.k00_numpre = :numpre
   and arrematric.k00_matric = :matricula
 order by /* ordenacao dinamica */
```

Regra comprovada:

- O debito precisa existir em `divida` e a parcela correspondente precisa continuar em `arrecad`.

Cardinalidade:

- Como o join com `arrecad` usa `numpre + numpar` vindos de `divida`, o grao tende a ser uma linha por vinculo de matricula e parcela da divida.

#### Consulta: `sql_query_info`

- **Objetivo:** Recuperar informacoes de debitos abertos vinculados a matricula sem passar por `divida`.
- **Tabelas:** `arrematric`, `arrecad`, `arretipo`, `cadtipo`.

```sql
select /* campos dinamicos */
  from arrematric
       inner join arrecad
          on arrecad.k00_numpre = arrematric.k00_numpre
       inner join arretipo
          on arretipo.k00_tipo = arrecad.k00_tipo
       inner join cadtipo
          on cadtipo.k03_tipo = arretipo.k03_tipo
 where arrematric.k00_numpre = :numpre
   and arrematric.k00_matric = :matricula
 order by /* ordenacao dinamica */
```

Cardinalidade:

- O join com `arrecad` usa apenas `k00_numpre`.
- Como `arrecad` possui parcelas em `k00_numpar`, um unico vinculo de `arrematric` pode gerar varias linhas, uma para cada parcela aberta.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler apenas a tabela fisica `arrematric`.

```sql
select /* campos dinamicos */
  from arrematric
 where arrematric.k00_numpre = :numpre
   and arrematric.k00_matric = :matricula
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar se um debito esta vinculado a uma matricula;
- listar todas as matriculas de um `numpre`;
- listar todos os `numpres` de uma matricula;
- ler `k00_perc` sem multiplicacao por parcelas.

#### Regra de percentual: `k00_perc`

Evidencias complementares no codigo:

- `db_arrepaga_classe.php` usa `arrematric.k00_perc` como `percentual_origem` quando ha vinculo por matricula.
- `db_arrematric_classe.php` inicializa `k00_perc = 0` quando o valor nao e informado na inclusao.

Interpretacao segura:

- quando o vinculo por matricula existe, o percentual pode ser usado para ratear o valor historico entre origens;
- quando nao existe vinculo por matricula nem por inscricao, outras rotinas assumem `100` como percentual de origem;
- `0` em `k00_perc` nao significa automaticamente "sem efeito"; significa apenas que a linha foi gravada assim e a interpretacao final depende da rotina consumidora.

#### Evidencia adicional de uso

- `db_certid_classe.php` usa `arrematric` para decidir se a origem do debito e imobiliaria e para recuperar uma matricula associada ao `numpre`.
- `db_recibounicageracao_classe.php` relaciona `arrematric.k00_numpre` a `iptunump.j20_numpre`, reforcando o uso como ponte entre arrecadacao e cadastro imobiliario.

#### Cuidados para consultas do agente

- Nao some valores de `arrecad` ou `arrepaga` apos juntar `arrematric` sem decidir se o percentual deve ser aplicado.
- Para listar debitos em aberto por matricula, prefira controlar a entidade contada: `numpre`, `numpre + numpar` ou vinculo `numpre + matricula`.
- `sql_query_info` nao passa por `divida`; `sql_query_div` passa. Escolha conforme a pergunta exigir debito aberto geral ou debito ja inscrito em divida.
- Para situacao cadastral do imovel, `arrematric` sozinho nao informa matricula ativa ou baixada; valide em `iptubase` e, se necessario, em `j01_baixa`.

---

### Conceito: vinculo_inscricao
- **Descrição:** Vínculo de débitos (como ISSQN, taxas de alvará e tributos mobiliários) com a inscrição da empresa/atividade econômica no Cadastro Mobiliário Municipal.
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arreinscr`, `issqn.issbase`
- **Junções:**
  - `arrecad.k00_numpre = arreinscr.k00_numpre` (para débitos em aberto) ou `arrepaga.k00_numpre = arreinscr.k00_numpre` (para pagamentos)
  - `arreinscr.k00_inscr = issbase.q02_inscr`

#### Detalhamento da tabela `arreinscr`

> Fonte: `/var/www/html/e-cidade-php74/classes/db_arreinscr_classe.php`
>
> Classe: `cl_arreinscr`

`arreinscr` vincula um numero de arrecadacao a uma inscricao mobiliaria e registra um percentual associado ao debito.

- **Chave pratica observada:** `k00_numpre`, `k00_inscr`.
- **Grau:** Uma linha por vinculo entre um `numpre` e uma inscricao.
- **Percentual:** `k00_perc` representa o percentual da inscricao em relacao ao debito.

Interpretacao segura:

- um `numpre` pode ter mais de uma inscricao vinculada;
- uma inscricao pode aparecer em varios `numpres`;
- quando existe mais de uma linha para o mesmo debito, o resultado deixa de ser "um debito por inscricao" e passa a ser "um vinculo inscricao x debito".

#### Consulta: `sql_query`

- **Objetivo:** Recuperar o vinculo da inscricao com dados cadastrais da empresa e do CGM principal.
- **Tabelas:** `arreinscr`, `issbase`, `cgm`.
- **Grau do resultado:** Uma linha por vinculo `numpre` x inscricao.

```sql
select /* campos dinamicos */
  from arreinscr
       inner join issbase
          on issbase.q02_inscr = arreinscr.k00_inscr
       inner join cgm
          on cgm.z01_numcgm = issbase.q02_numcgm
 where arreinscr.k00_numpre = :numpre
   and arreinscr.k00_inscr = :inscricao
 order by /* ordenacao dinamica */
```

Regras observadas:

- O `inner join issbase` exige que a inscricao exista no cadastro mobiliario.
- O `inner join cgm` retorna o CGM principal da empresa por `issbase.q02_numcgm`.
- A consulta nao informa situacao financeira do debito; ela so resolve o caminho `numpre -> inscricao -> cadastro da empresa`.

#### Consulta: `sql_query_arrecad`

- **Objetivo:** Recuperar inscricoes associadas a debitos ainda abertos.
- **Tabelas:** `arreinscr`, `issbase`, `cgm`, `arrecad`, `arretipo`.

```sql
select /* campos dinamicos */
  from arreinscr
       inner join issbase
          on issbase.q02_inscr = arreinscr.k00_inscr
       inner join cgm
          on cgm.z01_numcgm = issbase.q02_numcgm
       inner join arrecad
          on arrecad.k00_numpre = arreinscr.k00_numpre
       inner join arretipo
          on arretipo.k00_tipo = arrecad.k00_tipo
 where arreinscr.k00_numpre = :numpre
   and arreinscr.k00_inscr = :inscricao
 order by /* ordenacao dinamica */
```

Cardinalidade:

- O join com `arrecad` usa apenas `k00_numpre`.
- Como `arrecad` possui parcelas em `k00_numpar`, um unico vinculo de `arreinscr` pode gerar varias linhas, uma para cada parcela aberta.
- Uma linha do resultado representa a combinacao de inscricao e parcela em aberto, nao apenas a inscricao.

Regra comprovada:

- O `inner join arrecad` restringe o resultado aos debitos que ainda permanecem em aberto.

#### Consulta: `sql_query_file`

- **Objetivo:** Ler apenas a tabela fisica `arreinscr`.

```sql
select /* campos dinamicos */
  from arreinscr
 where arreinscr.k00_numpre = :numpre
   and arreinscr.k00_inscr = :inscricao
 order by /* ordenacao dinamica */
```

Uso seguro:

- confirmar se um debito esta vinculado a uma inscricao;
- listar todas as inscricoes de um `numpre`;
- listar todos os `numpres` de uma inscricao;
- ler `k00_perc` sem multiplicacao por parcelas.

#### Regra de percentual: `k00_perc`

Evidencias complementares no codigo:

- `db_arrepaga_classe.php` usa `arreinscr.k00_perc` como `percentual_origem` quando ha vinculo por inscricao.
- `db_arreinscr_classe.php` inicializa `k00_perc = 0` quando o valor nao e informado na inclusao.

Interpretacao segura:

- quando o vinculo por inscricao existe, o percentual pode ser usado para ratear o valor historico entre origens;
- quando nao existe vinculo por inscricao nem por matricula, outras rotinas assumem `100` como percentual de origem;
- `0` em `k00_perc` nao significa automaticamente "sem efeito"; significa apenas que a linha foi gravada assim e a interpretacao final depende da rotina consumidora.

#### Evidencia adicional de uso

- `db_issvar_classe.php` relaciona `issvar.q05_numpre = arreinscr.k00_numpre` para conectar apuracoes de ISS a inscricoes mobiliarias.
- Nesses joins, `arreinscr` funciona como ponte entre o debito financeiro e a inscricao da empresa.

#### Cuidados para consultas do agente

- Nao some valores de `arrecad` ou `arrepaga` apos juntar `arreinscr` sem decidir se o percentual deve ser aplicado.
- Para listar debitos em aberto por inscricao, prefira controlar a entidade contada: `numpre`, `numpre + numpar` ou vinculo `numpre + inscricao`.
- O join de `sql_query_arrecad` nao amarra parcela nem receita; ele serve para situacao aberta do debito, nao para identificar um componente financeiro especifico.
- Para situacao cadastral da empresa, consulte tambem `issbase.q02_dtbaix`; `arreinscr` sozinho nao informa se a inscricao esta ativa ou baixada.

---

---

### Conceito: debito_aberto_arrecad

- **Descricao:** Estado corrente do debito em aberto no caixa, por numero de arrecadacao, parcela, receita e tipo.
- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_arrecad_classe.php`
- **Tabelas:** `caixa.arrecad`, `caixa.arreinstit`, `protocolo.cgm`, `arrecadacao.histcalc`, `configuracao.tabrec`, `caixa.arretipo`, `configuracao.tabrecjm`, `caixa.cadtipo`
- **Chave pratica observada:** `k00_numpre`, `k00_numpar`, `k00_receit`
- **Grao base:** Uma linha por componente financeiro em aberto de um `numpre`, normalmente separado por parcela e receita.

`arrecad` e a tabela principal do saldo devedor corrente. Cada linha representa um componente financeiro ainda aberto, com valor em `k00_valor`, vencimento em `k00_dtvenc`, historico de calculo em `k00_hist`, receita em `k00_receit` e classificacao do debito em `k00_tipo`.

- um mesmo `numpre` pode ter varias parcelas em `k00_numpar`;
- uma mesma parcela pode ter varias receitas;
- o campo `k00_numcgm` guarda um CGM principal da linha, mas outros CGMs relacionados podem existir em `arrenumcgm`.

#### Consulta: `sql_query`

- **Objetivo:** Montar a visao mais completa do debito em aberto com instituicao, contribuinte principal, historico, receita, tipo e grupo.
- **Tabelas:** `arrecad`, `arreinstit`, `cgm`, `histcalc`, `tabrec`, `arretipo`, `tabrecjm`, `cadtipo`
- **Grau do resultado:** Uma linha por linha existente em `arrecad`, desde que o `numpre` esteja vinculado em `arreinstit`.
- **Parametros dinamicos:** `:campos`, `:ordem`, `:dbwhere`, `:oid`
- **Juncoes:**
  - `arreinstit.k00_numpre = arrecad.k00_numpre`
  - `cgm.z01_numcgm = arrecad.k00_numcgm`
  - `histcalc.k01_codigo = arrecad.k00_hist`
  - `tabrec.k02_codigo = arrecad.k00_receit`
  - `arretipo.k00_tipo = arrecad.k00_tipo`
  - `tabrecjm.k02_codjm = tabrec.k02_codjm`
  - `cadtipo.k03_tipo = arretipo.k03_tipo`
- **Filtros e regras:**
  - Quando `dbwhere` nao e informado, o metodo so filtra por `arrecad.oid` se `oid` vier preenchido.
  - O join com `arreinstit` mostra que o debito pertence ao caixa de uma instituicao, mas o filtro da instituicao precisa ser passado em `dbwhere`.
- **Cuidados:**
  - O metodo nao aplica `distinct`; qualquer duplicidade em joins auxiliares impacta a contagem final.
  - Como o join com `arreinstit` usa apenas `k00_numpre`, trate o `numpre` como cabecalho institucional e a linha de `arrecad` como detalhe financeiro.

#### Consulta: `sql_query_div`

- **Objetivo:** Relacionar debitos em aberto com registros ja presentes em `divida`.
- **Tabelas:** `arrecad`, `arreinstit`, `divida`, `arretipo`, `cadtipo`
- **Juncoes:**
  - `arreinstit.k00_numpre = arrecad.k00_numpre`
  - `arrecad.k00_numpre = divida.v01_numpre`
  - `arrecad.k00_numpar = divida.v01_numpar`
  - `arretipo.k00_tipo = arrecad.k00_tipo`
  - `cadtipo.k03_tipo = arretipo.k03_tipo`
- **Regra:** A linha so aparece quando a mesma parcela continua aberta em `arrecad` e tambem existe em `divida`.
- **Cuidados:** O metodo nao usa `k00_receit` na ligacao com `divida`; se uma parcela tiver mais de uma receita em `arrecad`, o join continua no grao do detalhe financeiro da arrecadacao.

#### Consulta: `sql_query_info`

- **Objetivo:** Expor o debito em aberto junto com possiveis vinculos de CGM adicional, inscricao mobiliaria e matricula.
- **Tabelas:** `arrecad`, `arreinstit`, `arretipo`, `cadtipo`, `arrenumcgm`, `arreinscr`, `arrematric`
- **Juncoes:**
  - `arreinstit.k00_numpre = arrecad.k00_numpre`
  - `arretipo.k00_tipo = arrecad.k00_tipo`
  - `cadtipo.k03_tipo = arretipo.k03_tipo`
  - `arrenumcgm.k00_numpre = arrecad.k00_numpre`
  - `arreinscr.k00_numpre = arrecad.k00_numpre`
  - `arrematric.k00_numpre = arrecad.k00_numpre`
- **Regra:** Os vinculos complementares entram por `left join`, portanto podem nao existir.
- **Cuidados:**
  - Esse metodo e propenso a multiplicacao de linhas quando o mesmo `numpre` tiver mais de um CGM, mais de uma inscricao ou mais de uma matricula.
  - Nao some `k00_valor` diretamente apos esse join sem normalizar a entidade contada.

#### Consulta: `sql_query_arrecad`

- **Objetivo:** Retornar o debito aberto com classificacao fiscal, sem trazer historico, receita ou contribuinte.
- **Tabelas:** `arrecad`, `arreinstit`, `arretipo`, `cadtipo`
- **Uso pratico:** Base enxuta para listar debitos em aberto por tipo ou grupo, quando nao for necessario detalhar `tabrec`, `histcalc` ou `cgm`.

#### Consulta: `sql_query_file` e `sql_query_file_instit`

- **Objetivo:** Recuperar linhas de `arrecad` com pouca ou nenhuma expansao de joins.
- **Regra:**
  - `sql_query_file` consulta somente `arrecad`.
  - `sql_query_file_instit` acrescenta `arreinstit`.
- **Cuidados:** Sao consultas mais seguras para auditoria de chaves e confronto de totais, porque reduzem o risco de multiplicacao por joins auxiliares.

#### Consulta: `sql_query_buscaDesconto`

- **Objetivo:** Listar descontos do `numpre` atual, tanto os ainda abertos quanto os ja movidos para historico anterior.
- **Tabelas:** `arrecad`, `arrecant`, `arrepaga`, `tabrec`, `arreinstit`
- **Filtros e regras:**
  - Considera somente linhas com `k00_hist = 918`.
  - Restringe o resultado a `arreinstit.k00_instit = db_getsession("DB_instit")`.
  - Une dois estados:
    - `tipo = 'a'`: desconto ainda em `arrecad`, com `k00_dtpaga = null`;
    - `tipo = 'r'`: desconto ja saiu de `arrecad`, esta em `arrecant`, e continua sem pagamento em `arrepaga`.
- **Campos relevantes:**
  - `abs(k00_valor)` normaliza o valor do desconto para exibicao positiva.
  - `k00_numpar` preserva a parcela.
- **Cuidados:** O `left join` em `arrepaga` amarra por `numpre + numpar`, nao por `receita`; se houver mais de uma linha de pagamento para a mesma parcela, trate a cardinalidade com cautela.

#### Consulta: `sql_query_getReceitasTipo`

- **Objetivo:** Listar receitas em aberto associadas a um tipo especifico de debito ou grupo fiscal.
- **Tabelas:** `arrecad`, `tabrec`, `arretipo`, `cadtipo`, `arreinstit`, `arrepaga`, `arrecant`, `arreold`, `arresusp`
- **Parametros:** `:codigoTipo`, `:cadtipo`
- **Filtros e regras:**
  - Quando `cadtipo = true`, o filtro usa `cadtipo.k03_tipo`.
  - Quando `cadtipo = false`, o filtro usa `arrecad.k00_tipo`.
  - Sempre restringe `arreinstit.k00_instit` para a instituicao logada.
  - No modo `cadtipo = true`, a receita so entra se nao existir para o mesmo `numpre + receita` em `arrepaga`, `arrecant`, `arreold` ou `arresusp`.
- **Regra de negocio:** No uso por grupo fiscal, o metodo tenta devolver apenas receitas ainda efetivamente em aberto e nao deslocadas para pago, historico anterior, historico de origem ou suspensao.
- **Cuidados:** O `not exists` ignora parcela; o bloqueio acontece por `numpre + receita`.

#### Consulta: `sql_query_getReceitasTipoVinculo`

- **Objetivo:** Listar receitas em aberto de um tipo e informar o procedimento de `diversos/procdiver` associado ao `numpre`.
- **Tabelas:** `arrecad`, `diversos`, `procdiver`, `proced`, `tabrec`, `arretipo`, `cadtipo`, `arreinstit`, `arrepaga`, `arrecant`, `arreold`, `arresusp`
- **Juncoes adicionais:**
  - `diversos.dv05_numpre = arrecad.k00_numpre`
  - `procdiver.dv09_procdiver = diversos.dv05_procdiver`
  - `proced.v03_codigo = procdiver.dv09_proced`
- **Regra:** Repete a mesma logica de exclusao de estados de `sql_query_getReceitasTipo`, mas acrescenta o contexto do procedimento administrativo.

#### Consulta: `sqlDebitosPorTipoContribuinte`

- **Objetivo:** Listar debitos em aberto por origem do contribuinte pesquisado.
- **Tipos aceitos:** `1 = CGM`, `2 = matricula`, `3 = inscricao`, `4 = auto de infracao`, `5 = notificacao de lancamento`
- **Juncoes fixas:**
  - `arreinstit.k00_numpre = arrecad.k00_numpre`
  - `arretipo.k00_tipo = arrecad.k00_tipo`
  - `cadtipo.k03_tipo = arretipo.k03_tipo`
  - `issvar.q05_numpre = arrecad.k00_numpre`
  - `issvar.q05_numpar = arrecad.k00_numpar`
- **Juncoes variaveis por tipo:**
  - CGM: `arrenumcgm.k00_numpre = arrecad.k00_numpre`
  - Matricula: `arrematric.k00_numpre = arrecad.k00_numpre`
  - Inscricao: `arreinscr.k00_numpre = arrecad.k00_numpre`
  - Auto: `arreauto.k00_numpre = arrecad.k00_numpre`
  - Notificacao: `arrelanc.k00_numpre = arrecad.k00_numpre`
- **Regra de valor:**
  - Para `cadtipo.k03_tipo = 3`, a linha tambem pode ser aceita quando `issvar.q05_vlrinf > 0` ou `issvar.q05_valor > 0`, mesmo que a regra de valor nao dependa apenas de `arrecad.k00_valor`.
  - Nos demais casos, a linha precisa ter `arrecad.k00_valor > 0`.
- **Cuidados:** O metodo sempre injeta o filtro da instituicao logada em `arreinstit`; consultas interinstitucionais precisam de outra base.

#### Consulta: `sqlTiposDebitosGeral`

- **Objetivo:** Retornar tipos de debito do exercicio no contexto da instituicao logada.
- **Tabelas:** `arrecad`, `arretipo`, `cadtipo`, `issvar`
- **Regra:** Reaplica a mesma validacao de valor de `sqlDebitosPorTipoContribuinte`, mas sem exigir um contribuinte especifico.
- **Cuidado importante:** O metodo filtra `k00_instit = db_getsession("DB_instit")` no `where`, mas o SQL montado nao faz join com `arreinstit`. Como `k00_instit` nao pertence a `arrecad`, a consulta depende de contexto externo ou esta inconsistente na forma atual da classe.

#### Regras operacionais observadas na classe

- `excluir_arrecad($numpre, $numpar, $excluir_arrecad, $receit)` copia linhas de `arrecad` para `arreold` antes da exclusao, preservando o historico do debito que saiu do saldo aberto.
- `excluir_arrecad_inc_arrecant($numpre, $numpar, $excluir_arrecad)` copia linhas de `arrecad` para `arrecant` antes da exclusao, preservando um estado anterior do debito.
- O loop dessas rotinas le o primeiro registro encontrado e repete o `insert` pelo numero de linhas retornadas; isso indica intencao de copiar varias linhas, mas a implementacao observada reutiliza sempre os valores da primeira linha do `select`.
- `alterar_tipo($tipo, $where)` permite reclassificar o tipo do debito sem alterar os demais campos da linha.

#### Consulta: `sql_busca_custas`

- **Objetivo:** Somar custas e honorarios de termo em qualquer estado do debito.
- **Tabelas:** `arrecad`, `arrecant`, `arreold`, `taxa`
- **Filtros e regras:**
  - Busca somente `k00_hist in (11303, 11304)`.
  - Usa `k00_receit = taxa.ar36_receita`.
  - Quando `lAgrupaPorParcela = true`, retorna `parcela` e `valor`.
  - Quando `lAgrupaPorParcela = false`, retorna `custa_honorario`, `descricao` e `valor`.
- **Regra de negocio:** Custas de termo podem estar no debito aberto, no historico anterior ou no historico de origem; por isso a apuracao precisa unir os tres estados.

#### Cuidados para consultas do agente

- Para saldo atual em aberto, a referencia primaria e `arrecad`; `arreold` e `arrecant` sao historicos e `arrepaga` e quitacao.
- Ao juntar `arrecad` com tabelas de vinculo por `k00_numpre`, confirme se a pergunta exige contar `numpre`, parcela ou componente financeiro.
- Filtros por instituicao geralmente entram por `arreinstit`, nao por coluna interna de `arrecad`.
- Receitas em aberto por tipo usam exclusao por existencia em outros estados; isso e mais forte do que apenas verificar se a linha ainda existe em `arrecad`.

---

---

### Conceito: tipo_e_grupo_debito
- **Descrição:** Classificação dos débitos por tipo específico (arretipo) e grupo geral (cadtipo).
- **Tabelas:** `caixa.arrecad`, `caixa.arrepaga`, `caixa.arretipo`, `caixa.cadtipo`
- **Junções:**
  - `arrecad.k00_tipo = arretipo.k00_tipo`
  - `arretipo.k03_tipo = cadtipo.k03_tipo`
- **Regras de Negócio e Raciocínio Logístico:**
  1. **Autonomia de Cadastro e Padronização:** O `cadtipo` representa o agrupador fiscal macro (ex: 1 = IPTU, 2 = ISSQN, 3 = Taxas, etc.), sendo fixo e padrão em todas as instalações do e-Cidade. Contudo, cada prefeitura possui seu próprio Código Tributário Municipal (CTM). Por isso, cada cliente cria seus próprios tipos derivados em `arretipo` (ex: "IPTU Comercial", "IPTU Residencial Alíquota Progressiva", "ISS Variável Sociedade Uniprofissional") vinculando-os ao respectivo `cadtipo` pai.
  2. **Agrupamentos Globais:** Para responder perguntas como *"Quanto arrecadamos de ISSQN?"*, a IA deve rastrear o grupo global `cadtipo.k03_tipo = 2` e somar os débitos dos tipos filhos vinculados, em vez de tentar adivinhar ou filtrar por nomes literais em `arretipo.k00_descr`, que mudam em cada município.

---

### Regra de Negócio: Ciclo de Vida do Débito e Fluxo de Caixa
Para raciocinar sobre adimplência, inadimplência e arrecadação geral, o Agente deve considerar as seguintes regras fundamentais de funcionamento do caixa:
1. **O Estado de "A Vencer" e "Vencido" (Em Aberto):**
   Todos os débitos gerados e não pagos residem na tabela `caixa.arrecad`. Um débito é identificado por um `k00_numpre` (número de arrecadação) e desmembrado em parcelas (`k00_numpar`). Se a data atual for maior que `k00_dtvenc` e o débito continuar em `arrecad`, ele é considerado inadimplente/vencido.
2. **O Estado de "Pago" (Quitado):**
   No exato momento em que um contribuinte paga um débito no banco ou tesouraria, o registro correspondente é **deletado** da tabela `caixa.arrecad` (sai do saldo devedor ativo) e uma cópia com os dados da quitação é **inserida** na tabela `caixa.arrepaga` (arrecadação realizada).
3. **Cálculo de Inadimplência:**
   Para saber o total calculado/lançado histórico, a soma deve considerar `calculado = (tudo que está em arrepaga) + (tudo que está em arrecad)`. A taxa de inadimplência atual é calculada dividindo `arrecad.k00_valor` (o que sobrou sem pagar) pelo `total_calculado`.
4. **Pagamentos Parciais:**
   Se um contribuinte paga apenas parte de uma parcela, o sistema liquida a parcela original em `arrecad`, joga o valor pago para `arrepaga`, e gera um novo desmembramento (normalmente uma parcela complementar ou resíduo) em `arrecad` com o saldo restante.

---

---

### Regras de Negócio e Receitas de IPTU
As regras de negócio específicas para apurações de valores calculados, lançados, arrecadados e inadimplência de IPTU foram consolidadas no arquivo dedicado:
- Para detalhes de IPTU, consulte: [iptu.md](file:///home/dbseller/Modelos/MVP/knowledge/rag/caixa/iptu.md)
