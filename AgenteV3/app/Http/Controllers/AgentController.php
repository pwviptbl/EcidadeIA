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
