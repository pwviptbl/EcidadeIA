<?php

namespace App\Services\Agent;

use App\Events\AgentStepStreamed;
use App\Services\Mcp\McpClient;
use App\Tools\McpCatalogRagSearchTool;
use App\Tools\McpDescribeTableTool;
use App\Tools\McpExecutionTool;
use App\Tools\McpListSchemasTool;
use App\Tools\McpRelationshipsTool;
use App\Tools\RagSearchTool;
use Prism\Prism\Facades\Prism;
use Prism\Prism\Enums\Provider;
use Prism\Prism\ValueObjects\Messages\UserMessage;
use Prism\Prism\ValueObjects\Messages\AssistantMessage;
use Prism\Prism\ValueObjects\Messages\ToolResultMessage;
use Prism\Prism\ValueObjects\ToolResult;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;

class Orchestrator
{
    public function __construct(
        private readonly McpClient $mcpClient,
        private readonly AgentPreflightPlanner $preflightPlanner
    ) {
    }

    /**
     * Executa a pergunta do usuário no loop agentivo do Prism com suporte a streaming de passos via WebSockets.
     *
     * O loop é implementado manualmente com maxSteps(1) porque o Prism v0.100.1 não expõe hooks
     * de passo (callbacks por iteração). Usar withMaxSteps(N>1) nativo executaria as ferramentas
     * internamente sem permitir interceptação para transmissão via Reverb.
     *
     * @param string $question A pergunta fornecida pelo usuário.
     * @param string|null $sessionId ID da sessão para o tracking do Reverb e MCP.
     * @return array Array associativo contendo o session_id, response final e o histórico completo de steps.
     */
    public function ask(string $question, ?string $sessionId = null): array
    {
        $sessionId = $sessionId ?? Str::uuid()->toString();
        Log::info('Orchestrator: Nova execução iniciada.', [
            'question'   => $question,
            'session_id' => $sessionId,
        ]);

        $messages     = $this->buildMessageHistory($sessionId, $question);
        $tools        = $this->buildTools();
        $steps        = [];
        $executedSqls = [];
        $maxSteps     = 15;
        $currentStep  = 1;
        $finalText    = '';
        $circuitBreaker = new CircuitBreaker((int) env('AGENT_CIRCUIT_BREAKER_LIMIT', 3));

        $preflight = $this->preflightPlanner->plan($question);
        $preflightStep = $this->buildPreflightStep($preflight, $currentStep);
        $steps[] = $preflightStep;
        event(new AgentStepStreamed($sessionId, $this->buildBroadcastStep($preflightStep)));
        $currentStep++;

        if (! $preflight['approved']) {
            $finalText = (string) $preflight['answer_if_blocked'];

            \App\Models\AgentConversation::create([
                'session_id' => $sessionId,
                'question'   => $question,
                'response'   => $finalText,
                'sql_used'   => null,
            ]);

            return [
                'session_id' => $sessionId,
                'response'   => $finalText,
                'sql_used'   => null,
                'steps'      => $steps,
            ];
        }

        $messages[] = new AssistantMessage((string) $preflight['context']);
        $messages[] = new UserMessage(
            "Continue a pergunta original usando o PREFLIGHT_AGENTICO aprovado. "
            . "Gere SQL somente se respeitar o query_spec, as evidências e a crítica pré-SQL. "
            . "Depois da execução, responda apenas com base nas linhas retornadas."
        );

        while ($currentStep <= $maxSteps) {
            Log::info("Orchestrator: Passo {$currentStep}.", ['session_id' => $sessionId]);

            $response = Prism::text()
                ->using(Provider::Gemini, env('GEMINI_MODEL', 'gemini-2.5-flash'))
                ->withSystemPrompt($this->getSystemPrompt())
                ->withMessages($messages)
                ->withTools($tools)
                ->withMaxSteps(1)
                ->generate();

            $lastStep = $response->steps->last();
            if (! $lastStep) {
                Log::warning('Orchestrator: Nenhum passo retornado.', ['session_id' => $sessionId]);
                break;
            }

            $stepData = [
                'text'         => $lastStep->text,
                'finishReason' => $lastStep->finishReason->value,
                'toolCalls'    => collect($lastStep->toolCalls)->map(fn ($tc) => $tc->toArray())->toArray(),
                'toolResults'  => [],
                'stepCount'    => $currentStep,
            ];

            if ($lastStep->finishReason->value === 'tool-calls') {
                [$toolResults, $stepData] = $this->executeToolCalls(
                    $lastStep, $tools, $stepData, $executedSqls, $sessionId, $circuitBreaker
                );

                $steps[] = $stepData;
                event(new AgentStepStreamed($sessionId, $this->buildBroadcastStep($stepData)));

                $messages[] = new AssistantMessage($lastStep->text, $lastStep->toolCalls);
                $messages[] = new ToolResultMessage($toolResults);
            } else {
                $finalText = $lastStep->text;

                \App\Models\AgentConversation::create([
                    'session_id' => $sessionId,
                    'question'   => $question,
                    'response'   => $finalText,
                    'sql_used'   => empty($executedSqls) ? null : implode(";\n\n", $executedSqls),
                ]);

                $steps[] = $stepData;
                event(new AgentStepStreamed($sessionId, $stepData));
                $messages[] = new AssistantMessage($lastStep->text);
                break;
            }

            $currentStep++;
        }

        Log::info('Orchestrator: Loop concluído.', [
            'total_steps' => count($steps),
            'session_id'  => $sessionId,
        ]);

        return [
            'session_id' => $sessionId,
            'response'   => $finalText ?: 'Não foi possível obter resposta final do modelo após atingir o limite máximo de passos.',
            'sql_used'   => empty($executedSqls) ? null : implode(";\n\n", $executedSqls),
            'steps'      => $steps,
        ];
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Métodos privados auxiliares
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Monta as ferramentas disponíveis para o loop ReAct.
     *
     * Mantém `rag_search` por compatibilidade com o prompt atual, mas expõe
     * também as ferramentas MCP estruturadas para catálogo, metadados e joins.
     *
     * @return array<int, object>
     */
    private function buildTools(): array
    {
        return [
            new RagSearchTool($this->mcpClient),
            new McpCatalogRagSearchTool($this->mcpClient),
            new McpListSchemasTool($this->mcpClient),
            new McpDescribeTableTool($this->mcpClient),
            new McpRelationshipsTool($this->mcpClient),
            new McpExecutionTool($this->mcpClient),
        ];
    }

    /**
     * @param array<string, mixed> $preflight
     * @return array<string, mixed>
     */
    private function buildPreflightStep(array $preflight, int $stepCount): array
    {
        $plan = $preflight['plan'] ?? [];
        $approved = (bool) ($preflight['approved'] ?? false);
        $answerOnly = (bool) ($plan['answer_only'] ?? false);

        $summary = match (true) {
            $approved => 'Preflight agentico aprovado.',
            $answerOnly => 'Preflight identificou dúvida de conhecimento e desativou SQL.',
            default => 'Preflight agentico bloqueou a execução SQL.',
        };

        return [
            'text' => $summary . "\n\n"
                . json_encode($plan, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
            'finishReason' => $approved ? 'preflight-approved' : ($answerOnly ? 'preflight-answer-only' : 'preflight-blocked'),
            'toolCalls' => [
                [
                    'name' => 'preflight_router_queryspec_critic',
                    'arguments' => ['question' => $preflight['question'] ?? null],
                ],
            ],
            'toolResults' => [
                [
                    'tool_name' => 'preflight_router_queryspec_critic',
                    'result' => json_encode([
                        'approved' => $approved,
                        'evidence_count' => count((array) ($preflight['evidence'] ?? [])),
                        'answer_if_blocked' => $preflight['answer_if_blocked'] ?? null,
                    ], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
                ],
            ],
            'stepCount' => $stepCount,
        ];
    }

    /**
     * Monta o histórico de mensagens da sessão + a pergunta atual.
     *
     * @return array<int, UserMessage|AssistantMessage>
     */
    private function buildMessageHistory(string $sessionId, string $question): array
    {
        $limit   = (int) env('AGENT_MEMORY_LIMIT', 3);
        $history = \App\Models\AgentConversation::where('session_id', $sessionId)
            ->latest('id')
            ->take($limit)
            ->get()
            ->reverse();

        $messages = [];
        foreach ($history as $interaction) {
            $messages[] = new UserMessage($interaction->question);
            $ctx = $interaction->response;
            if (! empty($interaction->sql_used)) {
                $ctx .= "\n\n[Contexto - SQL Utilizado Anteriormente:\n{$interaction->sql_used}\n]";
            }
            $messages[] = new AssistantMessage($ctx);
        }

        $messages[] = new UserMessage($question);
        return $messages;
    }

    /**
     * Executa as tool calls do passo atual e captura SQLs válidos.
     *
     * @param  array<int, object>  $tools
     * @param  array<string, mixed>  $stepData
     * @param  array<int, string>  $executedSqls
     * @return array{0: ToolResult[], 1: array<string,mixed>}
     */
    private function executeToolCalls(
        object $lastStep,
        array $tools,
        array $stepData,
        array &$executedSqls,
        string $sessionId,
        CircuitBreaker $circuitBreaker
    ): array {
        $toolResults = [];

        foreach ($lastStep->toolCalls as $toolCall) {
            $toolInstance = collect($tools)->first(fn ($t) => $t->name() === $toolCall->name);

            if (! $toolInstance) {
                Log::warning("Orchestrator: Ferramenta '{$toolCall->name}' não encontrada.", ['session_id' => $sessionId]);
                continue;
            }

            Log::info("Orchestrator: Executando tool '{$toolCall->name}'.", [
                'session_id' => $sessionId,
                'arguments'  => $toolCall->arguments(),
            ]);

            try {
                $output = call_user_func_array([$toolInstance, 'handle'], $toolCall->arguments());
                $resultText = is_string($output) ? $output : ($output->result ?? (string) $output);

                if ($toolCall->name === 'mcp_execute_sql') {
                    $this->captureSqlFromResult($toolCall, $resultText, $executedSqls);
                }
            } catch (\Throwable $e) {
                Log::error("Orchestrator: Erro na tool '{$toolCall->name}'.", ['error' => $e->getMessage()]);
                $resultText = 'Erro na execução da ferramenta: ' . $e->getMessage();
            }

            $resultText = $this->applyCircuitBreaker(
                $circuitBreaker,
                $toolCall->name,
                $toolCall->arguments(),
                $resultText,
                $sessionId
            );

            $toolResults[] = new ToolResult(
                toolCallId:       $toolCall->id,
                toolName:         $toolCall->name,
                args:             $toolCall->arguments(),
                result:           $resultText,
                toolCallResultId: $toolCall->resultId
            );
        }

        $stepData['toolResults'] = $this->truncateToolResultsForDashboard($toolResults);

        return [$toolResults, $stepData];
    }

    /**
     * Registra o resultado de uma tool no circuit breaker e devolve orientação
     * explícita para o modelo quando ele estiver repetindo a mesma falha.
     *
     * @param array<string, mixed> $arguments
     */
    private function applyCircuitBreaker(
        CircuitBreaker $circuitBreaker,
        string $toolName,
        array $arguments,
        string $resultText,
        string $sessionId
    ): string {
        if (! $this->isToolError($resultText)) {
            $circuitBreaker->recordSuccess();
            return $resultText;
        }

        $circuitBreaker->recordError($toolName, $resultText, $arguments);

        if (! $circuitBreaker->shouldBreak()) {
            return $resultText;
        }

        $summary = $circuitBreaker->getErrorSummary();
        $strategy = $circuitBreaker->getSuggestedStrategy();

        Log::warning('Orchestrator: Circuit breaker acionado.', [
            'session_id' => $sessionId,
            'tool' => $toolName,
            'summary' => $summary,
            'strategy' => $strategy,
        ]);

        return $resultText
            . "\n\n[ORIENTACAO_DO_ORQUESTRADOR]\n"
            . "A mesma falha se repetiu em chamadas recentes. Pare de repetir a mesma ferramenta com os mesmos pressupostos.\n"
            . "Estratégia sugerida: {$strategy}\n"
            . "Antes de tentar nova execução SQL, refaça a rota, consulte evidências alternativas e revise o query_spec.";
    }

    /**
     * Detecta falhas retornadas por tools em texto ou JSON.
     */
    private function isToolError(string $resultText): bool
    {
        $lower = strtolower($resultText);

        return str_contains($lower, '"error":true')
            || str_contains($lower, '"error": true')
            || str_contains($lower, 'erro na execução')
            || str_contains($lower, 'falha de comunicação')
            || str_contains($lower, 'error executing tool')
            || str_contains($lower, 'exception')
            || str_contains($lower, 'sqlstate')
            || str_contains($lower, 'undefined column')
            || str_contains($lower, 'column does not exist')
            || str_contains($lower, 'tabela fora do catalogo')
            || str_contains($lower, 'fora do catalogo')
            || str_contains($lower, 'allowlist')
            || str_contains($lower, 'syntax error');
    }

    /**
     * Captura o SQL da tool call apenas se a execução foi bem-sucedida.
     *
     * @param  array<int, string>  $executedSqls
     */
    private function captureSqlFromResult(object $toolCall, string $resultText, array &$executedSqls): void
    {
        $args = $toolCall->arguments();
        if (! isset($args['sql'])) {
            return;
        }
        $isError = str_contains($resultText, 'Error executing tool')
            || str_contains($resultText, 'Erro na execução')
            || str_contains($resultText, '"error":true');

        if (! $isError) {
            $executedSqls[] = $args['sql'];
        }
    }

    /**
     * Trunca os resultados das ferramentas para exibição no Dashboard.
     * Evita payloads >5KB no WebSocket sem perder dados nos $steps internos.
     *
     * @param  ToolResult[]  $toolResults
     * @return array<int, array<string, mixed>>
     */
    private function truncateToolResultsForDashboard(array $toolResults): array
    {
        return collect($toolResults)->map(function ($tr) {
            $arr = $tr->toArray();

            if (! is_string($arr['result'])) {
                if (is_array($arr['result']) && count($arr['result']) > 5) {
                    $extra = count($arr['result']) - 5;
                    $arr['result'] = array_slice($arr['result'], 0, 5);
                    $arr['result'][] = ['info' => "... [Mais {$extra} registros truncados para exibição]"];
                }
                return $arr;
            }

            try {
                $decoded = json_decode($arr['result'], true, 512, JSON_THROW_ON_ERROR);

                if (is_array($decoded)) {
                    foreach ($decoded as $key => $item) {
                        if (is_array($item)) {
                            foreach ($item as $subKey => $subVal) {
                                if (is_string($subVal) && strlen($subVal) > 300) {
                                    $decoded[$key][$subKey] = substr($subVal, 0, 300) . '... [Corte do dashboard]';
                                }
                            }
                        } elseif (is_string($item) && strlen($item) > 300) {
                            $decoded[$key] = substr($item, 0, 300) . '... [Corte do dashboard]';
                        }
                    }
                    if (count($decoded) > 5) {
                        $extra = count($decoded) - 5;
                        $decoded = array_slice($decoded, 0, 5);
                        $decoded[] = ['info' => "... [Mais {$extra} registros truncados para exibição]"];
                    }
                    $arr['result'] = json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
                } else {
                    $arr['result'] = $this->truncateString($arr['result'], 1000);
                }
            } catch (\Throwable) {
                $arr['result'] = $this->truncateString($arr['result'], 1000);
            }

            return $arr;
        })->toArray();
    }

    /**
     * Prepara o stepData para broadcast via Reverb com truncamento agressivo de rede.
     * Não afeta o array $steps que é retornado ao cliente HTTP.
     *
     * @param  array<string, mixed>  $stepData
     * @return array<string, mixed>
     */
    private function buildBroadcastStep(array $stepData): array
    {
        $broadcast = $stepData;

        if (strlen($broadcast['text'] ?? '') > 2000) {
            $broadcast['text'] = substr($broadcast['text'], 0, 2000) . '... [Raciocínio truncado devido ao tamanho]';
        }

        if (strlen(json_encode($broadcast)) > 5000) {
            foreach ($broadcast['toolCalls'] ?? [] as &$tc) {
                if (isset($tc['name']) && $tc['name'] !== 'mcp_execute_sql') {
                    $tc['arguments'] = ['aviso' => '[Argumentos longos ocultos]'];
                }
            }
            unset($tc);

            foreach ($broadcast['toolResults'] ?? [] as &$tr) {
                if (isset($tr['result']) && is_string($tr['result'])) {
                    $tr['result'] = $this->truncateString($tr['result'], 300)
                        . "\n\n... [Resultado massivo truncado pelo backend (Limite de WebSocket)]";
                } else {
                    $tr['result'] = '[Resultado truncado no backend]';
                }
            }
            unset($tr);
        }

        return $broadcast;
    }

    /**
     * Trunca uma string para um tamanho máximo, adicionando reticências.
     */
    private function truncateString(string $value, int $max): string
    {
        return strlen($value) > $max ? substr($value, 0, $max) . '...' : $value;
    }

    /**
     * Retorna o System Prompt injetado no LLM (Gemini) durante o Loop ReAct.
     * Define as diretrizes operacionais do E-CidadeIA e as convenções invariantes
     * do banco do e-Cidade. Os schemas disponíveis são descobertos dinamicamente via RAG.
     *
     * @return string O texto do prompt principal da IA.
     */
    private function getSystemPrompt(): string
    {
        return <<<PROMPT
Você é o E-CidadeIA, um agente de IA especializado no sistema e-Cidade, focado em analisar e responder perguntas de negócio complexas consultando dados reais do banco de dados municipal.

Você opera sob um loop ReAct (Reasoning and Acting). Raciocine antes de agir e valide sua lógica antes de montar qualquer SQL.

---

## CONVENÇÕES CRÍTICAS DO BANCO (invariantes do e-Cidade)

1. **Schemas dinâmicos:** Os módulos e schemas disponíveis variam por instalação e são expandidos continuamente. Sempre use `rag_search` ou `ecidade_list_schemas` para descobrir os schemas ativos — nunca assuma quais schemas existem.

2. **Campo de Ano/Exercício:** O ano fiscal é sempre armazenado em um campo dedicado (não calculado a partir de datas). Use o campo indicado pelo RAG. Nunca use `YEAR(data)`.

3. **Chave Universal de Pessoas (CGM):** Existe uma tabela central de cadastro de pessoas com uma chave numérica que funciona como ID universal para pessoas físicas e jurídicas em todos os módulos. Consulte o RAG para obter o nome exato da tabela e da coluna de chave estrangeira no módulo em questão.

4. **Formato do CNAE:** No banco, o CNAE é armazenado com o prefixo da seção econômica e SEM separadores (ex: `L6810202`, e não `6810-2/02`). Use `LIKE '%6810202'` para buscas resilientes.

5. **Status Ativo/Inativo:** Registros cancelados ou encerrados geralmente têm um campo de data de baixa não nulo. Verifique no RAG qual campo indica o status ativo para cada entidade.

6. **Prefixo de Colunas:** As colunas seguem o padrão `[sigla_tabela]_[nome]`. O RAG e o `ecidade_describe_table` fornecem os nomes exatos.

---

## SUAS DIRETRIZES DE OPERAÇÃO

1. **Sempre consulte o catálogo/RAG primeiro:** Use `rag_search` ou `ecidade_catalog_rag_search` com termos de negócio da pergunta antes de escrever qualquer SQL. Se a busca retornar vazio, tente termos mais simples, sinônimos técnicos e nomes de tabelas prováveis.

2. **Nunca suponha estrutura:** Não invente nomes de colunas ou schemas. Use `ecidade_list_schemas` para descobrir módulos disponíveis, `ecidade_describe_table` para confirmar colunas reais e `ecidade_get_relationships` para confirmar joins.

3. **PROIBIDO consultar `information_schema` diretamente via SQL:** O SQL Guard bloqueará qualquer query que referencie `information_schema`. Para inspecionar colunas de uma tabela, use a ferramenta `ecidade_describe_table` do MCP.

4. **Ao receber erro de permissão/allowlist:**
   - Não tente o mesmo SQL novamente.
   - Use `rag_search` para encontrar uma tabela alternativa dentro dos schemas disponíveis.
   - Se não houver alternativa, informe o usuário claramente: "O domínio solicitado não está disponível no momento. Solicite ao administrador a liberação do schema necessário."

5. **Agregações no SQL:** Se a resposta requerer totais, médias ou rankings, sempre agregue diretamente no SQL com `SUM`, `COUNT`, `GROUP BY` etc. Não traga dados brutos para calcular no texto.

6. **Responda em Português:** De forma técnica, clara e objetiva. Apresente os dados em tabela quando houver múltiplos registros. Informe a fonte dos dados (tabelas e critérios utilizados) nas notas técnicas.

7. **SQL exibido na resposta = SQL que gerou os dados:** Nunca exiba ou mencione uma query que falhou ou foi usada apenas para inspeção de estrutura.

---

## FLUXO AGENTICO OBRIGATÓRIO

Antes de chamar `mcp_execute_sql`, produza no texto do passo um plano curto com:

- `rota`: conceito de negócio, domínio/schema provável e tabelas candidatas;
- `evidências`: documentos, regras ou metadados usados;
- `query_spec`: entidade principal, grão, medida, filtros obrigatórios, eixo temporal e joins;
- `crítica pré-SQL`: por que as tabelas/joins/filtros são suficientes e quais lacunas permanecem.

Se faltar ano, entidade, relacionamento ou regra de contagem para responder corretamente, não invente. Faça nova busca com termos alternativos ou explique a lacuna ao usuário antes de executar SQL.

Para montar SQL, siga esta ordem:

1. Use consulta validada do RAG/catálogo quando existir.
2. Use relacionamentos confirmados por `ecidade_get_relationships`.
3. Use colunas confirmadas por `ecidade_describe_table`.
4. Só gere SQL livre quando o `query_spec` estiver coerente com as evidências disponíveis.
PROMPT;
    }
}
