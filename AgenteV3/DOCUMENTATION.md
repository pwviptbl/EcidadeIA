# E-cidade Agente V3 (Laravel Prism)

## Visão Geral da Arquitetura
Esta versão representa uma grande evolução em relação ao AgenteV2. O AgenteV2 operava com uma **Pipeline Linear** desenvolvida em Python (IntentExtractor -> BusinessResolver -> SchemaPlanner -> SqlCompiler). Se ocorresse qualquer erro na montagem do SQL, o script parava a execução.

A **V3** implementa um **Agentic Loop (ReAct - Reason + Act)** usando PHP e Laravel. Neste formato autônomo, o Agente raciocina sobre o erro de sintaxe SQL, pesquisa o Markdown do RAG em busca de mais informações e tenta compilar a query novamente usando Ferramentas (Tool Calling), de maneira análoga a como um Engenheiro DevSecOps analisaria logs e corrigiria seu payload.

### Stack Tecnológica
- **Orquestrador LLM:** Laravel + pacote `echolabsdev/prism` (Raciocínio, Tool Calling e Gestão de Estado).
- **Ambiente:** Conteinerizado usando Docker / Laravel Sail.
- **Data Execution (Read-only):** Servidor Python MCP independente (comunicando-se via JSON-RPC via porta 8010), responsável exclusivamente por lidar com o tráfego da VPN para o PostgreSQL do E-cidade.

## Por que Laravel Prism?
1. **Tool Calling Nativo:** Permite instanciar classes simples no PHP que a IA aciona automaticamente (ex: `readMarkdownFile()`, `executeSqlOnMcp()`).
2. **Ciclo ReAct Automático:** O LLM tenta resolver a tarefa e, caso o Postgres (via MCP) devolva erro de coluna inexistente, o LLM recebe o erro no histórico e deduz como ajustar a query automaticamente.
3. **Escalabilidade Web:** Facilita a criação imediata de APIs (FastAPI no V2 daria trabalho extra com gestão assíncrona, enquanto o Laravel foca 100% na produtividade e em prover a interface REST/WebSockets ao front-end).

## Divisão de Responsabilidades
- `AgenteV3 (Container Laravel)`: Cérebro. Entende a pergunta do usuário, busca no RAG, monta o SQL, lida com as repetições de erro, orquestra e devolve a resposta ao Front-end.
- `Python MCP (Host local)`: Braço Operacional. Seu único papel é receber uma String SQL pura do Laravel e devolver as Rows ou Erros diretamente do banco na VPN.

## Roadmap de Implementação

### Passo 1: Inicialização do Core
- [x] Rodar o comando de scaffolding do Laravel (ex: `composer create-project laravel/laravel .`)
- [x] Instalar o Laravel Sail para subir o ambiente no Docker.
- [x] Instalar o pacote `echolabsdev/prism` via composer.

### Passo 2: Integração de Ferramentas (Tools)
- [x] Mover/mapear os arquivos Markdown de RAG (`knowledge/rag/`) para serem acessíveis ao Laravel.
- [x] Criar a Tool `RagSearchTool`: Permite o agente Prism buscar regras de negócios em texto.
- [x] Criar a Tool `McpExecutionTool`: Dispara requisição HTTP POST para o nosso MCP de banco (`http://host.docker.internal:8010/`).

### Passo 3: O Workflow Autônomo (Prism Loop)
- [x] Configurar o System Prompt orientando-o explicitamente sobre o dialeto do PostgreSQL e sua autonomia para falhar, refletir e reescrever as queries.
- [x] Criar a Controller Web ou Comando Artisan que inicie a sessão Prism.

### Passo 4: WebSockets & Human-in-the-Loop
- [ ] Implementar Laravel Reverb (ou Websockets nativos) para fazer o streaming interativo do raciocínio do Prism de volta para o Dashboard.
- [ ] Adicionar suporte a interrupções se o Agente concluir que não há tabelas com os dados exigidos pelo usuário.

## Evoluções Futuras: Migração de RAG para ChromaDB
Tendo em vista o crescimento do volume de dados, a busca em memória baseada em BM25 será substituída por uma arquitetura híbrida de busca vetorial:

1. **Benefício da Persistência:** ChromaDB em container dedicado (`chromadb/chroma` na porta `8000`) para desonerar a memória RAM do Python/Laravel.
2. **Arquitetura de Busca Híbrida (Dense + Sparse):**
   - **Dense (ChromaDB + Gemini Embeddings):** Busca conceitual (ex: entender termos como "inadimplência", "não pago").
   - **Sparse (Filtros de Metadados / Keyword):** Busca técnica exata de tabelas (ex: achar a tabela exata `iptuisen` ou coluna `j23_vlrisen`).
3. **Pipeline de Ingestão:** Script em Python ou Laravel Artisan para ler os `.md` e os arquivos JSONL, fatiar em chunks semânticos, chamar o Gemini Embeddings API e persistir no ChromaDB.

