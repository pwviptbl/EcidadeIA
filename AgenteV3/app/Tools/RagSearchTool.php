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
        
        // Remove pontuações comuns e divide em termos individuais
        $terms = array_filter(preg_split('/[\s\-_,.]+/', $queryNormalized), function($term) {
            return strlen($term) >= 2;
        });

        if (empty($terms)) {
            $terms = [$queryNormalized];
        }

        $results = [];
        $directoryIterator = new \RecursiveDirectoryIterator($baseDir);
        $iterator = new \RecursiveIteratorIterator($directoryIterator);

        foreach ($iterator as $file) {
            if ($file->isFile() && $file->getExtension() === 'md') {
                $filename = strtolower($file->getBasename('.md'));
                $pathname = $file->getPathname();
                $content = file_get_contents($pathname);
                $contentLower = strtolower($content);

                $matchedFilenameTerms = 0;
                $matchedContentTerms = 0;
                $matchingLines = [];

                foreach ($terms as $term) {
                    if (strpos($filename, $term) !== false) {
                        $matchedFilenameTerms++;
                    }
                    if (strpos($contentLower, $term) !== false) {
                        $matchedContentTerms++;
                    }
                }

                // Se houver qualquer correspondência
                if ($matchedFilenameTerms > 0 || $matchedContentTerms > 0) {
                    $lines = explode("\n", $content);
                    foreach ($lines as $line) {
                        foreach ($terms as $term) {
                            if (stripos($line, $term) !== false) {
                                $matchingLines[] = trim($line);
                                break;
                            }
                        }
                    }

                    // Calcula score de relevância
                    $score = ($matchedFilenameTerms * 10) + $matchedContentTerms;
                    
                    // Boost para correspondência exata do nome do arquivo
                    foreach ($terms as $term) {
                        if ($filename === $term) {
                            $score += 50;
                        }
                    }

                    // Boost enorme se encontrar receitas de relacionamentos de negócio
                    if (strpos($filename, 'relacionamentos_negocio') !== false) {
                        $score += 30;
                    }

                    $results[] = [
                        'score' => $score,
                        'file' => $pathname,
                        'title' => $file->getBasename(),
                        'content' => $content,
                        'matching_lines' => $matchingLines
                    ];
                }
            }
        }

        if (empty($results)) {
            return json_encode([
                'message' => "Nenhuma correspondência encontrada para '{$query}'. Tente usar termos mais genéricos como 'iptu', 'caixa', 'bairro', ou nomes de tabelas."
            ]);
        }

        // Ordena por score decrescente
        usort($results, function($a, $b) {
            return $b['score'] <=> $a['score'];
        });

        // Pega no máximo os 5 resultados mais relevantes
        $topResults = array_slice($results, 0, 5);
        $formattedResults = [];

        foreach ($topResults as $res) {
            // Se tiver um score mínimo de relevância, retorna conteúdo integral. Caso contrário, retorna snippets de linhas
            if ($res['score'] >= 25) {
                $formattedResults[] = [
                    'file' => $res['file'],
                    'title' => $res['title'],
                    'content' => $res['content']
                ];
            } else {
                $formattedResults[] = [
                    'file' => $res['file'],
                    'title' => $res['title'],
                    'snippet' => implode("\n", array_slice(array_unique($res['matching_lines']), 0, 10))
                ];
            }
        }

        return json_encode($formattedResults, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
    }
}
