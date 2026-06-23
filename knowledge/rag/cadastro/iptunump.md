## cadastro.iptunump

> Fonte manual: `knowledge/manual/cadastro.md#cadastro.iptunump`
> Fonte de codigo: `/var/www/html/e-cidade-php74/classes/db_iptunump_classe.php`

### Resumo tecnico

- Descricao: vincula matricula e exercicio ao `numpre` gerado para os carnês de IPTU.
- Chave primaria: `j20_anousu`, `j20_matric`
- Chave de negocio: `j20_anousu`, `j20_matric`
- Coluna de tempo: `j20_anousu`
- Grao: uma linha por matricula e exercicio; algumas consultas ampliam o resultado com territorio e receitas de taxa
- Recomendada: sim
- Significado da contagem: conta vinculos entre matricula, exercicio e codigo de arrecadacao, nao parcelas nem pagamentos.
- Candidatas a chave de negocio: `j20_matric`, `j20_numpre`
- Candidatas a coluna de tempo: `j20_anousu`

### Relacionamentos

- `j20_matric` -> `cadastro.iptubase` (`j01_matric`) [iptunump_matric_fk]

### Perguntas que esta tabela ajuda a responder

- Qual `numpre` foi gerado para uma matricula no exercicio?
- Quais matriculas ja possuem codigo de arrecadacao no ano?
- Como localizar o endereço territorial usado na emissão do carnê para uma matricula?
- Como combinar o `numpre` com taxas específicas do exercício?

### Filtros e regras reaproveitaveis

#### Filtros padrao

- Exercício: `j20_anousu = :anousu`
- Matrícula: `j20_matric = :matricula`
- Código de arrecadação: `j20_numpre = :numpre`

#### Semantica de filtros

- `j20_anousu` define o ano do vínculo do `numpre`.
- `j20_matric` amarra o código de arrecadação ao imóvel cadastrado em `iptubase`.
- `j20_numpre` é o identificador usado para arrecadação, carnê e recibos.

