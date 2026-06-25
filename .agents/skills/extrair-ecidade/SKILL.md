---
name: extrair-ecidade
description: >-
  Extrair consultas SQL e regras de negocio relevantes de arquivos PHP legados
  do e-Cidade e documenta-las em Markdown para o RAG do projeto.
---

# Extrair e-Cidade

Analisar codigo PHP do e-Cidade manualmente e transformar consultas relevantes em conhecimento auditavel para o agente. Nao criar script de extracao e nao executar SQL no banco.

## Objetivo

Ter informacoes suficientes para o agente usar o conhecimento para responder perguntas e tomar decisoes. Para isso, as informacoes devem ser ricas para o agente entender a logica de negocio do sistema e como ele funciona com RAG.

O foco e na regra de negocio para que o agente seja capaz de criar suas proprias queries; o SQL e apenas um caminho rapido.

## Fluxo

1. Localizar o arquivo informado.
   - Respeitar um caminho absoluto quando fornecido.
   - Para caminho relativo, procurar primeiro no checkout de e-Cidade indicado pelo usuario.
   - Se nenhum checkout for indicado, verificar os checkouts locais plausiveis e declarar qual arquivo foi usado.
   - Se houver copias divergentes, nao combinar versoes silenciosamente.

2. Identificar o escopo solicitado.
   - Se o usuario nomear um metodo, priorizar esse metodo.
   - Se informar apenas o arquivo, listar os metodos de consulta e selecionar os que carregam semantica util.
   - Ignorar CRUD gerado e consultas triviais quando nao acrescentarem regra, relacionamento ou significado para o agente.

3. Reconstruir a consulta.
   - Ler o metodo completo e os auxiliares chamados por ele.
   - Rastrear SQL concatenado em varias variaveis, condicionais e metodos.
   - Separar trechos fixos de fragmentos dinamicos como campos, ordem e `$dbwhere`.
   - Preservar placeholders sem inventar valores.
   - Normalizar a SQL somente para legibilidade; nao alterar sua semantica.

4. Entender a regra.
   - Mapear tabelas reais, aliases, joins, filtros, agrupamentos, ordenacao e parametros.
   - Determinar o grao do resultado e o que uma linha representa.
   - Ler chamadas do metodo e telas consumidoras quando isso for necessario para entender o uso.
   - Crie perguntas que essa consulta responde e liste na documentação.
   - Crie pergutas relacionadas a tabela.
   - Diferenciar regra comprovada pelo codigo de interpretacao provavel.
   - Nao transformar nome de metodo, comentario ou semelhanca de colunas em regra confirmada.

5. Escolher o destino em `knowledge/rag`.
   - Reutilizar um documento de negocio existente quando ele representar claramente a consulta.
   - Usar o modulo/schema como diretorio, por exemplo `cadastro/`, `issqn/` ou `caixa/`.
   - Usar o documento da tabela principal quando a consulta for essencialmente centrada nela, como `knowledge/rag/cadastro/iptuconstr.md`.
   - Criar um nome de conceito intuitivo quando a consulta combinar varias tabelas ou representar uma pergunta de negocio.
   - Nao inventar nome de tabela. Conceitos que nao sao objetos fisicos devem ser declarados como conceitos de negocio.
   - Antes de criar arquivo, pesquisar documentos relacionados para evitar duplicidade.

6. Atualizar o Markdown.
   - Preservar o conteudo correto que ja existe.
   - Fazer merge por metodo/receita, sem duplicar a mesma consulta.
   - Registrar a origem exata do codigo e o nome do metodo.
   - Escrever para recuperacao RAG: termos de negocio explicitos, nomes reais de tabelas e regras objetivas.
   - Nao copiar blocos irrelevantes da classe.

7. Validar.
   - Conferir se todas as tabelas e colunas documentadas aparecem no codigo analisado ou estao marcadas como contexto adicional.
   - Conferir aliases, chaves de join e filtros contra a SQL original.
   - Conferir se agregacoes respeitam o grao e nao multiplicam entidades indevidamente.
   - Procurar contradicoes com o documento de destino.
   - Revisar o diff final e informar arquivo criado ou atualizado.

## Formato da Documentacao

Adaptar ao documento existente. Para uma nova receita, preferir:

````markdown
### Consulta: `sql_query_exemplo`

- **Fonte:** `/caminho/classes/db_exemplo_classe.php`
- **Objetivo:** Explicacao curta do que a consulta recupera.
- **Tabelas:** `schema.tabela_a`, `schema.tabela_b`
- **Grao do resultado:** Uma linha por ...
- **Parametros:** `:parametro` - significado.
- **Juncoes:**
  - `tabela_a.chave = tabela_b.chave`
- **Filtros e regras:**
  - Regra comprovada pela condicao SQL.
- **Campos relevantes:**
  - `coluna` - significado observado no contexto.
- **SQL normalizada:**

  ```sql
  SELECT ...
  ```
````

- **Cuidados:**
  - Fragmentos dinamicos, cardinalidade, nulos, historico ou risco de duplicacao.
- **Evidencia adicional:** Chamada ou tela consumidora, quando consultada.

````

Omitir secoes vazias. Se a SQL depender de fragmento arbitrario, representar explicitamente, por exemplo `/* campos dinamicos */`, e explicar o limite em **Cuidados**.

## Regras de Qualidade

- Usar somente tabelas, colunas e relacionamentos verificaveis.
- Nao afirmar que um filtro e regra municipal geral quando ele aparece apenas em uma tela ou chamada especifica.
- Nao confundir `LEFT JOIN` com obrigatoriedade do relacionamento.
- Nao confundir contagem de linhas com contagem de entidades; indicar quando usar `DISTINCT`.
- Nao inferir entidade ativa, cancelada, baixada ou vigente sem condicao explicita ou evidencia complementar.
- Nao executar consultas que alterem dados.
- Nao sobrescrever documentos inteiros quando uma secao incremental resolve.
- Se a regra permanecer ambigua, documentar a SQL e registrar a ambiguidade em vez de completar por suposicao.

## Exemplo de Uso

Pedido:

```text
Use $extrair-ecidade em classes/db_iptuconstr_classe.php,
metodo sql_query_proprietario_nome.
````

Resultado esperado: localizar a classe correta, reconstruir a consulta do metodo, explicar o relacionamento entre construcao, matricula e proprietario, e atualizar `knowledge/rag/cadastro/iptuconstr.md` ou outro documento mais intuitivo caso a semantica encontrada seja mais ampla.
