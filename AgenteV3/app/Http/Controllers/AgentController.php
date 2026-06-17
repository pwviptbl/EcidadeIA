<?php

namespace App\Http\Controllers;

use App\Services\Agent\Orchestrator;
use Illuminate\Http\Request;

class AgentController extends Controller
{
    protected Orchestrator $orchestrator;

    public function __construct(Orchestrator $orchestrator)
    {
        $this->orchestrator = $orchestrator;
    }

    /**
     * Ponto de entrada da API (/api/ask).
     * Recebe a pergunta do usuário, valida a entrada e delega para o Orchestrator.
     * 
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse JSON contendo o histórico de passos e a resposta final.
     */
    public function ask(Request $request)
    {
        $request->validate([
            'question' => 'required|string',
            'session_id' => 'nullable|string'
        ]);

        $result = $this->orchestrator->ask(
            $request->input('question'),
            $request->input('session_id')
        );

        return response()->json($result);
    }
}
