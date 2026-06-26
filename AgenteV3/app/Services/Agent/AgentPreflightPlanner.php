<?php

namespace App\Services\Agent;

use App\Services\Mcp\McpClient;
use Illuminate\Support\Facades\Log;
use Prism\Prism\Enums\Provider;
use Prism\Prism\Facades\Prism;
use Prism\Prism\ValueObjects\Messages\UserMessage;

class AgentPreflightPlanner
{
    public function __construct(
        private readonly McpClient $mcpClient
    ) {
    }

    /**
     * Executa subagentes lógicos antes do loop SQL:
     * Router, EvidenceSearch, QuerySpec, Critic, SearchRepair e votação de rota.
     *
     * @return array<string, mixed>
     */
    public function plan(string $question): array
    {
        $evidence = $this->collectEvidence($question, $this->buildSearchQueries($question));
        $answerOnly = $this->isAnswerOnlyQuestion($question);

        if (! $this->hasUsableEvidence($evidence)) {
            $plan = [
                'routes' => [],
                'selected_route_index' => null,
                'query_spec' => [
                    'missing_requirements' => ['Nenhuma evidência útil retornada pelo MCP/catalogo/RAG.'],
                ],
                'critic' => [
                    'approved_for_sql' => false,
                    'reason' => 'Não há evidência de catálogo/RAG suficiente para montar rota ou SQL.',
                    'required_repairs' => ['Verificar servidor MCP, índice RAG e termos de busca para esta pergunta.'],
                ],
                'search_repairs' => [],
            ];

            return [
                'approved' => false,
                'phase' => 'preflight',
                'question' => $question,
                'evidence' => $evidence,
                'plan' => $plan,
                'context' => $this->buildContext($question, $plan, $evidence, false),
                'answer_if_blocked' => $this->buildBlockedAnswer($plan, $evidence),
            ];
        }

        if ($answerOnly) {
            $plan = $this->buildAnswerOnlyPlan($question, $evidence);

            return [
                'approved' => false,
                'phase' => 'preflight-answer-only',
                'question' => $question,
                'evidence' => $evidence,
                'plan' => $plan,
                'context' => $this->buildContext($question, $plan, $evidence, false),
                'answer_if_blocked' => $this->buildKnowledgeAnswer($question, $plan, $evidence),
            ];
        }

        $plan = $this->askPlanner($question, $evidence, []);

        if (! $this->isApproved($plan)) {
            $repairs = $this->repairQueries($plan);
            if (! empty($repairs)) {
                $repairEvidence = $this->collectEvidence($question, $repairs);
                $evidence = array_merge($evidence, $repairEvidence);
                $plan = $this->askPlanner($question, $evidence, $repairs);
            }
        }

        $approved = $this->isApproved($plan);
        $intent = data_get($plan, 'query_spec.intent');

        if (! $approved && $intent === 'conhecimento') {
            return [
                'approved' => false,
                'phase' => 'preflight-answer-only',
                'question' => $question,
                'evidence' => $evidence,
                'plan' => $plan,
                'context' => $this->buildContext($question, $plan, $evidence, false),
                'answer_if_blocked' => $this->buildKnowledgeAnswer($question, $plan, $evidence),
            ];
        }

        return [
            'approved' => $approved,
            'phase' => 'preflight',
            'question' => $question,
            'evidence' => $evidence,
            'plan' => $plan,
            'context' => $this->buildContext($question, $plan, $evidence, $approved),
            'answer_if_blocked' => $approved ? null : $this->buildBlockedAnswer($plan, $evidence),
        ];
    }

    /**
     * @return array<int, string>
     */
    private function buildSearchQueries(string $question): array
    {
        $normalized = strtolower($question);
        $queries = [$question];

        $domainHints = [
            'iptu' => 'iptu matricula arrecadacao calculo bairro pagamento',
            'inadimpl' => 'inadimplencia debito pagamento arrecad arrepaga',
            'bairro' => 'bairro lote ruasbairro ruas localizacao',
            'imove' => 'matricula imovel iptubase lote proprietario',
            'nota' => 'notas fiscais issqn issvarnotas nota avulsa cancelamento',
            'cnae' => 'cnae atividade issbase tabativ atividcnae',
            'empenh' => 'empenho empempenho dotacao liquidacao pagamento',
        ];

        foreach ($domainHints as $needle => $query) {
            if (str_contains($normalized, $needle)) {
                $queries[] = $query;
            }
        }

        $technicalTerms = [];
        foreach (preg_split('/[^\pL\pN_]+/u', $normalized) ?: [] as $term) {
            if (strlen($term) >= 4 && ! is_numeric($term)) {
                $technicalTerms[] = $term;
            }
        }

        if (! empty($technicalTerms)) {
            $queries[] = implode(' ', array_slice(array_unique($technicalTerms), 0, 8));
        }

        return array_values(array_unique(array_filter($queries))) ?: [$question];
    }