### Consulta: `sql_query`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptunump_classe.php`
- **Objetivo:** ler o vínculo entre matrícula, exercício e `numpre` com enriquecimento cadastral do imóvel, lote e contribuinte.
- **Tabelas:** `iptunump`, `iptubase`, `lote`, `cgm`
- **Grau do resultado:** uma linha por matrícula e exercício, desde que existam correspondências em `iptubase`, `lote` e `cgm`
- **Parametros:** `j20_anousu`, `j20_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - `iptubase.j01_matric = iptunump.j20_matric` `inner join`
  - `lote.j34_idbql = iptubase.j01_idbql` `inner join`
  - `cgm.z01_numcgm = iptubase.j01_numcgm` `inner join`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio, filtra por exercício e/ou matrícula.
  - Os `inner join` descartam vínculos sem lote ou contribuinte associados.
- **Campos relevantes:**
  - `j20_anousu`, `j20_matric`, `j20_numpre`
  - `j01_idbql`, `j01_numcgm`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptunump
    inner join iptubase on iptubase.j01_matric = iptunump.j20_matric
    inner join lote on lote.j34_idbql = iptubase.j01_idbql
    inner join cgm on cgm.z01_numcgm = iptubase.j01_numcgm
   where /* j20_anousu, j20_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Use esta consulta quando precisar do `numpre` ligado ao cadastro do imóvel.
  - Não trate o retorno como histórico de parcelas pagas; ele só aponta o código de arrecadação.

### Consulta: `sql_query_ender`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptunump_classe.php`
- **Objetivo:** montar a posição do IPTU com dados territoriais do imóvel.
- **Tabelas:** `iptunump`, `iptubase`, `lote`, `testada`, `testpri`, `bairro`, `ruas`, `zonas`, `setor`
- **Grau do resultado:** uma linha por matrícula e exercício, enriquecida com área territorial, face, bairro, rua, zona e setor
- **Parametros:** `j20_anousu`, `j20_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - `iptubase.j01_matric = iptunump.j20_matric` `inner join`
  - `lote.j34_idbql = iptubase.j01_idbql` `inner join`
  - `testada.j34_idbql = j36_idbql` `inner join`
  - `testpri.j49_idbql = j36_idbql and j49_face = j36_face and j49_codigo = j36_codigo` `inner join`
  - `bairro.j13_codi = j34_bairro` `inner join`
  - `ruas.j14_codigo = j36_codigo` `inner join`
  - `zonas.j50_zona = j34_zona` `inner join`
  - `setor.j30_codi = j34_setor` `inner join`
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio, filtra por exercício e/ou matrícula.
  - A consulta é territorial: ela depende de registros completos de lote, testada, rua, zona e setor.
- **Campos relevantes:**
  - `j20_anousu`, `j20_matric`, `j20_numpre`
  - `j34_bairro`, `j34_setor`, `j34_zona`, `j36_codigo`, `j36_face`
  - `j13_descr`, `j14_nome`, `j50_descr`, `j30_descr`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptunump
    inner join iptubase on iptubase.j01_matric = iptunump.j20_matric
    inner join lote on lote.j34_idbql = iptubase.j01_idbql
    inner join testada on testada.j36_idbql = lote.j34_idbql
    inner join testpri
      on testpri.j49_idbql = testada.j36_idbql
     and testpri.j49_face = testada.j36_face
     and testpri.j49_codigo = testada.j36_codigo
    inner join bairro on bairro.j13_codi = lote.j34_bairro
    inner join ruas on ruas.j14_codigo = testada.j36_codigo
    inner join zonas on zonas.j50_zona = lote.j34_zona
    inner join setor on setor.j30_codi = lote.j34_setor
   where /* j20_anousu, j20_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Esta consulta é usada para a “posição do IPTU”, então ela só funciona bem quando o cadastro territorial está consistente.
  - Nao confunda com `sql_query()`: aqui o foco é endereço/território, não apenas o vínculo `numpre`.

### Consulta: `sql_query_file`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptunump_classe.php`
- **Objetivo:** leitura direta da tabela `iptunump` por exercício, matrícula ou filtro livre.
- **Tabelas:** `iptunump`
- **Grau do resultado:** uma linha por matrícula e exercício
- **Parametros:** `j20_anousu`, `j20_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:** nenhuma
- **Filtros e regras:**
  - Quando `dbwhere` esta vazio, aplica os filtros informados de exercício e matrícula.
  - É a leitura bruta do vínculo, sem contexto territorial nem cadastral adicional.
- **Campos relevantes:**
  - `j20_anousu`, `j20_matric`, `j20_numpre`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptunump
   where /* j20_anousu, j20_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - Use quando a pergunta for apenas sobre o vínculo entre matrícula e `numpre`.
  - Não carrega evidência de carnê emitido, pagamento ou arrecadação efetiva.

### Consulta: `sql_query_ender_taxa`

- **Fonte:** `/var/www/html/e-cidade-php74/classes/db_iptunump_classe.php`
- **Objetivo:** combinar o `numpre` do IPTU com `numpre` de taxas do mesmo exercício e retornar a base territorial do imóvel.
- **Tabelas:** `iptubase`, `iptunump`, `iptutaxanump`, `iptucadtaxaexe`, `lote`, `testada`, `testpri`, `bairro`, `ruas`, `zonas`, `setor`
- **Grau do resultado:** uma linha por matrícula associada a `numpre` de IPTU ou de taxa; pode haver mais de uma linha por matrícula se existirem vínculos em `iptunump` e `iptutaxanump`
- **Parametros:** `j20_anousu`, `j20_matric`, `campos`, `ordem`, `dbwhere`
- **Juncoes:**
  - Subconsulta `nump` faz `union` entre:
    - `iptunump.j20_matric`, `iptunump.j20_anousu`, `iptunump.j20_numpre`
    - `iptutaxanump.j151_matric as j20_matric`, `iptucadtaxaexe.j08_anousu as j20_anousu`, `iptutaxanump.j151_numpre as j20_numpre`
  - `iptubase.j01_matric = nump.j20_matric` `inner join`
  - `lote.j34_idbql = iptubase.j01_idbql` `inner join`
  - `testada.j34_idbql = j36_idbql` `inner join`
  - `testpri.j49_idbql = j36_idbql and j49_face = j36_face and j49_codigo = j36_codigo` `inner join`
  - `bairro.j13_codi = j34_bairro` `inner join`
  - `ruas.j14_codigo = j36_codigo` `inner join`
  - `zonas.j50_zona = j34_zona` `inner join`
  - `setor.j30_codi = j34_setor` `inner join`
- **Filtros e regras:**
  - A subconsulta usa `j20_anousu = $j20_anousu` e `txexe.j08_anousu = $j20_anousu`.
  - O `union` junta `numpre` de IPTU e de taxas do mesmo exercício.
  - A consulta depende de dados de taxa específica cadastrados em `iptutaxanump` e `iptucadtaxaexe`.
- **Campos relevantes:**
  - `j20_anousu`, `j20_matric`, `j20_numpre`
  - `j151_matric`, `j151_numpre`, `j08_anousu`
- **SQL normalizada:**

  ```sql
  select /* campos dinamicos */
    from iptubase
    inner join (
      select j20_matric, j20_anousu, j20_numpre
        from iptunump
       where j20_anousu = :anousu
      union
      select j151_matric as j20_matric,
             j08_anousu as j20_anousu,
             j151_numpre as j20_numpre
        from iptutaxanump
        inner join iptucadtaxaexe on iptucadtaxaexe.j08_iptucadtaxaexe = iptutaxanump.j151_iptucadtaxaexe
       where iptucadtaxaexe.j08_anousu = :anousu
    ) nump on iptubase.j01_matric = nump.j20_matric
    inner join lote on lote.j34_idbql = iptubase.j01_idbql
    inner join testada on testada.j34_idbql = lote.j34_idbql
    inner join testpri
      on testpri.j49_idbql = testada.j36_idbql
     and testpri.j49_face = testada.j36_face
     and testpri.j49_codigo = testada.j36_codigo
    inner join bairro on bairro.j13_codi = lote.j34_bairro
    inner join ruas on ruas.j14_codigo = testada.j36_codigo
    inner join zonas on zonas.j50_zona = lote.j34_zona
    inner join setor on setor.j30_codi = lote.j34_setor
   where /* j20_anousu, j20_matric ou dbwhere dinamico */
   order by /* ordem dinamica */
  ```

- **Cuidados:**
  - O `union` pode retornar mais de um `numpre` por matrícula dependendo do exercício e da existência de taxa específica.
  - Este método é mais analítico do que `sql_query_ender()`, porque agrega também o universo de taxas do exercício.

### Regras de manutenção observadas

1. `j20_anousu` e `j20_matric` formam a chave operacional do vínculo.
2. `j20_numpre` é preenchido externamente e representa o código de arrecadação do carnê.
3. `sql_query()` é a consulta direta do vínculo com o imóvel.
4. `sql_query_ender()` é a visão territorial usada em posição do IPTU.
5. `sql_query_ender_taxa()` consolida IPTU e taxas específicas do exercício.

### Cuidados / riscos

- Nao confundir `iptunump` com cobrança paga: ele só vincula o carnê ao imóvel e ao exercício.
- Nao usar a chave primaria como se fosse numérico único global; ela é composta por exercício e matrícula.
- `sql_query_ender()` e `sql_query_ender_taxa()` dependem de integridade territorial alta; registros faltantes em `lote`, `testada`, `testpri`, `bairro`, `ruas`, `zonas` ou `setor` removem linhas.
- O `union` de `sql_query_ender_taxa()` pode multiplicar o resultado quando IPTU e taxa coexistem para a mesma matrícula.
- Em fluxos de carnê e recibo, cruze com `arrematric`, `arrecad` e `arrepaga` quando a pergunta for sobre cobrança ou pagamento, não apenas geração de `numpre`.
