<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

class McpValidateSqlTool extends Tool
{
    protected McpClient $mcpClient;

    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('mcp_validate_sql')
            ->for('Valida estaticamente uma query SQL usando EXPLAIN no PostgreSQL para verificar sintaxe, schema e joins antes de executa-la realmente. Sempre use esta ferramenta antes da execucao se estiver com duvida sobre a validade das colunas ou joins.')
            ->withStringParameter('sql', 'A query SQL a ser validada.')
            ->using(fn (string $sql) => $this->execute($sql));
    }

    protected function execute(string $sql): string
    {
        Log::info('McpValidateSqlTool: Validando SQL via EXPLAIN...', ['sql' => $sql]);

        return $this->mcpClient->callTool('ecidade_validate_sql_explain', [
            'sql' => $sql,
        ]);
    }
}
