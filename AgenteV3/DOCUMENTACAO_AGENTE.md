# Documentação de Arquitetura: AgenteV3 (e-Cidade IA)

Este documento foi criado para facilitar o estudo e a explicação do fluxo de dados e dos módulos do AgenteV3.

## 1. Visão Geral do Fluxo

O AgenteV3 atua como um assistente inteligente com acesso a leitura do banco de dados (e-Cidade). O fluxo de uma pergunta do usuário ocorre na seguinte ordem:

1. **Frontend (Dashboard):** O usuário envia uma pergunta.
2. **Backend (API):** A requisição chega no `AgentController`.
3. **Orquestrador (Loop ReAct):** O `Orchestrator` intercepta a pergunta e inicia um "Loop ReAct" (Raciocínio e Ação). 
4. **Ferramentas (Tools):** O Agente decide se precisa ler as regras de negócio (`RagSearchTool`) ou consultar o banco de dados (`McpExecutionTool`).
5. **Comunicação em Tempo Real (WebSockets):** Cada passo que o Agente dá é transmitido ao vivo para o Frontend via Laravel Reverb.
6. **Resposta Final:** O Agente compila os dados encontrados, devolve o resultado final, e encerra o fluxo.

---

## 2. Componentes Principais

### 2.1 AgentController (`app/Http/Controllers/AgentController.php`)
É a **porta de entrada** da API.
- **Responsabilidade:** Receber a requisição POST com a variável `question`, validar a entrada e repassar para a camada de serviço (o `Orchestrator`).
- **Retorno:** Retorna o JSON contendo a resposta final do agente (após a conclusão do loop).

### 2.2 Orchestrator (`app/Services/Agent/Orchestrator.php`)
É o **Cérebro** da aplicação. Implementa manualmente o padrão *ReAct* usando o pacote Laravel Prism.
- **Loop ReAct (while):** O orquestrador injeta as "Ferramentas" (Tools) no prompt do Gemini. Como definimos `withMaxSteps(1)`, o Prism tenta resolver a pergunta, mas nós o "pausamos" a cada passo.
- **Execução Manual:** Se o modelo disser "Eu preciso usar a ferramenta RAG", o código do Orchestrator captura esse pedido, roda a ferramenta manualmente em PHP (bloqueante), colhe o resultado, e empurra de volta para o modelo na iteração seguinte.
- **Eventos em Tempo Real:** Ao final de cada passo intermediário, o Orchestrator dispara o evento `AgentStepStreamed`. Esse evento vai pelo canal do Laravel Reverb (WebSocket) e faz a tela do usuário piscar "Agente processando...".
- **Truncamento de Payload:** Como ferramentas SQL ou RAG podem retornar megabytes de dados (o que derrubaria o WebSocket), o Orchestrator possui um filtro de segurança antes do `event()`. Se os dados passarem de 5KB, ele oculta grandes blocos textuais (`[Resultado truncado no backend]`), enviando apenas as cascas para que a interface não congele.

### 2.3 RagSearchTool (`app/Tools/RagSearchTool.php`)
É a biblioteca de regras de negócio.
- **Funcionamento:** Quando o Agente não sabe como uma tabela funciona, ele usa essa ferramenta buscando por uma palavra-chave (ex: `inadimplencia`).
- **Lógica de Busca:** A classe varre o diretório de arquivos Markdown local (`knowledge/rag/`). 
  - Se a palavra pesquisada bater exatamente com o **nome do arquivo**, ela devolve o conteúdo **inteiro**.
  - Se a palavra pesquisada não for nome de arquivo, mas estiver dentro de algum texto, ela devolve apenas um "recorte" (snippet) das linhas ao redor da palavra.
- **Dica de Negócio:** Sempre nomeie arquivos vitais com termos-chave para garantir que o Agente carregue a regra por completo.

### 2.4 McpExecutionTool (`app/Tools/McpExecutionTool.php`)
É o braço de execução no PostgreSQL.
- **Padrão MCP:** O Agente não acessa o banco do Laravel diretamente. Ele utiliza a ferramenta MCP (Model Context Protocol).
- **Processo HTTP RPC:** O PHP empacota a String do SQL que o Gemini escreveu e dispara um POST JSON-RPC para o servidor MCP local (`host.docker.internal:8010/mcp`).
- **Controle de Sessão:** Como o servidor MCP gerencia cursores e transações, a classe implementa um handshake de inicialização no primeiro contato (método `ensureSession()`), mantendo um `Mcp-Session-Id` pelo resto do processo.
- **Segurança:** O MCP Server está configurado (via Python) em modo read-only e possui timeouts (ex: 5 segundos ou mais, configuráveis no `.env` do MCP) para impedir que o Agente faça Drop Tables ou cause lentidão no ERP da Prefeitura.

---

## 3. Considerações de Arquitetura e Extensibilidade

- **Troca de Modelos (LLMs):** O modelo é lido da variável de ambiente (`GEMINI_MODEL=gemini-2.5-flash`). Para trocar por um modelo superior (`pro`) ou inferior (`lite`), basta alterar o `.env` e rodar `php artisan config:clear`.
- **Prevenção de Fan-out no SQL:** Devido às estruturas complexas de parcelamento no sistema tributário municipal (ex: tabela `caixa.arrecad` vs `cadastro.iptucalv`), o Agente foi explicitamente instruído (via RAG) a nunca usar `COUNT` puro, mas sim subqueries com `SUM`, isolando os montantes financeiros antes de um `LEFT JOIN`.
