# Modelo - Receita de relacionamento

Use este modelo para documentar caminhos de negocio entre entidades. A FK mostra uma direcao tecnica; a receita explica quando e por que usar o caminho.
Arquivos dentro de `_modelos` nao devem entrar no RAG; copie o bloco para `knowledge/manual/<schema>/relacionamentos_negocio.md`.

## Receita de relacionamento: nome_da_receita

- Quando usar:
- Origem de negocio:
- Destino de negocio:
- Tabelas no caminho:
  -
- Caminho de negocio:
  -
- Join logico:
  -
- Cardinalidade:
- Filtros recomendados:
  -
- Grao recomendado apos o relacionamento:
- Agregacoes seguras:
  -
- Evidencias / fonte de negocio:
  -
- Cuidados:
  -
- O que nao fazer:
  -

## Como preencher

- Documente o caminho de negocio, mesmo que a FK exista em direcao inversa.
- Explique cardinalidade: um-para-um, um-para-muitos ou muitos-para-muitos.
- Aponte onde a consulta pode multiplicar linhas.
- Nao coloque SQL pronto; descreva joins logicos e filtros de negocio.
