<?php

namespace App\Services\Agent;

/**
 * Cache de metadados de schema com escopo de sessão para o E-CidadeIA.
 *
 * Armazena informações de estrutura de tabelas descobertas durante o loop
 * agentivo, evitando chamadas redundantes ao MCP (ecidade_describe_table)
 * para tabelas já inspecionadas na mesma sessão.
 *
 * Implementa evição FIFO quando o número máximo de entradas é atingido.
 */
class SchemaCache
{
    /**
     * Armazenamento interno do cache.
     *
     * Estrutura: ['schema.table' => array{metadata: array, cached_at: float}]
     *
     * @var array<string, array{metadata: array, cached_at: float}>
     */
    private array $cache = [];

    /**
     * Número máximo de entradas no cache antes da evição FIFO.
     */
    private int $maxEntries;

    /**
     * Cria uma nova instância do cache de schemas.
     *
     * @param int $maxEntries Limite máximo de tabelas cacheadas.
     */
    public function __construct(int $maxEntries = 50)
    {
        $this->maxEntries = $maxEntries;
    }

    /**
     * Recupera os metadados cacheados de uma tabela.
     *
     * @param string $schema Nome do schema.
     * @param string $table  Nome da tabela.
     * @return array|null Metadados da tabela ou null se não cacheado.
     */
    public function get(string $schema, string $table): ?array
    {
        $key = $this->buildKey($schema, $table);

        if (!isset($this->cache[$key])) {
            return null;
        }

        return $this->cache[$key]['metadata'];
    }

    /**
     * Armazena metadados de uma tabela no cache.
     *
     * Aplica evição FIFO (remove a entrada mais antiga) quando o cache
     * atinge o limite máximo de entradas.
     *
     * @param string $schema   Nome do schema.
     * @param string $table    Nome da tabela.
     * @param array  $metadata Metadados da tabela (colunas, tipos, PKs, FKs, etc.).
     */
    public function set(string $schema, string $table, array $metadata): void
    {
        $key = $this->buildKey($schema, $table);

        // Evição FIFO: remove a entrada mais antiga se o cache está cheio
        if (!isset($this->cache[$key]) && count($this->cache) >= $this->maxEntries) {
            // array_key_first retorna a chave mais antiga (inserida primeiro)
            $oldestKey = array_key_first($this->cache);
            if ($oldestKey !== null) {
                unset($this->cache[$oldestKey]);
            }
        }

        $this->cache[$key] = [
            'metadata'  => $metadata,
            'cached_at' => microtime(true),
        ];
    }

    /**
     * Verifica se uma tabela possui metadados no cache.
     *
     * @param string $schema Nome do schema.
     * @param string $table  Nome da tabela.
     * @return bool True se a tabela está cacheada.
     */
    public function has(string $schema, string $table): bool
    {
        return isset($this->cache[$this->buildKey($schema, $table)]);
    }

    /**
     * Gera um resumo textual de todos os schemas descobertos na sessão.
     *
     * Formato de saída:
     * ```
     * [Schemas já descobertos nesta sessão:]
     * - schema.tabela: coluna1 (tipo), coluna2 (tipo, PK), ...
     * ```
     *
     * Limita a 10 colunas por tabela para economia de tokens.
     * Anota colunas PK e FK quando detectáveis nos metadados.
     *
     * @return string Contexto textual dos schemas cacheados (vazio se cache vazio).
     */
    public function buildSchemaContext(): string
    {
        if (empty($this->cache)) {
            return '';
        }

        $lines = ['[Schemas já descobertos nesta sessão:]'];

        foreach ($this->cache as $key => $entry) {
            $metadata = $entry['metadata'];
            $columns  = $this->extractColumns($metadata);

            // Limita a 10 colunas por tabela
            $truncated    = false;
            $totalColumns = count($columns);

            if ($totalColumns > 10) {
                $columns   = array_slice($columns, 0, 10);
                $truncated = true;
            }

            $columnDescriptions = [];

            foreach ($columns as $column) {
                $name = $column['name'] ?? $column['column_name'] ?? 'desconhecido';
                $type = $column['type'] ?? $column['data_type'] ?? $column['udt_name'] ?? '?';

                $annotations = [];

                // Detecta chave primária
                if ($this->isPrimaryKey($column)) {
                    $annotations[] = 'PK';
                }

                // Detecta chave estrangeira
                if ($this->isForeignKey($column)) {
                    $annotations[] = 'FK';
                }

                $desc = "{$name} ({$type}";

                if (!empty($annotations)) {
                    $desc .= ', ' . implode(', ', $annotations);
                }

                $desc .= ')';
                $columnDescriptions[] = $desc;
            }

            $line = "- {$key}: " . implode(', ', $columnDescriptions);

            if ($truncated) {
                $remaining = $totalColumns - 10;
                $line .= " ... [+{$remaining} colunas]";
            }

            $lines[] = $line;
        }

        return implode("\n", $lines);
    }