    private function isAnswerOnlyQuestion(string $question): bool
    {
        $normalized = strtolower($question);

        $answerOnlyHints = [
            'como funciona',
            'me explique',
            'explique',
            'qual a regra',
            'regra de',
            'o que significa',
            'o que é',
            'o que e',
            'onde fica a regra',
            'qual tabela guarda',
            'qual tabela',
            'quais tabelas',
            'relacionamento',
            'join',
            'sem consultar',
            'sem consulta',
            'não consulte',
            'nao consulte',
            'não precisa consultar',
            'nao precisa consultar',
            'só dúvida',
            'so duvida',
            'apenas dúvida',
            'apenas duvida',
            'para que serve',
            'o que faz',
            'função da',
            'funcao da',
            'estrutura da',
            'sobre a tabela',
        ];

        foreach ($answerOnlyHints as $hint) {
            if (str_contains($normalized, $hint)) {
                return true;
            }
        }

        return false;
    }

    /**
     * @param array<int, string> $queries
     * @return array<int, array<string, mixed>>
     */
    private function collectEvidence(string $question, array $queries): array
    {
        $evidence = [];

        foreach (array_slice($queries, 0, 5) as $query) {
            $evidence[] = [
                'agent' => 'EvidenceSearch',
                'tool' => 'ecidade_catalog_search',
                'query' => $query,
                'result' => $this->compactToolResult(
                    $this->mcpClient->callTool('ecidade_catalog_search', [
                        'text' => $query,
                        'limit' => 8,
                    ])
                ),
            ];

            $evidence[] = [
                'agent' => 'EvidenceSearch',
                'tool' => 'ecidade_catalog_rag_search',
                'query' => $query,
                'result' => $this->compactToolResult(
                    $this->mcpClient->callTool('ecidade_catalog_rag_search', [
                        'text' => $query,
                        'limit' => 8,
                        'kinds' => [
                            'validated_query',
                            'business_concept',
                            'relationship_recipe',
                            'counting_rule',
                            'business_filter',
                            'markdown_rule',
                        ],
                    ])
                ),
            ];
        }

        return $evidence;
    }

