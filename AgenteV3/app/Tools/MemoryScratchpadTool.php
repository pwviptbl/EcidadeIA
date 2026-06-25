<?php

namespace App\Tools;

use Prism\Prism\Tool;

class MemoryScratchpadTool extends Tool
{
    public function __construct()
    {
        $this->as('update_memory_scratchpad')
            ->for('Atualiza o bloco de memoria temporal da sessao. Útil para anotar descobertas de metadados, colunas corretas de relacionamento e fatos importantes que o agente deve se lembrar nos proximos passos do loop, evitando perda de contexto.')
            ->withStringParameter('anotacao', 'O texto com as conclusoes/schemas que devem ser mantidos na memoria do agente.')
            ->using(fn (string $anotacao) => $this->execute($anotacao));
    }

    protected function execute(string $anotacao): string
    {
        return json_encode([
            'status' => 'sucesso',
            'mensagem' => 'Scratchpad atualizado com sucesso. Esta memoria acompanhara as proximas requisicoes.',
            'conteudo_armazenado' => $anotacao
        ], JSON_UNESCAPED_UNICODE);
    }
}
