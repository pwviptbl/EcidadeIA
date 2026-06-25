<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta de execução SQL read-only via servidor MCP.
 *
 * Recebe uma query SQL gerada pelo LLM e a envia para a tool 'ecidade_readonly_query'
 * no servidor MCP. Retorna os registros resultantes em formato textual.
 */
class McpExecutionTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'mcp_execute_sql'.
     * Define o nome, descrição e o parâmetro esperado (sql).
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('mcp_execute_sql')
            ->for('Executa uma consulta SQL read-only no banco de dados do e-Cidade através do servidor MCP. Retorna os registros resultantes.')
            ->withStringParameter('sql', 'A query SQL a ser executada. A query deve ser estritamente de leitura (SELECT)')
            ->using(fn (string $sql) => $this->execute($sql));
    }

    /**
     * Empacota a query SQL gerada pelo LLM e delega a execução ao McpClient.
     *
     * @param string $sql A consulta SQL a ser executada.
     * @return string Resultado da consulta ou mensagem de erro em JSON.
     */
    protected function execute(string $sql): string
    {
        Log::info('McpExecutionTool: Executando SQL...', ['sql' => $sql]);

        return $this->mcpClient->callTool('ecidade_readonly_query', [
            'sql' => $sql,
            'limit' => 1000,
        ]);
    }
}
