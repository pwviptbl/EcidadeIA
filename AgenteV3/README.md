<p align="center">
  <h1 align="center">E-Cidade IA</h1>
</p>

Este é o repositório principal do E-CidadeIA, um assistente inteligente (LLM) baseado na arquitetura ReAct, capaz de raciocinar sobre regras de negócio e realizar consultas (Read-Only) em bancos de dados legados do e-Cidade.

---

## 🚀 Como Iniciar os Serviços

Para que o E-CidadeIA funcione corretamente (incluindo o chat em tempo real, as buscas RAG e as consultas SQL seguras), você precisa subir 4 serviços em terminais separados:

### 1. Servidor MCP (Python)

Este é o servidor seguro (Model Context Protocol) que expõe o banco de dados PostgreSQL do e-Cidade para o Agente sem arriscar a integridade dos dados (apenas leitura).

```bash
cd /home/dbseller/Modelos/MVP/mcp
source .venv/bin/activate
MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 MCP_PORT=8010 python server.py
```

### 2. Laravel Reverb (WebSockets)

Responsável por fazer o _streaming_ em tempo real dos pensamentos e ações do Agente para a tela do Dashboard (via AlpineJS/Echo).

```bash
cd /home/dbseller/Modelos/MVP/AgenteV3
php artisan reverb:start --host=0.0.0.0 --port=8090
```

_(Dica: Se estiver usando o Laravel Sail, rode `./vendor/bin/sail php artisan reverb:start`)_

### 3. Fila de Trabalhadores (Queue Worker)

Como o Laravel Reverb pode colocar eventos em fila (Queue) para broadcasting assíncrono, é recomendável manter o worker ativo:

```bash
cd /home/dbseller/Modelos/MVP/AgenteV3
php artisan queue:work
```

### 4. Servidor Web (Laravel/PHP)

O backend principal da aplicação (Controller e API).

```bash
cd /home/dbseller/Modelos/MVP/AgenteV3
php artisan serve
```

_(Se estiver usando Laravel Sail, o `sail up -d` já cobre este serviço)_

### 5. Frontend Vite (Opcional, para Dev)

Se for editar o Tailwind CSS, Javascript ou layout do `dashboard.blade.php`:

```bash
cd /home/dbseller/Modelos/MVP/AgenteV3
npm run dev
```

---

## 🧠 Como Funciona a Arquitetura?

1. **RAG (Knowledge Base):** O conhecimento de regras de negócio (como calcular inadimplência, quais tabelas cruzar) fica armazenado em arquivos Markdown em `knowledge/rag/`.
2. **Orchestrator:** Localizado em `app/Services/Agent/Orchestrator.php`, é o motor que roda o Loop ReAct em PHP.
3. **Tools:**
    - `RagSearchTool.php`: Ensina o Agente a ler os arquivos Markdown de regras.
    - `McpExecutionTool.php`: Empacota as consultas SQL do Agente e envia via JSON-RPC para o Servidor MCP validar e executar no banco.

> **Precisa trocar de Modelo LLM?**
> Abra o arquivo `.env`, altere a variável `GEMINI_MODEL=gemini-2.5-flash` para a versão desejada (ex: `flash-lite`) e rode `php artisan config:clear`.
