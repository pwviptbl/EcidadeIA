<?php

namespace App\Tools;

use Prism\Prism\Tool;

class AnalyzeFailureTool extends Tool
{
    public function __construct()
    {
        $this->as('analyze_failure')
            ->for('Use esta ferramenta OBRIGATORIAMENTE após uma falha de SQL (syntax error, schema error) para estruturar a reflexao da IA. O agente deve refletir sobre a falha e propor um plano corretivo antes de tentar nova query.')
            ->withStringParameter('error_msg', 'A mensagem de erro recebida do banco de dados ou do MCP.')
            ->withStringParameter('attempted_sql', 'O comando SQL que falhou.')
            ->withStringParameter('correction_plan', 'A analise passo a passo do porquê falhou e o que será alterado.')
            ->using(fn (string $error_msg, string $attempted_sql, string $correction_plan) => $this->execute($error_msg, $attempted_sql, $correction_plan));
    }

    protected function execute(string $error_msg, string $attempted_sql, string $correction_plan): string
    {
        return json_encode([
            'status' => 'reflexao_registrada',
            'feedback' => 'A auto-crítica foi processada. Siga agora com a execução do plano corretivo utilizando as ferramentas adequadas (descrever tabelas, buscar RAG) ou execute a nova query.'
        ], JSON_UNESCAPED_UNICODE);
    }
}
