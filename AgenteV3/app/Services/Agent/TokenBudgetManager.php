<?php

namespace App\Services\Agent;

use Prism\Prism\ValueObjects\Messages\AssistantMessage;
use Prism\Prism\ValueObjects\Messages\UserMessage;
use Prism\Prism\ValueObjects\Messages\ToolResultMessage;

/**
 * Gerenciador de orçamento de tokens para o loop agentivo do E-CidadeIA.
 *
 * Estima o consumo de tokens das mensagens do contexto e aplica compressão
 * inteligente quando o orçamento disponível está baixo, priorizando manter
 * as mensagens mais recentes e relevantes enquanto sumariza passos intermediários.
 *
 * Utiliza a heurística de ~4 caracteres por token, ajustada para texto PT-BR
 * que tende a ter palavras mais longas que inglês.
 */
class TokenBudgetManager
{
    /**
     * Limite máximo de tokens da janela de contexto.
     */
    private int $maxTokens;

    /**
     * Tokens reservados para a resposta do modelo.
     */
    private int $reservedForResponse;

    /**
     * Tokens reservados para o system prompt.
     */
    private int $reservedForSystemPrompt;

    /**
     * Cria uma nova instância do gerenciador de orçamento de tokens.
     *
     * @param int $maxTokens              Limite total de tokens do modelo.
     * @param int $reservedForResponse     Tokens reservados para a geração da resposta.
     * @param int $reservedForSystemPrompt Tokens reservados para o system prompt.
     */
    public function __construct(
        int $maxTokens = 32000,
        int $reservedForResponse = 4000,
        int $reservedForSystemPrompt = 3000,
    ) {
        $this->maxTokens              = $maxTokens;
        $this->reservedForResponse    = $reservedForResponse;
        $this->reservedForSystemPrompt = $reservedForSystemPrompt;
    }

    /**
     * Estima o total de tokens consumidos pelo array de mensagens.
     *
     * Utiliza heurística de ~4 caracteres por token para PT-BR.
     * Serializa cada mensagem de forma segura para contagem.
     *
     * @param array<int, AssistantMessage|UserMessage|ToolResultMessage> $messages
     * @return int Estimativa de tokens consumidos.
     */
    public function estimateTokens(array $messages): int
    {
        $totalChars = 0;

        foreach ($messages as $message) {
            $totalChars += mb_strlen($this->extractTextFromMessage($message), 'UTF-8');
        }

        return (int) ceil($totalChars / 4);
    }

    /**
     * Calcula o orçamento de tokens disponível para novas mensagens.
     *
     * @param array<int, AssistantMessage|UserMessage|ToolResultMessage> $messages
     * @return int Tokens disponíveis (pode ser negativo se já estourou).
     */
    public function availableBudget(array $messages): int
    {
        $used = $this->estimateTokens($messages);

        return $this->maxTokens - $used - $this->reservedForResponse - $this->reservedForSystemPrompt;
    }

    /**
     * Verifica se a compressão de mensagens é necessária.
     *
     * Retorna true quando o orçamento disponível é inferior a 4000 tokens,
     * sinalizando que há risco de overflow na próxima iteração.
     *
     * @param array<int, AssistantMessage|UserMessage|ToolResultMessage> $messages
     * @return bool True se a compressão deve ser aplicada.
     */
    public function shouldCompress(array $messages): bool
    {
        return $this->availableBudget($messages) < 4000;
    }

    /**
     * Comprime o array de mensagens mantendo contexto essencial.
     *
     * Estratégia de compressão:
     * - Mantém a primeira mensagem (pergunta original do usuário).
     * - Mantém as 2 últimas mensagens (contexto recente mais relevante).
     * - Sumariza as mensagens intermediárias em um único AssistantMessage.
     *
     * @param array<int, AssistantMessage|UserMessage|ToolResultMessage> $messages
     * @return array<int, AssistantMessage|UserMessage|ToolResultMessage> Mensagens comprimidas.
     */
    public function compress(array $messages): array
    {
        $count = count($messages);

        // Se houver 3 ou menos mensagens, não há o que comprimir
        if ($count <= 3) {
            return $messages;
        }

        $first  = $messages[0];
        $last2  = array_slice($messages, -2);
        $middle = array_slice($messages, 1, $count - 3);

        $summaries = [];

        foreach ($middle as $message) {
            $summaries[] = $this->summarizeMessage($message);
        }

        $summaryText = "[Resumo dos passos anteriores]\n" . implode("\n", $summaries);

        return array_merge(
            [$first],
            [new AssistantMessage($summaryText)],
            $last2,
        );
    }

