<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta para descrever a estrutura de uma tabela do e-Cidade via MCP.
 *
 * Retorna as colunas reais do banco de dados junto com metadados do catálogo.
 * Essencial para o agente validar nomes de colunas antes de montar queries SQL.
 */
class McpDescribeTableTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'ecidade_describe_table'.
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('ecidade_describe_table')
            ->for('Descreve a estrutura de uma tabela do e-Cidade. Retorna colunas reais do banco + metadados do catálogo. Use ANTES de montar SQL para confirmar nomes de colunas.')
            ->withStringParameter('schema', 'Nome do schema da tabela (ex: cadastro, protocolo, compras)')
            ->withStringParameter('table', 'Nome da tabela (ex: bairro, cgm, processo)')
            ->using(fn (string $schema, string $table) => $this->describeTable($schema, $table));
    }

    /**
     * Solicita a descrição da tabela ao servidor MCP.
     *
     * @param string $schema Nome do schema.
     * @param string $table  Nome da tabela.
     * @return string Resposta do MCP com a estrutura da tabela.
     */
    protected function describeTable(string $schema, string $table): string
    {
        Log::info('McpDescribeTableTool: Descrevendo tabela...', [
            'schema' => $schema,
            'table' => $table,
        ]);

        return $this->mcpClient->callTool('ecidade_describe_table', [
            'schema' => $schema,
            'table' => $table,
        ]);
    }
}