    /**
     * @param array<int, array<string, mixed>> $evidence
     * @param array<int, string> $repairQueries
     * @return array<string, mixed>
     */
    private function askPlanner(string $question, array $evidence, array $repairQueries): array
    {
        $payload = [
            'question' => $question,
            'repair_queries_used' => $repairQueries,
            'evidence' => array_slice($evidence, 0, 12),
        ];

        try {
            $response = Prism::text()
                ->using(Provider::Gemini, env('GEMINI_MODEL', 'gemini-2.5-flash'))
                ->withSystemPrompt($this->plannerPrompt())
                ->withMessages([
                    new UserMessage(json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)),
                ])
                ->generate();

            return $this->decodePlannerJson($response->text);
        } catch (\Throwable $e) {
            Log::error('AgentPreflightPlanner: falha no planner.', ['error' => $e->getMessage()]);

            return [
                'routes' => [],
                'selected_route_index' => null,
                'query_spec' => [
                    'missing_requirements' => ['Falha ao executar preflight planner: ' . $e->getMessage()],
                ],
                'critic' => [
                    'approved_for_sql' => false,
                    'reason' => 'O preflight planner falhou antes de validar rota e query_spec.',
                    'required_repairs' => [],
                ],
                'search_repairs' => [],
            ];
        }
    }

    private function plannerPrompt(): string
    {
        return <<<'PROMPT'
Você é um conjunto de subagentes internos do E-CidadeIA: Router, QuerySpec, Critic, SearchRepair e RouteVoter.

Você NÃO escreve SQL. Sua função é decidir se a pergunta pode avançar para geração de SQL.

Responda somente JSON válido, sem Markdown.

Contrato JSON:
{
  "routes": [
    {
      "name": "string",
      "score": 0,
      "tables": ["schema.tabela"],
      "evidence_refs": ["descrição curta da evidência usada"],
      "risks": ["risco ou lacuna"]
    }
  ],
  "selected_route_index": 0,
  "route_vote_reason": "por que a rota vencedora venceu",
  "query_spec": {
    "intent": "ranking|contagem|soma|detalhamento|comparacao|conhecimento|desconhecido",
    "main_entity": "string",
    "grain": "string",
    "measure": "string|null",
    "time_axis": "string|null",
    "required_filters": ["string"],
    "joins": ["string"],
    "expected_answer_shape": "string",
    "missing_requirements": ["string"]
  },
  "critic": {
    "approved_for_sql": false,
    "reason": "string",
    "required_repairs": ["string"]
  },
  "search_repairs": [
    {"query": "string", "reason": "string"}
  ]
}

Regras:
- Gere 2 ou 3 rotas candidatas quando houver evidência suficiente.
- Faça votação simples pela maior coerência entre pergunta, tabelas, grão, filtros e relacionamentos.
- Aprove SQL apenas se houver rota, entidade principal, grão, tabelas, medida/finalidade e joins/filtros suficientes.
- Se a pergunta exigir recorte temporal e ele não estiver explícito nem evidente, bloqueie e liste a lacuna.
- Se houver risco de duplicidade por join, bloqueie ou exija regra de contagem/agregação.
- Se as evidências forem fracas, gere search_repairs com consultas alternativas.
- IMPORTANTE: Se a pergunta for sobre definições de tabela, finalidade, "para que serve" ou metadados, defina a intent como "conhecimento" e bloqueie o SQL (approved_for_sql: false).
PROMPT;
    }

    /**
     * @param array<int, array<string, mixed>> $evidence
     * @return array<string, mixed>
     */
    private function buildAnswerOnlyPlan(string $question, array $evidence): array
    {
        return [
            'routes' => [
                [
                    'name' => 'resposta_somente_conhecimento',
                    'score' => 100,
                    'tables' => $this->extractTablesFromEvidence($evidence),
                    'evidence_refs' => ['Pergunta classificada como dúvida de regra/conceito, sem necessidade de SQL.'],
                    'risks' => [],
                ],
            ],
            'selected_route_index' => 0,
            'route_vote_reason' => 'O usuário pediu explicação/regra/conceito. A melhor rota é responder com conhecimento RAG/catálogo, sem consultar dados.',
            'query_spec' => [
                'intent' => 'explicacao_regra',
                'main_entity' => null,
                'grain' => null,
                'measure' => null,
                'time_axis' => null,
                'required_filters' => [],
                'joins' => [],
                'expected_answer_shape' => 'explicação técnica curta baseada nas evidências',
                'missing_requirements' => [],
            ],
            'critic' => [
                'approved_for_sql' => false,
                'reason' => 'SQL desnecessário: a pergunta é de regra/conceito e deve ser respondida por conhecimento.',
                'required_repairs' => [],
            ],
            'search_repairs' => [],
            'answer_only' => true,
        ];
    }

    /**
     * @param array<string, mixed> $plan
     * @param array<int, array<string, mixed>> $evidence
     */
    private function buildKnowledgeAnswer(string $question, array $plan, array $evidence): string
    {
        $payload = [
            'question' => $question,
            'plan' => $plan,
            'evidence' => array_slice($evidence, 0, 8),
        ];

        try {
            $response = Prism::text()
                ->using(Provider::Gemini, env('GEMINI_MODEL', 'gemini-2.5-flash'))
                ->withSystemPrompt($this->knowledgeAnswerPrompt())
                ->withMessages([
                    new UserMessage(json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)),
                ])
                ->generate();

            return trim($response->text);
        } catch (\Throwable $e) {
            Log::error('AgentPreflightPlanner: falha ao gerar resposta sem SQL.', ['error' => $e->getMessage()]);

            return "Não vou executar SQL para esta pergunta.\n\n"
                . "A pergunta parece ser uma dúvida de regra/conceito, mas não consegui gerar a explicação automática agora.\n"
                . "Evidências consultadas: " . count($evidence) . ' resultado(s) de catálogo/RAG.';
        }
    }

    private function knowledgeAnswerPrompt(): string
    {
        return <<<'PROMPT'
Você é o E-CidadeIA respondendo uma dúvida de regra de negócio ou estrutura, sem consultar dados.

Use somente as evidências de catálogo/RAG fornecidas. Não escreva SQL executável e não diga que consultou o banco.
Se a evidência for insuficiente, diga exatamente o que falta curar no RAG/catálogo.

Responda em português, de forma técnica e objetiva.
PROMPT;
    }

    /**
     * @return array<string, mixed>
     */
    private function decodePlannerJson(string $text): array
    {
        $clean = trim($text);
        $clean = preg_replace('/^```(?:json)?\s*/i', '', $clean) ?? $clean;
        $clean = preg_replace('/\s*```$/', '', $clean) ?? $clean;

        try {
            $decoded = json_decode($clean, true, 512, JSON_THROW_ON_ERROR);
            return is_array($decoded) ? $decoded : [];
        } catch (\JsonException) {
            $start = strpos($clean, '{');
            $end = strrpos($clean, '}');

            if ($start !== false && $end !== false && $end > $start) {
                $candidate = substr($clean, $start, $end - $start + 1);
                try {
                    $decoded = json_decode($candidate, true, 512, JSON_THROW_ON_ERROR);
                    return is_array($decoded) ? $decoded : [];
                } catch (\JsonException) {
                    // cai no retorno bloqueado abaixo
                }
            }
        }

        return [
            'routes' => [],
            'selected_route_index' => null,
            'query_spec' => ['missing_requirements' => ['O planner não retornou JSON válido.']],
            'critic' => [
                'approved_for_sql' => false,
                'reason' => 'O preflight não conseguiu estruturar uma decisão auditável.',
                'required_repairs' => ['Reexecutar busca RAG/catálogo com termos mais específicos.'],
            ],
            'search_repairs' => [],
        ];
    }

    /**
     * @param array<string, mixed> $plan
     */
    private function isApproved(array $plan): bool
    {
        $routes = (array) ($plan['routes'] ?? []);
        $missingRequirements = (array) data_get($plan, 'query_spec.missing_requirements', []);

        return (bool) data_get($plan, 'critic.approved_for_sql', false)
            && ! empty($routes)
            && empty($missingRequirements)
            && data_get($plan, 'selected_route_index') !== null;
    }

    /**
     * @param array<string, mixed> $plan
     * @return array<int, string>
     */
    private function repairQueries(array $plan): array
    {
        $repairs = [];
        foreach ((array) ($plan['search_repairs'] ?? []) as $repair) {
            if (is_array($repair) && ! empty($repair['query'])) {
                $repairs[] = (string) $repair['query'];
            } elseif (is_string($repair) && trim($repair) !== '') {
                $repairs[] = $repair;
            }
        }

        return array_values(array_unique(array_slice($repairs, 0, 3)));
    }

    /**
     * @param array<string, mixed> $plan
     * @param array<int, array<string, mixed>> $evidence
     */
    private function buildContext(string $question, array $plan, array $evidence, bool $approved): string
    {
        return "[PREFLIGHT_AGENTICO]\n"
            . "Pergunta original: {$question}\n"
            . "Status: " . ($approved ? 'APROVADO_PARA_SQL' : 'BLOQUEADO_ANTES_DO_SQL') . "\n"
            . "Plano aprovado/avaliado:\n"
            . json_encode($plan, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
            . "\n\nEvidências compactas usadas:\n"
            . json_encode(array_slice($evidence, 0, 8), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    }

    /**
     * @param array<string, mixed> $plan
     * @param array<int, array<string, mixed>> $evidence
     */
    private function buildBlockedAnswer(array $plan, array $evidence): string
    {
        $reason = data_get($plan, 'critic.reason', 'O agente não encontrou evidência suficiente para executar SQL com segurança analítica.');
        $missing = (array) data_get($plan, 'query_spec.missing_requirements', []);
        $repairs = (array) data_get($plan, 'critic.required_repairs', []);

        $lines = [
            'Não vou executar SQL para esta pergunta ainda.',
            '',
            'Motivo: ' . $reason,
        ];

        if (! empty($missing)) {
            $lines[] = '';
            $lines[] = 'Lacunas encontradas:';
            foreach ($missing as $item) {
                $lines[] = '- ' . (is_scalar($item) ? (string) $item : json_encode($item, JSON_UNESCAPED_UNICODE));
            }
        }

        if (! empty($repairs)) {
            $lines[] = '';
            $lines[] = 'O que precisa ser reparado/curado:';
            foreach ($repairs as $item) {
                $lines[] = '- ' . (is_scalar($item) ? (string) $item : json_encode($item, JSON_UNESCAPED_UNICODE));
            }
        }

        $lines[] = '';
        $lines[] = 'Evidências consultadas: ' . count($evidence) . ' resultado(s) de catálogo/RAG.';

        return implode("\n", $lines);
    }

    private function compactToolResult(string $result): string
    {
        if (strlen($result) <= 5000) {
            return $result;
        }

        return substr($result, 0, 5000) . '... [evidência truncada no preflight]';
    }

    /**
     * @param array<int, array<string, mixed>> $evidence
     * @return array<int, string>
     */
    private function extractTablesFromEvidence(array $evidence): array
    {
        $tables = [];

        foreach ($evidence as $item) {
            $result = (string) ($item['result'] ?? '');
            if (preg_match_all('/\b[a-z_][a-z0-9_]*\.[a-z_][a-z0-9_]*\b/i', $result, $matches)) {
                foreach ($matches[0] as $table) {
                    $tables[] = strtolower($table);
                }
            }
        }

        return array_values(array_unique(array_slice($tables, 0, 12)));
    }

    /**
     * @param array<int, array<string, mixed>> $evidence
     */
    private function hasUsableEvidence(array $evidence): bool
    {
        foreach ($evidence as $item) {
            $result = strtolower((string) ($item['result'] ?? ''));

            if ($result === '') {
                continue;
            }

            if (str_contains($result, '"error":true') || str_contains($result, '"error": true')) {
                continue;
            }

            if (str_contains($result, '"results"') || str_contains($result, 'relationship') || str_contains($result, 'table')) {
                return true;
            }
        }

        return false;
    }
}