    /**
     * Trunca o resultado de uma ferramenta para caber no orçamento de tokens.
     *
     * Lógica de truncamento:
     * - JSON com array 'rows' > 20 itens: mantém os primeiros 20 e adiciona nota.
     * - Texto plano > maxChars: corta e adiciona indicador de truncamento.
     *
     * @param string $result   Resultado original da ferramenta.
     * @param int    $maxChars Tamanho máximo em caracteres.
     * @return string Resultado truncado.
     */
    public function truncateToolResult(string $result, int $maxChars = 8000): string
    {
        // Tenta interpretar como JSON com array 'rows'
        try {
            $decoded = json_decode($result, true, 512, JSON_THROW_ON_ERROR);

            if (is_array($decoded) && isset($decoded['rows']) && is_array($decoded['rows'])) {
                $totalRows = count($decoded['rows']);

                if ($totalRows > 20) {
                    $decoded['rows'] = array_slice($decoded['rows'], 0, 20);
                    $decoded['_truncated'] = true;
                    $decoded['_nota']      = "Exibindo 20 de {$totalRows} registros. Resultado truncado para economia de tokens.";

                    return json_encode($decoded, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
                }
            }
        } catch (\JsonException) {
            // Não é JSON válido, trata como texto plano abaixo
        }

        // Truncamento de texto plano
        if (mb_strlen($result, 'UTF-8') > $maxChars) {
            return mb_substr($result, 0, $maxChars, 'UTF-8') . '... [truncado]';
        }

        return $result;
    }

    /**
     * Extrai o conteúdo textual de uma mensagem para estimativa de tokens.
     *
     * Lida com os diferentes tipos de mensagem do Prism de forma segura,
     * usando json_encode como fallback para estruturas desconhecidas.
     *
     * @param AssistantMessage|UserMessage|ToolResultMessage|object $message
     * @return string Texto extraído da mensagem.
     */
    private function extractTextFromMessage(object $message): string
    {
        // UserMessage: propriedade $content
        if ($message instanceof UserMessage) {
            return $message->content ?? '';
        }

        // AssistantMessage: propriedade $content + possíveis toolCalls
        if ($message instanceof AssistantMessage) {
            $text = $message->content ?? '';

            if (!empty($message->toolCalls)) {
                $text .= ' ' . json_encode($message->toolCalls, JSON_UNESCAPED_UNICODE);
            }

            return $text;
        }

        // ToolResultMessage: array de ToolResult com propriedade $result
        if ($message instanceof ToolResultMessage) {
            $parts = [];

            if (!empty($message->toolResults) && is_iterable($message->toolResults)) {
                foreach ($message->toolResults as $toolResult) {
                    $parts[] = $toolResult->result ?? '';
                }
            }

            return implode(' ', $parts);
        }

        // Fallback seguro: serializa o objeto inteiro
        return json_encode($message, JSON_UNESCAPED_UNICODE) ?: '';
    }

    /**
     * Gera um resumo compacto de uma mensagem intermediária.
     *
     * @param AssistantMessage|UserMessage|ToolResultMessage|object $message
     * @return string Resumo conciso da mensagem.
     */
    private function summarizeMessage(object $message): string
    {
        // ToolResultMessage: extrai nome da ferramenta e indica resultado
        if ($message instanceof ToolResultMessage) {
            $parts = [];

            if (!empty($message->toolResults) && is_iterable($message->toolResults)) {
                foreach ($message->toolResults as $toolResult) {
                    $toolName = $toolResult->toolName ?? 'tool';
                    $result   = $toolResult->result ?? '';

                    // Detecta se o resultado contém erro
                    $lowerResult = mb_strtolower($result, 'UTF-8');
                    if (str_contains($lowerResult, 'error') || str_contains($lowerResult, 'erro')) {
                        $parts[] = "- {$toolName}: ERRO";
                        continue;
                    }

                    // Detecta contagem de registros em JSON
                    try {
                        $decoded = json_decode($result, true, 512, JSON_THROW_ON_ERROR);
                        if (is_array($decoded)) {
                            $rowCount = isset($decoded['rows']) ? count($decoded['rows']) : count($decoded);
                            $parts[]  = "- {$toolName}: {$rowCount} registros";
                            continue;
                        }
                    } catch (\JsonException) {
                        // Não é JSON
                    }

                    $parts[] = "- {$toolName}: OK";
                }
            }

            return implode("\n", $parts);
        }

        // AssistantMessage: mantém os primeiros 200 caracteres
        if ($message instanceof AssistantMessage) {
            $content = $message->content ?? '';

            if (mb_strlen($content, 'UTF-8') > 200) {
                return '- Raciocínio: ' . mb_substr($content, 0, 200, 'UTF-8') . '...';
            }

            return '- Raciocínio: ' . $content;
        }

        // UserMessage: mantém a mensagem completa (geralmente curta)
        if ($message instanceof UserMessage) {
            return '- Usuário: ' . ($message->content ?? '');
        }

        // Fallback
        return '- [passo intermediário]';
    }
}
