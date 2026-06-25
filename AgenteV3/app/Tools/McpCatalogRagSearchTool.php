<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta de busca RAG tipada no catálogo do e-Cidade via MCP.
 *
 * Diferente da busca genérica (rag_search), esta ferramenta permite filtrar
 * por tipo de documento (kinds): validated_query, business_concept,
 * relationship_recipe, counting_rule, business_filter, etc.
 */
class McpCatalogRagSearchTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'ecidade_catalog_rag_search'.
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('ecidade_catalog_rag_search')
            ->for('Busca documentos específicos no RAG do e-Cidade por tipo (validated_query, business_concept, relationship_recipe, counting_rule, business_filter, etc). Use para encontrar regras de negócio e queries validadas.')
            ->withStringParameter('text', 'Texto de busca semântica para encontrar documentos relevantes')
            ->withStringParameter('kinds', 'Filtro opcional de tipos de documento separados por vírgula (ex: validated_query,business_concept). Deixe vazio para buscar todos os tipos.')
            ->using(fn (string $text, string $kinds = '') => $this->searchCatalog($text, $kinds));
    }

    /**
     * Executa a busca RAG tipada no catálogo via MCP.
     *
     * Converte a string de kinds separada por vírgula em array.
     * Se nenhum kind for informado, passa null para buscar todos os tipos.
     *
     * @param string $text  Texto de busca semântica.
     * @param string $kinds Tipos de documento separados por vírgula (opcional).
     * @return string Resposta do MCP com os documentos encontrados.
     */
    protected function searchCatalog(string $text, string $kinds = ''): string
    {
        $kindsArray = null;

        if (trim($kinds) !== '') {
            $kindsArray = array_map('trim', explode(',', $kinds));
            $kindsArray = array_filter($kindsArray, fn (string $k) => $k !== '');
            $kindsArray = array_values($kindsArray);
        }

        Log::info('McpCatalogRagSearchTool: Pesquisando catálogo...', [
            'text' => $text,
            'kinds' => $kindsArray,
        ]);

        $arguments = [
            'text' => $text,
            'limit' => 10,
        ];

        if ($kindsArray !== null) {
            $arguments['kinds'] = $kindsArray;
        }

        return $this->mcpClient->callTool('ecidade_catalog_rag_search', $arguments);
    }
}
