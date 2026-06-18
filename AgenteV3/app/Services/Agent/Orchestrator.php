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
     * Intercepta o loop do ReAct definindo maxSteps(1), permitindo capturar as chamadas de ferramenta
     * e executá-las de forma síncrona pelo PHP, transmitindo o andamento via Laravel Reverb.
     *
     * @param string $question A pergunta fornecida pelo usuário.
     * @param string|null $sessionId ID da sessão para o tracking do Reverb e MCP.
     * @return array Array associativo contendo o session_id, response final e o histórico completo de steps.
     */
    public function ask(string $question, ?string $sessionId = null): array
    {
        $sessionId = $sessionId ?? Str::uuid()->toString();
        Log::info("Orchestrator: Nova execução iniciada (Loop ReAct Manual)...", [
            'question' => $question,
            'session_id' => $sessionId
        ]);

        $messages = [];

        // Carrega o histórico da conversa baseado no limite do .env
        $limit = env('AGENT_MEMORY_LIMIT', 3);
        $history = \App\Models\AgentConversation::where('session_id', $sessionId)
            ->latest('id')
            ->take($limit)
            ->get()
            ->reverse();

        foreach ($history as $interaction) {
            $messages[] = new UserMessage($interaction->question);
            
            $responseContext = $interaction->response;
            if (!empty($interaction->sql_used)) {
                $responseContext .= "\n\n[Contexto - SQL Utilizado Anteriormente:\n" . $interaction->sql_used . "\n]";
            }
            $messages[] = new AssistantMessage($responseContext);
        }

        // Adiciona a pergunta atual
        $messages[] = new UserMessage($question);

        $steps = [];
        $maxSteps = 15;
        $currentStep = 1;
        $finalResponseText = '';
        $executedSqls = []; // Guarda os SQLs dessa rodada

        $tools = [
            new RagSearchTool(),
            new McpExecutionTool()
        ];

        while ($currentStep <= $maxSteps) {
            Log::info("Orchestrator: Executando passo {$currentStep} no loop...", [
                'session_id' => $sessionId
            ]);

            // Chamamos o Gemini com limite de 1 passo de execução para interceptar o fluxo
            $response = Prism::text()
                ->using(Provider::Gemini, env('GEMINI_MODEL', 'gemini-2.5-flash'))
                ->withSystemPrompt($this->getSystemPrompt())
                ->withMessages($messages)
                ->withTools($tools)
                ->withMaxSteps(1)
                ->generate();

            $lastStep = $response->steps->last();
            if (!$lastStep) {
                Log::warning("Orchestrator: Nenhum passo retornado pela LLM.", [
                    'session_id' => $sessionId
                ]);
                break;
            }

            // Preparação dos dados iniciais do passo
            $stepData = [
                'text' => $lastStep->text,
                'finishReason' => $lastStep->finishReason->value,
                'toolCalls' => collect($lastStep->toolCalls)->map(fn ($tc) => $tc->toArray())->toArray(),
                'toolResults' => [],
                'stepCount' => $currentStep
            ];

            // Se terminou com Tool Calls, precisamos executar as ferramentas
            if ($lastStep->finishReason->value === 'tool-calls') {
                $toolResults = [];

                foreach ($lastStep->toolCalls as $toolCall) {
                    $toolInstance = collect($tools)->first(fn ($t) => $t->name() === $toolCall->name);

                    if ($toolInstance) {
                        Log::info("Orchestrator: Executando tool '{$toolCall->name}' manualmente...", [
                            'session_id' => $sessionId,
                            'arguments' => $toolCall->arguments()
                        ]);

                        try {
                            // Captura o SQL se for chamada do banco de dados
                            if ($toolCall->name === 'mcp_execute_sql') {
                                $args = $toolCall->arguments();
                                if (isset($args['sql'])) {
                                    $executedSqls[] = $args['sql'];
                                }
                            }

                            // Executa a lógica da ferramenta com os argumentos correspondentes
                            $output = call_user_func_array([$toolInstance, 'handle'], $toolCall->arguments());
                            
                            // Trata o retorno da ferramenta
                            if (is_string($output)) {
                                $resultText = $output;
                            } else {
                                $resultText = $output->result ?? (string)$output;
                            }
                        } catch (\Throwable $e) {
                            Log::error("Orchestrator: Erro na execução da tool '{$toolCall->name}'", [
                                'error' => $e->getMessage()
                            ]);
                            $resultText = "Erro na execução da ferramenta: " . $e->getMessage();
                        }

                        $toolResults[] = new ToolResult(
                            toolCallId: $toolCall->id,
                            toolName: $toolCall->name,
                            args: $toolCall->arguments(),
                            result: $resultText,
                            toolCallResultId: $toolCall->resultId
                        );
                    } else {
                        Log::warning("Orchestrator: Ferramenta '{$toolCall->name}' não encontrada no escopo.");
                    }
                }

                // Vincula os resultados no payload de transmissão truncando payloads muito grandes para evitar erros de rede/WebSocket
                $truncatedResults = collect($toolResults)->map(function ($tr) {
                    $arr = $tr->toArray();
                    
                    if (is_string($arr['result'])) {
                        try {
                            $decoded = json_decode($arr['result'], true);
                            if (is_array($decoded)) {
                                // Limita strings longas dentro de chaves de objetos (ex: o campo 'content' do RAG)
                                foreach ($decoded as $key => $item) {
                                    if (is_array($item)) {
                                        foreach ($item as $subKey => $subVal) {
                                            if (is_string($subVal) && strlen($subVal) > 300) {
                                                $decoded[$key][$subKey] = substr($subVal, 0, 300) . "... [Corte do dashboard]";
                                            }
                                        }
                                    } elseif (is_string($item) && strlen($item) > 300) {
                                        $decoded[$key] = substr($item, 0, 300) . "... [Corte do dashboard]";
                                    }
                                }
                                
                                // Limita a quantidade total de registros no array a 5
                                $originalCount = count($decoded);
                                if ($originalCount > 5) {
                                    $decoded = array_slice($decoded, 0, 5);
                                    $decoded[] = ['info' => "... [Mais " . ($originalCount - 5) . " registros truncados para exibição]"];
                                }
                                
                                $arr['result'] = json_encode($decoded, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES);
                            } else {
                                if (strlen($arr['result']) > 1000) {
                                    $arr['result'] = substr($arr['result'], 0, 1000) . "... [Resultado truncado no Dashboard]";
                                }
                            }
                        } catch (\Throwable $e) {
                            if (strlen($arr['result']) > 1000) {
                                $arr['result'] = substr($arr['result'], 0, 1000) . "... [Resultado truncado no Dashboard]";
                            }
                        }
                    } elseif (is_array($arr['result'])) {
                        $originalCount = count($arr['result']);
                        if ($originalCount > 5) {
                            $arr['result'] = array_slice($arr['result'], 0, 5);
                            $arr['result'][] = [
                                'info' => "... [Mais " . ($originalCount - 5) . " registros truncados para exibição]"
                            ];
                        }
                    }
                    
                    return $arr;
                })->toArray();

                $stepData['toolResults'] = $truncatedResults;
                
                // Salva o passo no histórico de steps (antes do truncamento agressivo pro websocket)
                $steps[] = $stepData;

                // Truncamento agressivo específico para evitar 'Payload too large' no Reverb (10KB limit)
                $broadcastData = $stepData;
                if (strlen($broadcastData['text'] ?? '') > 2000) {
                    $broadcastData['text'] = substr($broadcastData['text'], 0, 2000) . "... [Raciocínio truncado devido ao tamanho]";
                }
                
                // Se ainda for grande, limpa totalmente os arrays mantendo a estrutura esperada pelo frontend
                // Se ainda for grande, limpa apenas os campos pesados, MAS MANTÉM OS NOMES para a UI reconhecer o SQL
                if (strlen(json_encode($broadcastData)) > 5000) {
                    if (isset($broadcastData['toolCalls'])) {
                        foreach ($broadcastData['toolCalls'] as &$tc) {
                            // Se não for SQL, oculta argumentos para poupar espaço
                            if (isset($tc['name']) && $tc['name'] !== 'mcp_execute_sql') {
                                $tc['arguments'] = ['aviso' => '[Argumentos longos ocultos]'];
                            }
                        }
                    }
                    if (isset($broadcastData['toolResults'])) {
                        foreach ($broadcastData['toolResults'] as &$tr) {
                            // Preserva o começo do resultado pra debug, mas corta se for grande
                            if (isset($tr['result']) && is_string($tr['result'])) {
                                if (strlen($tr['result']) > 300) {
                                    $tr['result'] = substr($tr['result'], 0, 300) . "\n\n... [Resultado massivo truncado pelo backend (Limite de WebSocket)]";
                                }
                            } else {
                                $tr['result'] = '[Resultado truncado no backend]';
                            }
                        }
                    }
                }

                Log::info("Orchestrator: Transmitindo passo ReAct intermediário via Reverb", [
                    'session_id' => $sessionId,
                    'step' => $currentStep
                ]);
                event(new AgentStepStreamed($sessionId, $broadcastData));

                // Atualiza o histórico de mensagens para a próxima iteração
                $messages[] = new AssistantMessage($lastStep->text, $lastStep->toolCalls);
                $messages[] = new ToolResultMessage($toolResults);

            } else {
                // Se o finishReason é stop ou length, é a resposta final do loop
                $finalResponseText = $lastStep->text;
                
                // Salvar no banco a nova interação
                \App\Models\AgentConversation::create([
                    'session_id' => $sessionId,
                    'question' => $question,
                    'response' => $finalResponseText,
                    'sql_used' => empty($executedSqls) ? null : implode(";\n\n", $executedSqls)
                ]);

                $steps[] = $stepData;

                Log::info("Orchestrator: Transmitindo passo ReAct final via Reverb", [
                    'session_id' => $sessionId,
                    'step' => $currentStep
                ]);
                event(new AgentStepStreamed($sessionId, $stepData));

                $messages[] = new AssistantMessage($lastStep->text);
                break;
            }

            $currentStep++;
        }

        Log::info("Orchestrator: Loop concluído com sucesso.", [
            'total_steps' => count($steps),
            'session_id' => $sessionId
        ]);

        return [
            'session_id' => $sessionId,
            'response' => $finalResponseText ?: "Não foi possível obter resposta final do modelo após atingir o limite máximo de passos.",
            'steps' => $steps
        ];
    }

    /**
     * Retorna o System Prompt injetado no LLM (Gemini) durante o Loop ReAct.
     * Define as diretrizes operacionais do E-CidadeIA, como forçar a leitura do RAG
     * antes de gerar SQL e instruções para evitar consultas cruzadas custosas.
     *
     * @return string O texto do prompt principal da IA.
     */
    private function getSystemPrompt(): string
    {
        return <<<PROMPT
Você é o E-CidadeIA, um agente de IA especializado no sistema e-Cidade, focado em analisar e responder perguntas de negócio complexas consultando dados reais.

Você opera sob um loop ReAct (Reasoning and Acting). 

Suas diretrizes de operação são:
1. Sempre verifique as regras de negócio e os esquemas das tabelas associadas à pergunta usando a ferramenta `rag_search` antes de escrever qualquer query SQL.
2. IMPORTANTE PARA RAG: A ferramenta `rag_search` faz buscas por palavras chave (ex: lote, bairro, arrecad, etc). Se a busca por termos combinados falhar, tente usar termos individuais ou mais genéricos para encontrar seus esquemas e ligações.
3. Identifique os esquemas, chaves primárias, chaves estrangeiras e regras específicas de negócio ou regras de município no RAG.
4. Nunca faça suposições sobre a estrutura das tabelas ou sobre a lógica de junção. Consulte e siga estritamente as regras de negócio e relacionamentos documentados no RAG.
5. Para realizar a consulta real no banco de dados, use a ferramenta `mcp_execute_sql`. O SQL deve ser estritamente de leitura (SELECT).
6. Se a resposta requerer cálculos matemáticos ou agregação, faça a agregação diretamente no SQL sempre que possível, seguindo as diretrizes estruturais obtidas no RAG.
7. Responda ao usuário final em Português de forma técnica, clara, direta e objetiva, detalhando os dados encontrados e, se aplicável, as regras de negócio utilizadas.
PROMPT;
    }
}
