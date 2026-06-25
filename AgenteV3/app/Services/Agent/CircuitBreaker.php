<?php

namespace App\Services\Agent;

/**
 * Circuit Breaker para o loop agentivo do E-CidadeIA.
 *
 * Detecta padrões de erros repetidos (mesma ferramenta falhando da mesma forma)
 * e sugere mudanças de estratégia antes que o agente esgote seus passos em loop
 * improdutivo. O circuito "abre" quando N erros similares consecutivos são
 * detectados e "fecha" automaticamente ao registrar um sucesso.
 */
class CircuitBreaker
{
    /**
     * Histórico de erros registrados durante a sessão.
     *
     * Cada entrada contém: tool, message, pattern, args, timestamp.
     *
     * @var array<int, array{tool: string, message: string, pattern: string, args: array, timestamp: float}>
     */
    private array $errorHistory = [];

    /**
     * Quantidade máxima de erros similares consecutivos antes de acionar o circuit breaker.
     */
    private int $maxSimilarErrors;

    /**
     * Cria uma nova instância do CircuitBreaker.
     *
     * @param int $maxSimilarErrors Limite de erros similares antes de "abrir" o circuito.
     */
    public function __construct(int $maxSimilarErrors = 3)
    {
        $this->maxSimilarErrors = $maxSimilarErrors;
    }

    /**
     * Registra um erro ocorrido durante a execução de uma ferramenta.
     *
     * @param string $toolName    Nome da ferramenta que falhou.
     * @param string $errorMessage Mensagem de erro retornada.
     * @param array  $args         Argumentos passados à ferramenta (para diagnóstico).
     */
    public function recordError(string $toolName, string $errorMessage, array $args = []): void
    {
        $this->errorHistory[] = [
            'tool'      => $toolName,
            'message'   => $errorMessage,
            'pattern'   => $this->extractPattern($toolName, $errorMessage),
            'args'      => $args,
            'timestamp' => microtime(true),
        ];
    }

    /**
     * Verifica se o circuito deve ser aberto (interromper a estratégia atual).
     *
     * Retorna true se os últimos N erros possuem o mesmo padrão normalizado,
     * indicando que o agente está repetindo a mesma falha.
     *
     * @return bool True se o circuit breaker deve ser acionado.
     */
    public function shouldBreak(): bool
    {
        $count = count($this->errorHistory);

        if ($count < $this->maxSimilarErrors) {
            return false;
        }

        $lastErrors = array_slice($this->errorHistory, -$this->maxSimilarErrors);
        $patterns   = array_column($lastErrors, 'pattern');

        return count(array_unique($patterns)) === 1;
    }

    /**
     * Retorna uma sugestão de estratégia baseada no tipo do último erro registrado.
     *
     * A sugestão orienta o agente a tomar uma abordagem diferente para evitar
     * repetir o mesmo padrão de falha.
     *
     * @return string Texto de sugestão de estratégia em PT-BR.
     */
    public function getSuggestedStrategy(): string
    {
        if (empty($this->errorHistory)) {
            return 'Faça nova busca RAG com termos diferentes e tente uma abordagem alternativa.';
        }

        $lastError  = end($this->errorHistory);
        $lowerMsg   = strtolower($lastError['message']);

        if (str_contains($lowerMsg, 'allowlist') || str_contains($lowerMsg, 'catalogo')) {
            return 'Busque tabela alternativa via rag_search com termos diferentes. O schema/tabela atual não está na allowlist.';
        }

        if (str_contains($lowerMsg, 'column') || str_contains($lowerMsg, 'coluna')) {
            return 'Use ecidade_describe_table para verificar as colunas reais da tabela antes de montar o SQL.';
        }

        if (str_contains($lowerMsg, 'permission') || str_contains($lowerMsg, 'permissão')) {
            return 'O domínio solicitado não está disponível. Informe ao usuário e sugira schemas alternativos via ecidade_list_schemas.';
        }

        if (str_contains($lowerMsg, 'timeout')) {
            return 'A query é muito pesada. Simplifique: reduza JOINs, adicione filtros, use LIMIT menor.';
        }

        if (str_contains($lowerMsg, 'syntax') || str_contains($lowerMsg, 'sintaxe')) {
            return 'Erro de sintaxe SQL. Revise a query completa antes de reenviar.';
        }

        return 'Faça nova busca RAG com termos diferentes e tente uma abordagem alternativa.';
    }

    /**
     * Registra um sucesso, fechando o circuito e limpando o histórico de erros.
     *
     * Chamado após uma execução bem-sucedida de ferramenta para resetar
     * o estado do circuit breaker.
     */
    public function recordSuccess(): void
    {
        $this->errorHistory = [];
    }

    /**
     * Retorna um resumo do histórico de erros para logging e diagnóstico.
     *
     * @return array{total_errors: int, unique_patterns: int, last_error: ?array{tool: string, message: string, timestamp: float}, is_open: bool}
     */
    public function getErrorSummary(): array
    {
        $patterns = array_column($this->errorHistory, 'pattern');

        return [
            'total_errors'    => count($this->errorHistory),
            'unique_patterns' => count(array_unique($patterns)),
            'last_error'      => !empty($this->errorHistory) ? [
                'tool'      => end($this->errorHistory)['tool'],
                'message'   => end($this->errorHistory)['message'],
                'timestamp' => end($this->errorHistory)['timestamp'],
            ] : null,
            'is_open'         => $this->shouldBreak(),
        ];
    }

    /**
     * Extrai um padrão normalizado de erro para comparação.
     *
     * Normaliza a mensagem substituindo nomes de tabelas (schema.tabela)
     * por 'TABLE' e números por 'N', permitindo agrupar erros semanticamente
     * idênticos mesmo com parâmetros diferentes.
     *
     * @param string $tool  Nome da ferramenta.
     * @param string $error Mensagem de erro original.
     * @return string Hash MD5 do padrão normalizado.
     */
    private function extractPattern(string $tool, string $error): string
    {
        // Substitui padrões schema.tabela por 'TABLE'
        $normalized = preg_replace('/\b[a-z_]+\.[a-z_]+\b/i', 'TABLE', $error);

        // Substitui sequências numéricas por 'N'
        $normalized = preg_replace('/\b\d+\b/', 'N', $normalized);

        return md5($tool . '::' . $normalized);
    }
}
