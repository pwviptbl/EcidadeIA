<?php

namespace App\Tools;

use Prism\Prism\Tool;
use Illuminate\Support\Facades\Log;

class RagSearchTool extends Tool
{
    /**
     * Inicializa a ferramenta 'rag_search'.
     * Define o nome, descrição e o parâmetro esperado pela LLM (query).
     */
    public function __construct()
    {
        $this->as('rag_search')
            ->for('Pesquisa regras de negócio, esquemas de tabelas e relacionamentos específicos do e-Cidade no repositório de conhecimento (RAG) utilizando termos chave (ex: iptuisen, bairro, caixas, etc).')
            ->withStringParameter('query', 'Termo de busca ou nome da tabela a ser pesquisada (ex: iptuisen, arrepaga, bairro_para_imoveis).')
            ->using(fn (string $query) => $this->search($query));
    }

    /**
     * Varre o diretório de conhecimento do RAG buscando o termo informado.
     * Se houver correspondência exata no nome do arquivo, retorna o conteúdo integral.
     * Caso contrário, busca dentro do arquivo e retorna um "snippet" das linhas relacionadas.
     *
     * @param string $query Termo ou nome de tabela buscado.
     * @return string JSON encodado contendo os resultados da busca (snippets ou conteúdo integral).
     */
    protected function search(string $query): string
    {
        Log::info("RagSearchTool: Pesquisando por...", ['query' => $query]);

        $baseDir = env('RAG_KNOWLEDGE_PATH', '/home/dbseller/Modelos/MVP/knowledge/rag');
        $queryNormalized = strtolower(trim($query));

        $results = [];
        $directoryIterator = new \RecursiveDirectoryIterator($baseDir);
        $iterator = new \RecursiveIteratorIterator($directoryIterator);

        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getExtension() === 'md') {
                $filename = strtolower($file->getBasename('.md'));
                
                if (strpos($filename, $queryNormalized) !== false) {
                    $content = file_get_contents($file->getPathname());
                    $results[] = [
                        'file' => $file->getPathname(),
                        'title' => $file->getBasename(),
                        'content' => $content
                    ];
                }
            }
        }

        if (empty($results)) {
            foreach ($iterator as $file) {
                if ($file->isFile() && $file->getExtension() === 'md') {
                    $content = file_get_contents($file->getPathname());
                    if (stripos($content, $queryNormalized) !== false) {
                        $lines = explode("\n", $content);
                        $matchingLines = [];
                        foreach ($lines as $line) {
                            if (stripos($line, $queryNormalized) !== false) {
                                $matchingLines[] = trim($line);
                            }
                        }
                        $results[] = [
                            'file' => $file->getPathname(),
                            'title' => $file->getBasename(),
                            'snippet' => implode("\n", array_slice($matchingLines, 0, 10))
                        ];
                    }
                }
            }
        }

        if (empty($results)) {
            return json_encode([
                'message' => "Nenhuma correspondência exata encontrada para '{$query}'. Tente usar termos mais genéricos como 'iptu', 'caixa', 'bairro', ou nomes de tabelas."
            ]);
        }

        return json_encode($results, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    }
}
