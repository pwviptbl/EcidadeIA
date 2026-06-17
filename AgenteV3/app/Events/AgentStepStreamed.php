<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class AgentStepStreamed implements ShouldBroadcastNow
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public array $stepData;
    public string $sessionId;

    /**
     * Create a new event instance.
     */
    public function __construct(string $sessionId, array $stepData)
    {
        $this->sessionId = $sessionId;
        $this->stepData = $stepData;
    }

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, Channel>
     */
    public function broadcastOn(): array
    {
        // Canal público simples para visualização direta no dashboard
        return [
            new Channel('agent-session.' . $this->sessionId),
        ];
    }

    /**
     * O nome do evento transmitido
     */
    public function broadcastAs(): string
    {
        return 'step.streamed';
    }
}
