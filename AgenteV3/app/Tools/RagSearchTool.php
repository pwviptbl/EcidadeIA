<?php

namespace App\Tools;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Tool;

/**
 * Ferramenta de busca semântica no catálogo RAG do e-Cidade via servidor MCP.
 *
 * Substitui a busca ingênua por arquivos .md locais, delegando a pesquisa
 * para a tool 'ecidade_catalog_search' no servidor MCP, que combina catálogo
 * estruturado, documentos RAG, scoring textual e sinônimos de domínio.
 */
class RagSearchTool extends Tool
{
    /** @var McpClient Cliente MCP compartilhado */
    protected McpClient $mcpClient;

    /**
     * Inicializa a ferramenta 'rag_search'.
     * Define o nome, descrição e o parâmetro esperado pela LLM (query).
     *
     * @param McpClient $mcpClient Cliente MCP injetado pelo container.
     */
    public function __construct(McpClient $mcpClient)
    {
        $this->mcpClient = $mcpClient;

        $this->as('rag_search')
            ->for('Pesquisa regras de negócio, esquemas de tabelas e relacionamentos específicos do e-Cidade no repositório de conhecimento (RAG) utilizando busca semântica. Retorna documentos relevantes do catálogo.')
            ->withStringParameter('query', 'Termo de busca ou nome da tabela a ser pesquisada (ex: iptuisen, arrepaga, bairro_para_imoveis).')
            ->using(fn (string $query) => $this->search($query));
    }

    /**
     * Executa a busca semântica no catálogo RAG via MCP.
     *
     * @param string $query Termo ou nome de tabela buscado.
     * @return string Resposta do MCP contendo os documentos encontrados.
     */
    protected function search(string $query): string
    {
        Log::info('RagSearchTool: Pesquisando por...', ['query' => $query]);

        return $this->mcpClient->callTool('ecidade_catalog_search', [
            'text' => $query,
            'limit' => 10,
        ]);
    }
}
