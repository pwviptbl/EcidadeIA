<?php

namespace App\Providers;

use App\Services\Mcp\McpClient;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Registra os serviços da aplicação no container IoC.
     */
    public function register(): void
    {
        // Registra o McpClient como singleton para compartilhar a sessão MCP
        // entre todas as tools que dependem do servidor MCP.
        $this->app->singleton(McpClient::class, function () {
            return new McpClient();
        });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        //
    }
}
