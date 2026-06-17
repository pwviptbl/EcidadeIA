<?php

namespace App\Tools;

use Prism\Prism\Tool;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class McpExecutionTool extends Tool
{
    protected ?string $sessionId = null;
    protected int $nextId = 1;

    /**
     * Inicializa a ferramenta 'mcp_execute_sql'.
     * Define o nome, descrição e o parâmetro esperado (sql).
     */
    public function __construct()
    {
        $this->as('mcp_execute_sql')
            ->for('Executa uma consulta SQL read-only no banco de dados do e-Cidade através do servidor MCP. Retorna os registros resultantes.')
            ->withStringParameter('sql', 'A query SQL a ser executada. A query deve ser estritamente de leitura (SELECT)')
            ->using(fn (string $sql) => $this->execute($sql));
    }

    /**
     * Empacota a query SQL gerada pelo LLM e dispara um JSON-RPC HTTP POST para o servidor MCP local.
     * Captura o resultado da execução read-only do banco e devolve para o agente em texto.
     *
     * @param string $sql A consulta SQL a ser executada.
     * @return string O resultado da consulta (ex: tabela convertida para texto/JSON) ou mensagem de erro.
     */
    protected function execute(string $sql): string
    {
        Log::info("McpExecutionTool: Executando SQL...", ['sql' => $sql]);

        try {
            $url = env('MCP_SERVER_URL', 'http://host.docker.internal:8010/mcp');
            
            $this->ensureSession($url);

            // Executa a chamada RPC tool/call para ecidade_readonly_query
            $requestId = $this->nextId++;
            
            $headers = [
                'Content-Type' => 'application/json',
                'Accept' => 'application/json, text/event-stream'
            ];
            if ($this->sessionId) {
                $headers['Mcp-Session-Id'] = $this->sessionId;
            }

            $response = Http::withHeaders($headers)
                ->post($url, [
                    'jsonrpc' => '2.0',
                    'id' => $requestId,
                    'method' => 'tools/call',
                    'params' => [
                        'name' => 'ecidade_readonly_query',
                        'arguments' => [
                            'sql' => $sql,
                            'limit' => 1000
                        ]
                    ]
                ]);

            if ($response->failed()) {
                Log::error("McpExecutionTool: Falha ao chamar a tool", [
                    'status' => $response->status(),
                    'body' => $response->body()
                ]);
                return json_encode([
                    'error' => true,
                    'message' => 'Erro ao processar SQL no MCP: ' . $response->body()
                ]);
            }

            $responseData = $response->json();
            
            // Extrai o conteúdo em texto do JSON-RPC
            $contentArray = data_get($responseData, 'result.content', []);
            $textResult = '';
            foreach ($contentArray as $item) {
                if (is_array($item) && isset($item['text'])) {
                    $textResult .= $item['text'];
                }
            }

            return $textResult ?: $response->body();
        } catch (\Exception $e) {
            Log::error("McpExecutionTool: Exceção ao chamar MCP", ['error' => $e->getMessage()]);
            return json_encode([
                'error' => true,
                'message' => 'Falha de comunicação com o servidor MCP: ' . $e->getMessage()
            ]);
        }
    }

    /**
     * Garante o Handshake de Inicialização do Protocolo MCP.
     * Se a sessão ainda não existir, envia a request de 'initialize' com capabilities, 
     * guarda o 'Mcp-Session-Id' retornado no header e envia 'notifications/initialized' para selar a conexão.
     *
     * @param string $url URL do servidor MCP.
     */
    protected function ensureSession(string $url): void
    {
        if ($this->sessionId) {
            return;
        }

        Log::info("McpExecutionTool: Inicializando nova sessão MCP");

        $response = Http::withHeaders([
            'Content-Type' => 'application/json',
            'Accept' => 'application/json, text/event-stream'
        ])->post($url, [
            'jsonrpc' => '2.0',
            'id' => $this->nextId++,
            'method' => 'initialize',
            'params' => [
                'protocolVersion' => '2025-06-18',
                'capabilities' => (object)[],
                'clientInfo' => [
                    'name' => 'agente-v3',
                    'version' => '0.1'
                ]
            ]
        ]);

        if ($response->header('mcp-session-id')) {
            $this->sessionId = $response->header('mcp-session-id');
            Log::info("McpExecutionTool: Sessão iniciada", ['session_id' => $this->sessionId]);
        }

        // Envia notificação initialized
        $headers = [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json, text/event-stream'
        ];
        if ($this->sessionId) {
            $headers['Mcp-Session-Id'] = $this->sessionId;
        }

        Http::withHeaders($headers)
            ->post($url, [
                'jsonrpc' => '2.0',
                'method' => 'notifications/initialized'
            ]);
    }
}
