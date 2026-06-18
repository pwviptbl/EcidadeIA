<?php

namespace App\Http\Controllers;

use App\Services\Agent\Orchestrator;
use App\Models\AgentConversation;
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

    /**
     * Retorna o histórico de mensagens de uma sessão específica.
     * 
     * @param string $session_id
     * @return \Illuminate\Http\JsonResponse
     */
    public function history(string $session_id)
    {
        $history = AgentConversation::where('session_id', $session_id)
            ->orderBy('id', 'asc')
            ->get(['id', 'question', 'response', 'sql_used', 'created_at']);

        return response()->json([
            'session_id' => $session_id,
            'messages' => $history
        ]);
    }

    /**
     * Limpa o histórico de uma sessão (Exclui as conversas do banco).
     * 
     * @param string $session_id
     * @return \Illuminate\Http\JsonResponse
     */
    public function clear(string $session_id)
    {
        $deletedCount = AgentConversation::where('session_id', $session_id)->delete();

        return response()->json([
            'success' => true,
            'message' => 'Sessão limpa com sucesso.',
            'deleted_count' => $deletedCount
        ]);
    }

    /**
     * Retorna a lista de todas as sessões distintas de conversa, ordenada pela mais recente.
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function sessions()
    {
        $latestActivity = AgentConversation::selectRaw('session_id, MAX(created_at) as latest_created_at, MIN(id) as first_id')
            ->groupBy('session_id');

        $sessions = AgentConversation::joinSub($latestActivity, 'latest_act', function ($join) {
                $join->on('agent_conversations.id', '=', 'latest_act.first_id');
            })
            ->orderBy('latest_act.latest_created_at', 'desc')
            ->get([
                'agent_conversations.session_id', 
                'agent_conversations.question', 
                'latest_act.latest_created_at as last_active_at'
            ]);

        return response()->json([
            'sessions' => $sessions
        ]);
    }
}