    /**
     * Retorna a quantidade de tabelas atualmente no cache.
     *
     * @return int Número de entradas no cache.
     */
    public function count(): int
    {
        return count($this->cache);
    }

    /**
     * Limpa todo o cache, removendo todos os metadados armazenados.
     */
    public function clear(): void
    {
        $this->cache = [];
    }

    /**
     * Constrói a chave interna do cache a partir de schema e tabela.
     *
     * @param string $schema Nome do schema.
     * @param string $table  Nome da tabela.
     * @return string Chave no formato 'schema.tabela'.
     */
    private function buildKey(string $schema, string $table): string
    {
        return mb_strtolower($schema, 'UTF-8') . '.' . mb_strtolower($table, 'UTF-8');
    }

    /**
     * Extrai o array de colunas dos metadados, independente do formato recebido.
     *
     * Suporta metadados no formato:
     * - ['columns' => [...]]
     * - [['name' => ..., 'type' => ...], ...]
     * - ['column_name' => 'tipo', ...]
     *
     * @param array $metadata Metadados da tabela.
     * @return array<int, array{name?: string, column_name?: string, type?: string, data_type?: string}> Lista de colunas.
     */
    private function extractColumns(array $metadata): array
    {
        // Formato padrão: ['columns' => [...]]
        if (isset($metadata['columns']) && is_array($metadata['columns'])) {
            return $metadata['columns'];
        }

        // Formato alternativo: array indexado de arrays associativos
        if (array_is_list($metadata) && !empty($metadata) && is_array($metadata[0])) {
            return $metadata;
        }

        // Formato simplificado: ['coluna' => 'tipo', ...]
        $columns = [];
        foreach ($metadata as $key => $value) {
            if (is_string($key) && is_string($value)) {
                $columns[] = ['name' => $key, 'type' => $value];
            }
        }

        return $columns;
    }

    /**
     * Verifica se uma coluna é chave primária com base nos metadados disponíveis.
     *
     * @param array $column Dados da coluna.
     * @return bool True se a coluna é identificada como PK.
     */
    private function isPrimaryKey(array $column): bool
    {
        // Campo explícito 'is_pk' ou 'primary_key'
        if (!empty($column['is_pk']) || !empty($column['primary_key'])) {
            return true;
        }

        // Campo 'constraint_type' indicando PRIMARY KEY
        if (isset($column['constraint_type'])) {
            return mb_strtoupper($column['constraint_type'], 'UTF-8') === 'PRIMARY KEY';
        }

        return false;
    }

    /**
     * Verifica se uma coluna é chave estrangeira com base nos metadados disponíveis.
     *
     * @param array $column Dados da coluna.
     * @return bool True se a coluna é identificada como FK.
     */
    private function isForeignKey(array $column): bool
    {
        // Campo explícito 'is_fk' ou 'foreign_key'
        if (!empty($column['is_fk']) || !empty($column['foreign_key'])) {
            return true;
        }

        // Campo 'constraint_type' indicando FOREIGN KEY
        if (isset($column['constraint_type'])) {
            return mb_strtoupper($column['constraint_type'], 'UTF-8') === 'FOREIGN KEY';
        }

        // Referência a tabela externa presente
        if (!empty($column['references_table']) || !empty($column['foreign_table'])) {
            return true;
        }

        return false;
    }
}
