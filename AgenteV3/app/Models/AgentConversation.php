<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AgentConversation extends Model
{
    protected $fillable = [
        'session_id',
        'question',
        'response',
        'sql_used'
    ];
}
