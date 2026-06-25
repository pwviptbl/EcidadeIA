<?php

namespace App\Services\Mcp;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

/**
 * Cliente MCP reutilizável para comunicação JSON-RPC 2.0 com o servidor MCP do e-Cidade.
 *
 * Responsável pelo handshake de inicialização (initialize + notifications/initialized),
 * gerenciamento do session ID e invocação genérica de qualquer tool registrada no servidor MCP.
 *
 * Projetado para ser registrado como singleton no container do Laravel.
 */
class McpClient
{
    /** @var string|null ID da sessão MCP ativa */
    protected ?string $sessionId = null;

    /** @var int Contador incremental para IDs de requisição JSON-RPC */
    protected int $nextId = 1;

    /**
     * Invoca uma tool no servidor MCP pelo nome, passando os argumentos fornecidos.
     *
     * Garante que a sessão está inicializada antes de executar a chamada.
     * Em caso de falha HTTP ou exceção, retorna uma string JSON com o erro — nunca lança exceção.
     *
     * @param string $toolName Nome da tool registrada no servidor MCP (ex: 'ecidade_readonly_query').
     * @param array  $arguments Argumentos a serem passados para a tool.
     * @return string Conteúdo textual extraído da resposta JSON-RPC ou string JSON de erro.
     */
    public function callTool(string $toolName, array $arguments): string
    {
        Log::info("McpClient: Chamando tool '{$toolName}'", ['arguments' => $arguments]);

        try {
            $url = config('services.mcp.url', 'http://host.docker.internal:8010/mcp');
            $timeout = (int) config('services.mcp.timeout', 30);

            $this->ensureSession($url, $timeout);

            $requestId = $this->nextId++;

            $headers = $this->buildHeaders();

            $response = Http::withHeaders($headers)
                ->timeout($timeout)
                ->post($url, [
                    'jsonrpc' => '2.0',
                    'id' => $requestId,
                    'method' => 'tools/call',
                    'params' => [
                        'name' => $toolName,
                        'arguments' => $arguments,
                    ],
                ]);

            if ($response->failed()) {
                Log::error("McpClient: Falha na chamada da tool '{$toolName}'", [
                    'status' => $response->status(),
                    'body' => $response->body(),
                ]);

                return json_encode([
                    'error' => true,
                    'message' => "Erro ao chamar '{$toolName}' no MCP: " . $response->body(),
                ]);
            }

            return $this->extractTextContent($response->json(), $response->body());
        } catch (\Exception $e) {
            Log::error("McpClient: Exceção ao chamar '{$toolName}'", [
                'error' => $e->getMessage(),
            ]);

            return json_encode([
                'error' => true,
                'message' => "Falha de comunicação com o servidor MCP: {$e->getMessage()}",
            ]);
        }
    }

    /**
     * Garante que a sessão MCP esteja inicializada.
     *
     * Executa o handshake JSON-RPC: envia 'initialize' com protocolVersion e capabilities,
     * captura o header 'Mcp-Session-Id' e envia 'notifications/initialized'.
     *
     * @param string $url     URL do servidor MCP.
     * @param int    $timeout Timeout HTTP em segundos.
     */
    protected function ensureSession(string $url, int $timeout): void
    {
        if ($this->sessionId) {
            return;
        }

        Log::info('McpClient: Inicializando nova sessão MCP');

        $baseHeaders = [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json, text/event-stream',
        ];

        $response = Http::withHeaders($baseHeaders)
            ->timeout($timeout)
            ->post($url, [
                'jsonrpc' => '2.0',
                'id' => $this->nextId++,
                'method' => 'initialize',
                'params' => [
                    'protocolVersion' => '2025-06-18',
                    'capabilities' => (object) [],
                    'clientInfo' => [
                        'name' => 'agente-v3',
                        'version' => '0.1',
                    ],
                ],
            ]);

        if ($response->header('mcp-session-id')) {
            $this->sessionId = $response->header('mcp-session-id');
            Log::info('McpClient: Sessão iniciada', ['session_id' => $this->sessionId]);
        }

        // Envia notificação de sessão inicializada
        $headers = $baseHeaders;
        if ($this->sessionId) {
            $headers['Mcp-Session-Id'] = $this->sessionId;
        }

        Http::withHeaders($headers)
            ->timeout($timeout)
            ->post($url, [
                'jsonrpc' => '2.0',
                'method' => 'notifications/initialized',
            ]);
    }

    /**
     * Monta os headers HTTP padrão para requisições ao MCP.
     *
     * Inclui o Mcp-Session-Id quando disponível.
     *
     * @return array<string, string> Headers HTTP.
     */
    protected function buildHeaders(): array
    {
        $headers = [
            'Content-Type' => 'application/json',
            'Accept' => 'application/json, text/event-stream',
        ];

        if ($this->sessionId) {
            $headers['Mcp-Session-Id'] = $this->sessionId;
        }

        return $headers;
    }

    /**
     * Extrai o conteúdo textual da resposta JSON-RPC.
     *
     * Percorre o array 'result.content' e concatena todos os campos 'text' encontrados.
     * Se nenhum texto for extraído, retorna o body bruto da resposta.
     *
     * @param array|null $responseData Dados decodificados da resposta JSON-RPC.
     * @param string     $rawBody      Body bruto da resposta HTTP (fallback).
     * @return string Conteúdo textual extraído.
     */
    protected function extractTextContent(?array $responseData, string $rawBody): string
    {
        $contentArray = data_get($responseData, 'result.content', []);
        $textResult = '';

        foreach ($contentArray as $item) {
            if (is_array($item) && isset($item['text'])) {
                $textResult .= $item['text'];
            }
        }

        return $textResult ?: $rawBody;
    }
}
