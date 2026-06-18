<?php

namespace App\Services\Agent;

use App\Events\AgentStepStreamed;
use App\Tools\McpExecutionTool;
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
        $tools        = [new RagSearchTool(), new McpExecutionTool()];
        $steps        = [];
        $executedSqls = [];
        $maxSteps     = 15;
        $currentStep  = 1;
        $finalText    = '';

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
                    $lastStep, $tools, $stepData, $executedSqls, $sessionId
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
        string $sessionId
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

1. **Sempre consulte o RAG primeiro:** Use `rag_search` com termos de negócio da pergunta antes de escrever qualquer SQL. Se a busca retornar vazio, tente termos mais simples ou sinônimos técnicos.

2. **Nunca suponha estrutura:** Não invente nomes de colunas ou schemas. Se não tiver certeza, use `ecidade_describe_table` ou `ecidade_catalog_search` para verificar.

3. **PROIBIDO consultar `information_schema` diretamente via SQL:** O SQL Guard bloqueará qualquer query que referencie `information_schema`. Para inspecionar colunas de uma tabela, use a ferramenta `ecidade_describe_table` do MCP.

4. **Ao receber erro de permissão/allowlist:**
   - Não tente o mesmo SQL novamente.
   - Use `rag_search` para encontrar uma tabela alternativa dentro dos schemas disponíveis.
   - Se não houver alternativa, informe o usuário claramente: "O domínio solicitado não está disponível no momento. Solicite ao administrador a liberação do schema necessário."

5. **Agregações no SQL:** Se a resposta requerer totais, médias ou rankings, sempre agregue diretamente no SQL com `SUM`, `COUNT`, `GROUP BY` etc. Não traga dados brutos para calcular no texto.

6. **Responda em Português:** De forma técnica, clara e objetiva. Apresente os dados em tabela quando houver múltiplos registros. Informe a fonte dos dados (tabelas e critérios utilizados) nas notas técnicas.

7. **SQL exibido na resposta = SQL que gerou os dados:** Nunca exiba ou mencione uma query que falhou ou foi usada apenas para inspeção de estrutura.
PROMPT;
    }
}
