<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta para listar os schemas autorizados no banco do e-Cidade via MCP.
 *
 * Permite ao agente descobrir quais módulos (schemas) estão disponíveis
 * antes de explorar tabelas ou montar queries.
 */
class McpListSchemasTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'ecidade_list_schemas'.
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('ecidade_list_schemas')
            ->for('Lista os schemas autorizados no banco e-Cidade. Use para descobrir quais módulos estão disponíveis.')
            ->using(fn () => $this->listSchemas());
    }

    /**
     * Solicita a lista de schemas ao servidor MCP.
     *
     * @return string Resposta do MCP com os schemas disponíveis.
     */
    protected function listSchemas(): string
    {
        Log::info('McpListSchemasTool: Listando schemas disponíveis...');

        return $this->mcpClient->callTool('ecidade_list_schemas', []);
    }
}
