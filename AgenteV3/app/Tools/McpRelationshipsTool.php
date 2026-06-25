<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta para descobrir relacionamentos entre tabelas do e-Cidade via MCP.
 *
 * Retorna FKs e caminhos semânticos de JOIN entre as tabelas informadas.
 * Permite ao agente montar JOINs corretos sem adivinhar.
 */
class McpRelationshipsTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'ecidade_get_relationships'.
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('ecidade_get_relationships')
            ->for('Retorna relacionamentos (FK e caminhos semânticos) entre tabelas do e-Cidade. Use para descobrir JOINs corretos. Passe as tabelas separadas por vírgula (ex: cadastro.bairro,cadastro.cgm).')
            ->withStringParameter('tables', 'Lista de tabelas no formato schema.tabela separadas por vírgula (ex: cadastro.bairro,cadastro.cgm)')
            ->using(fn (string $tables) => $this->getRelationships($tables));
    }

    /**
     * Consulta os relacionamentos entre as tabelas informadas via MCP.
     *
     * Converte a string de tabelas separadas por vírgula em array antes de enviar.
     *
     * @param string $tables Tabelas separadas por vírgula (ex: 'cadastro.bairro,cadastro.cgm').
     * @return string Resposta do MCP com os relacionamentos encontrados.
     */
    protected function getRelationships(string $tables): string
    {
        $tablesArray = array_map('trim', explode(',', $tables));
        $tablesArray = array_filter($tablesArray, fn (string $t) => $t !== '');

        Log::info('McpRelationshipsTool: Buscando relacionamentos...', [
            'tables' => $tablesArray,
        ]);

        return $this->mcpClient->callTool('ecidade_get_relationships', [
            'tables' => $tablesArray,
        ]);
    }
}
