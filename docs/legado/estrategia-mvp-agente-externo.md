# Estrategia do MVP - Agente Externo e e-Cidade

## Decisao principal

Para o MVP de apresentacao, a inteligencia fica no Agente Externo e o e-Cidade atua como conector seguro de dados.

O MCP nao entra como dependencia principal agora. Ele pode ser criado depois como adaptador padronizado sobre a propria API do e-Cidade, mas para a primeira entrega ele adiciona complexidade sem aumentar o valor demonstravel.

## Arquitetura do MVP

```text
Usuario
  -> Chat Web do Agente Externo
    -> Historico da conversa
    -> Catalogo tecnico-semantico local
    -> Planejador de consulta
      -> API e-Cidade /analise
        -> metadata
        -> query readonly
        -> docs/search
      <- JSON de dados
    <- Analise e resposta executiva
```

## Responsabilidades

### Agente Externo

- Receber perguntas em linguagem natural.
- Manter historico das conversas.
- Identificar dominio, inicialmente IPTU/Cadastro Imobiliario.
- Consultar catalogo local de tabelas, campos e significados.
- Montar consulta read-only usando nomes fisicos reais.
- Chamar a API do e-Cidade.
- Interpretar o retorno e gerar uma resposta compreensivel para apresentacao.

### API e-Cidade

- Expor metadados de schema, tabelas, campos, chaves e relacionamentos.
- Executar consultas read-only validadas.
- Bloquear comandos perigosos.
- Aplicar limite, timeout, schema permitido e log.
- Nunca conter a inteligencia analitica do agente.

### MCP

- Fica reservado para uma segunda etapa.
- Pode encapsular as chamadas da API e-Cidade em tools MCP.
- Nao deve acessar diretamente o banco no MVP.

## Endpoint base usado no MVP

```text
http://localhost:8090/e-cidade-php74/v4/api/analise
```

Endpoints ja disponiveis:

- `GET /health`
- `GET /metadata/schemas`
- `GET /metadata/tables?schema=cadastro`
- `GET /metadata/tables/{schema}/{table}`
- `GET /metadata/relationships`
- `GET /docs/search?q=termo`
- `POST /query/readonly`
- `POST /analysis/save`

## Primeiro caso demonstravel

Pergunta exemplo:

```text
Compare o IPTU 2026 e 2027 e explique os principais fatores de aumento.
```

Fluxo esperado:

1. O agente identifica o assunto IPTU.
2. O agente usa o catalogo local para selecionar `cadastro.iptucalc`.
3. O agente monta uma consulta read-only com campos de ano, matricula, area, valor de terreno, aliquota, isencao e flag de financeiro.
4. A API do e-Cidade valida e executa a consulta.
5. O agente compara os dados por matricula quando existirem os dois anos.
6. O chat apresenta resumo executivo, quantidade de registros, maiores variacoes e SQL usado.

## Evolucao depois da apresentacao

- Trocar SQL livre validado por plano declarativo JSON.
- Adicionar autenticacao por token no conector.
- Criar usuario PostgreSQL read-only especifico.
- Persistir catalogo em banco proprio do agente.
- Criar MCP como camada opcional sobre a API.
- Ampliar dominios alem de IPTU.
- Adicionar agendamento de relatorios aprovados.
