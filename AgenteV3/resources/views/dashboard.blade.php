<!DOCTYPE html>
<html lang="pt-BR" class="h-full">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Cidade Agente - Painel de Controle</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                        outfit: ['Outfit', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#eef2ff',
                            100: '#e0e7ff',
                            500: '#6366f1',
                            600: '#4f46e5',
                            700: '#4338ca',
                            900: '#312e81',
                        },
                        dark: {
                            950: '#070a13',
                            900: '#0f1322',
                            800: '#1d243d',
                            700: '#2d375a',
                        }
                    }
                }
            }
        }
    </script>
    <!-- CSS Customizado para Glassmorphism e Ajustes -->
    <style>
        body {
            background-color: #070a13;
            color: #f1f5f9;
        }
        .glass {
            background: rgba(15, 19, 34, 0.75);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glass-highlight {
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.25);
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: rgba(15, 19, 34, 0.5);
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.3);
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.5);
        }
        @keyframes pulse-slow {
            0%, 100% { opacity: 0.2; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.05); }
        }
        .glow-bg {
            position: absolute;
            width: 400px;
            height: 400px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            animation: pulse-slow 8s infinite ease-in-out;
        }
    </style>
    <!-- Pusher & Echo via CDN -->
    <script src="https://js.pusher.com/8.0.1/pusher.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/laravel-echo@1.16.0/dist/echo.iife.js"></script>
    <!-- Alpine.js -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.13.3/dist/cdn.min.js"></script>
</head>
<body class="h-full font-sans antialiased overflow-hidden flex flex-col relative" x-data="agentDashboard()">

    <!-- Efeitos de Brilho de Fundo -->
    <div class="glow-bg top-[-100px] left-[-100px]" style="animation-delay: 0s;"></div>
    <div class="glow-bg bottom-[-100px] right-[-100px]" style="animation-delay: 4s;"></div>

    <!-- Modal de Confirmação de Exclusão -->
    <div x-show="showDeleteConfirm" 
         class="fixed inset-0 z-50 flex items-center justify-center p-4"
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0 scale-95"
         x-transition:enter-end="opacity-100 scale-100"
         x-transition:leave="transition ease-in duration-200"
         x-transition:leave-start="opacity-100 scale-100"
         x-transition:leave-end="opacity-0 scale-95"
         style="display: none;">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-slate-950/65 backdrop-blur-sm" @click="showDeleteConfirm = false"></div>
        
        <!-- Card -->
        <div class="glass max-w-sm w-full rounded-2xl p-6 relative z-10 flex flex-col gap-4 shadow-2xl border border-white/10">
            <!-- Icon -->
            <div class="mx-auto w-12 h-12 rounded-full bg-rose-500/10 border border-rose-500/30 flex items-center justify-center text-rose-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
            </div>
            
            <!-- Title & Description -->
            <div class="text-center">
                <h3 class="text-base font-extrabold font-outfit text-white">Excluir Conversa?</h3>
                <p class="text-slate-400 text-xs mt-2 leading-relaxed">
                    Tem certeza que deseja apagar a memória desta conversa? A IA esquecerá todo o contexto das perguntas anteriores de forma definitiva.
                </p>
            </div>
            
            <!-- Actions -->
            <div class="flex gap-3 mt-2">
                <button @click="showDeleteConfirm = false" 
                        class="flex-1 bg-slate-900 hover:bg-slate-800 text-slate-300 font-bold py-2.5 px-4 rounded-xl border border-white/5 transition duration-150 text-xs">
                    Cancelar
                </button>
                <button @click="confirmDeleteSession()" 
                        class="flex-1 bg-rose-600 hover:bg-rose-700 text-white font-bold py-2.5 px-4 rounded-xl transition duration-150 text-xs shadow-lg shadow-rose-600/10">
                    Confirmar
                </button>
            </div>
        </div>
    </div>

    <!-- Header -->
    <header class="glass z-10 py-4 px-6 flex justify-between items-center border-b border-white/10 shrink-0">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-brand-500/20">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
            </div>
            <div>
                <h1 class="text-xl font-extrabold font-outfit tracking-wide bg-gradient-to-r from-white via-slate-100 to-brand-500 bg-clip-text text-transparent">
                    E-CIDADE AGENTE
                </h1>
                <p class="text-xs text-slate-400 font-medium tracking-wider">LOOP AUTÔNOMO DE RACIOCÍNIO & EXECUÇÃO</p>
            </div>
        </div>
        
        <!-- Status de Conexões e Ações -->
        <div class="flex items-center gap-4 text-xs font-semibold" x-data="{ wsStatus: 'desconectado', mcpStatus: 'conectando' }" x-init="
            // Verificar WebSocket após inicialização
            setTimeout(() => {
                if (window.Echo && window.Echo.connector.pusher.connection.state === 'connected') {
                    wsStatus = 'conectado';
                }
                window.Echo.connector.pusher.connection.bind('state_change', (states) => {
                    wsStatus = states.current;
                });
            }, 1000);
            
            // Simular/verificar MCP
            fetch('/api/user').catch(() => {}).finally(() => { mcpStatus = 'online'; });
        ">
            <!-- Botão Limpar Conversa -->
            <button @click="clearSession()" x-show="sessionId" class="flex items-center gap-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 px-3 py-1.5 rounded-full border border-rose-500/20 transition duration-200" title="Apagar a memória da sessão atual">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                <span>Limpar Conversa</span>
            </button>

            <!-- WebSocket Status -->
            <div class="flex items-center gap-2 bg-slate-900/60 px-3 py-1.5 rounded-full border border-white/5">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" 
                          :class="wsStatus === 'connected' || wsStatus === 'conectado' ? 'bg-emerald-400' : 'bg-rose-400'"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2"
                          :class="wsStatus === 'connected' || wsStatus === 'conectado' ? 'bg-emerald-500' : 'bg-rose-500'"></span>
                </span>
                <span class="text-slate-300">WebSocket:</span>
                <span class="text-slate-100 uppercase" x-text="wsStatus">verificando</span>
            </div>

            <!-- MCP Status -->
            <div class="flex items-center gap-2 bg-slate-900/60 px-3 py-1.5 rounded-full border border-white/5">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-emerald-400"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                <span class="text-slate-300">MCP Server:</span>
                <span class="text-slate-100 uppercase">ONLINE</span>
            </div>
        </div>
    </header>

    <!-- Main Workspace -->
    <main class="flex-1 flex overflow-hidden z-10">

        <!-- Barra Lateral: Histórico de Conversas -->
        <aside class="w-64 glass border-r border-white/5 h-full flex flex-col shrink-0">
            <!-- Botão Nova Conversa -->
            <div class="p-4 border-b border-white/5 flex flex-col gap-2 shrink-0">
                <button @click="startNewChat()" 
                        class="w-full flex items-center justify-center gap-2 bg-brand-600 hover:bg-brand-700 text-white rounded-xl px-4 py-3 text-sm font-semibold transition duration-200 shadow-lg shadow-brand-500/10">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                    </svg>
                    <span>Nova Conversa</span>
                </button>
            </div>

            <!-- Lista de Conversas -->
            <div class="flex-1 overflow-y-auto p-3 custom-scrollbar flex flex-col gap-2">
                <template x-for="sess in sessions" :key="sess.session_id">
                    <div class="group flex items-center justify-between rounded-xl p-3 text-xs font-medium cursor-pointer transition duration-200"
                         :class="sessionId === sess.session_id ? 'glass-highlight text-white' : 'hover:bg-white/5 text-slate-400 hover:text-slate-200'"
                         @click="selectSession(sess.session_id)">
                        
                        <div class="flex items-center gap-2.5 min-w-0 flex-1">
                            <svg class="w-4 h-4 text-slate-500 group-hover:text-brand-400 shrink-0" 
                                 :class="sessionId === sess.session_id ? 'text-brand-400' : ''" 
                                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                            </svg>
                            <div class="flex flex-col min-w-0">
                                <span class="truncate font-semibold text-slate-200" x-text="sess.question"></span>
                                <span class="text-[9px] text-slate-500 mt-0.5" x-text="formatDate(sess.last_active_at)"></span>
                            </div>
                        </div>

                        <!-- Botão Deletar Conversa -->
                        <button @click.stop="clearSession(sess.session_id)" 
                                class="opacity-0 group-hover:opacity-100 hover:bg-rose-500/10 hover:text-rose-400 p-1.5 rounded-lg text-slate-500 transition duration-150"
                                title="Excluir conversa">
                            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                            </svg>
                        </button>
                    </div>
                </template>
                <template x-if="sessions.length === 0">
                    <div class="text-center py-8 text-slate-500 text-[11px]">
                        Nenhuma conversa anterior
                    </div>
                </template>
            </div>
        </aside>

        <!-- Painel Esquerdo: Input de Pergunta & Resposta Final -->
        <section class="flex-1 flex flex-col border-r border-white/5 h-full relative">
            <!-- Conversa Principal -->
            <div class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col gap-6" id="chat-messages">
                <!-- Se estiver vazio, exibe tela de boas-vindas / sugestões -->
                <template x-if="messages.length === 0">
                    <div class="my-auto max-w-lg mx-auto text-center flex flex-col items-center">
                        <div class="w-16 h-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center mb-6 text-indigo-400">
                            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                            </svg>
                        </div>
                        <h2 class="text-2xl font-bold font-outfit text-white mb-2">Como posso ajudar no e-Cidade?</h2>
                        <p class="text-slate-400 text-sm mb-8">Digite uma pergunta de negócio. O E-CidadeIA irá raciocinar sobre as regras usando RAG e rodar queries SQL de forma autônoma.</p>
                        
                        <div class="grid grid-cols-1 gap-3 w-full">
                            <button @click="setQuestion('Quais são as isenções de IPTU concedidas no bairro Icaraí em 2026?')" 
                                    class="text-left text-xs bg-slate-900/50 hover:bg-slate-800/50 border border-white/5 hover:border-brand-500/30 p-3 rounded-xl transition duration-200 flex items-center justify-between group">
                                <span class="text-slate-300 group-hover:text-white">Isenções de IPTU no Bairro Icaraí (2026)</span>
                                <svg class="w-4 h-4 text-slate-500 group-hover:text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                            </button>
                            <button @click="setQuestion('Qual o valor total isento de IPTU?')" 
                                    class="text-left text-xs bg-slate-900/50 hover:bg-slate-800/50 border border-white/5 hover:border-brand-500/30 p-3 rounded-xl transition duration-200 flex items-center justify-between group">
                                <span class="text-slate-300 group-hover:text-white">Valor total isento de IPTU</span>
                                <svg class="w-4 h-4 text-slate-500 group-hover:text-brand-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
                            </button>
                        </div>
                    </div>
                </template>

                <!-- Histórico de Perguntas e Respostas Finais -->
                <template x-for="(msg, index) in messages" :key="index">
                    <div class="flex flex-col gap-3">
                        <!-- Pergunta do Usuário -->
                        <template x-if="msg.type === 'user'">
                            <div class="flex gap-3 self-end max-w-[85%]">
                                <div class="bg-brand-600 text-white rounded-2xl rounded-tr-none px-4 py-3 shadow-md shadow-brand-500/10 text-sm">
                                    <p class="font-medium" x-text="msg.content"></p>
                                </div>
                            </div>
                        </template>

                        <!-- Resposta da IA -->
                        <template x-if="msg.type === 'agent'">
                            <div class="flex gap-3 self-start max-w-[90%]">
                                <div class="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                                    </svg>
                                </div>
                                <div class="glass rounded-2xl rounded-tl-none p-5 text-sm flex flex-col gap-4 w-full">
                                    <div class="prose prose-invert text-slate-200 leading-relaxed font-medium">
                                        <span x-html="formatResponse(msg.content)"></span>
                                    </div>
                                    
                                    <!-- Renderização da tabela de dados final (se extraída) -->
                                    <template x-if="msg.tableData && msg.tableData.length > 0">
                                        <div class="overflow-x-auto rounded-xl border border-white/10 max-h-60 custom-scrollbar">
                                            <table class="min-w-full divide-y divide-white/10 text-xs">
                                                <thead class="bg-slate-900/80 sticky top-0">
                                                    <tr>
                                                        <template x-for="col in Object.keys(msg.tableData[0])" :key="col">
                                                            <th scope="col" class="px-4 py-2 text-left font-bold text-slate-400 uppercase tracking-wider" x-text="col"></th>
                                                        </template>
                                                    </tr>
                                                </thead>
                                                <tbody class="divide-y divide-white/5 bg-slate-950/20">
                                                    <template x-for="(row, rIndex) in msg.tableData" :key="rIndex">
                                                        <tr class="hover:bg-white/5 transition duration-150">
                                                            <template x-for="val in Object.values(row)" :key="val">
                                                                <td class="px-4 py-2 whitespace-nowrap text-slate-300 font-mono" x-text="val"></td>
                                                            </template>
                                                        </tr>
                                                    </template>
                                                </tbody>
                                            </table>
                                        </div>
                                    </template>

                                    <!-- Mostrar SQL executado se houver -->
                                    <template x-if="msg.sql">
                                        <details class="group bg-slate-950/80 rounded-xl border border-white/10 overflow-hidden mt-3">
                                            <summary class="flex justify-between items-center px-4 py-2.5 text-xs font-bold text-slate-300 cursor-pointer select-none hover:bg-white/5 transition duration-150">
                                                <div class="flex items-center gap-2">
                                                    <svg class="w-4 h-4 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                                                    </svg>
                                                    <span>Visualizar Query SQL Utilizada</span>
                                                </div>
                                                <div class="flex items-center gap-3">
                                                    <!-- Badge de performance da query -->
                                                    <template x-if="msg.durationMs != null">
                                                        <span
                                                            :class="{
                                                                'bg-emerald-500/15 text-emerald-400 border-emerald-500/30': msg.durationMs < 500,
                                                                'bg-amber-500/15 text-amber-400 border-amber-500/30': msg.durationMs >= 500 && msg.durationMs < 2000,
                                                                'bg-red-500/15 text-red-400 border-red-500/30': msg.durationMs >= 2000
                                                            }"
                                                            class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold border tracking-wider"
                                                        >
                                                            <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 20 20">
                                                                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clip-rule="evenodd"></path>
                                                            </svg>
                                                            <span x-text="msg.durationMs < 1000 ? msg.durationMs + 'ms' : (msg.durationMs/1000).toFixed(1) + 's'"></span>
                                                        </span>
                                                    </template>
                                                    <svg class="w-4 h-4 text-slate-500 group-open:rotate-180 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                                                    </svg>
                                                </div>
                                            </summary>
                                            <div class="p-4 border-t border-white/5 bg-slate-950/40 font-mono text-xs text-emerald-400 overflow-x-auto whitespace-pre-wrap leading-relaxed max-h-60 custom-scrollbar" x-text="msg.sql"></div>
                                        </details>
                                    </template>
                                </div>
                            </div>
                        </template>
                    </div>
                </template>

                <!-- Loader do Chat (Skeleton Loader Premium) -->
                <template x-if="isLoading">
                    <div class="flex gap-3 self-start max-w-[85%] animate-pulse">
                        <div class="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400 shrink-0">
                            <svg class="animate-spin w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        </div>
                        <div class="glass rounded-2xl rounded-tl-none p-4 text-xs flex flex-col gap-2.5 w-64">
                            <div class="flex items-center gap-1.5 text-indigo-400 font-semibold uppercase tracking-wider text-[10px]">
                                <span>Agente está processando</span>
                                <span class="flex gap-0.5">
                                    <span class="animate-bounce" style="animation-delay: 0.1s">.</span>
                                    <span class="animate-bounce" style="animation-delay: 0.2s">.</span>
                                    <span class="animate-bounce" style="animation-delay: 0.3s">.</span>
                                </span>
                            </div>
                            <p class="text-[10px] text-slate-400 leading-relaxed">
                                O agente está pesquisando as regras de negócio e executando queries SQL de forma autônoma.<br>
                                <strong>Aviso:</strong> Consultas complexas em grandes volumes de dados podem levar alguns minutos para finalizar.
                            </p>
                            <div class="h-2 bg-white/10 rounded-full w-full"></div>
                            <div class="h-2 bg-white/10 rounded-full w-5/6"></div>
                            <div class="h-2 bg-white/10 rounded-full w-2/3"></div>
                        </div>
                    </div>
                </template>
            </div>

            <!-- Caixa de Texto / Input -->
            <div class="p-4 bg-slate-950/40 border-t border-white/5">
                <form @submit.prevent="submitQuestion" class="flex gap-3 items-center">
                    <input type="text" x-model="inputQuestion" placeholder="Faça uma pergunta ao E-CidadeIA..." 
                           :disabled="isLoading"
                           class="flex-1 bg-slate-900/80 border border-white/10 hover:border-white/20 focus:border-brand-500 focus:ring-1 focus:ring-brand-500 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-500 focus:outline-none transition duration-200 disabled:opacity-50">
                    <button type="submit" :disabled="isLoading || !inputQuestion.trim()"
                            class="bg-brand-600 hover:bg-brand-700 disabled:bg-slate-800 disabled:opacity-40 text-white rounded-xl px-5 py-3 text-sm font-semibold transition duration-200 flex items-center gap-2 shadow-lg shadow-brand-500/10">
                        <span>Enviar</span>
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                        </svg>
                    </button>
                </form>
            </div>
        </section>

        <!-- Painel Direito: Orquestração ReAct em Tempo Real -->
        <section class="flex-1 flex flex-col bg-slate-950/35 h-full overflow-hidden">
            <!-- Header do painel -->
            <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center shrink-0">
                <div class="flex items-center gap-2">
                    <svg class="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                    </svg>
                    <h2 class="text-sm font-bold font-outfit text-white tracking-wide">PAINEL DE EXECUÇÃO REACT</h2>
                </div>
                <!-- ID de Sessão -->
                <div class="text-[10px] text-slate-500 font-mono">
                    SESSION_ID: <span class="text-slate-400 font-bold" x-text="sessionId ? sessionId.substring(0,8) + '...' : 'NENHUMA'">NENHUMA</span>
                </div>
            </div>

            <!-- Timeline dos Passos (Steps) -->
            <div class="flex-1 overflow-y-auto p-6 custom-scrollbar flex flex-col gap-6" id="steps-timeline">
                
                <template x-if="steps.length === 0">
                    <div class="my-auto text-center flex flex-col items-center p-6 text-slate-500">
                        <svg class="w-12 h-12 mb-4 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                        </svg>
                        <h3 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Aguardando Execução</h3>
                        <p class="text-xs max-w-xs leading-relaxed">Envie uma pergunta para ver o fluxo de reflexão da IA e execução de ferramentas em tempo real.</p>
                    </div>
                </template>

                <!-- Loop de Passos do Agente -->
                <template x-for="(step, sIdx) in steps" :key="sIdx">
                    <div class="flex gap-4 relative">
                        <!-- Linha Conectora da Timeline -->
                        <template x-if="sIdx < steps.length - 1">
                            <div class="absolute left-4 top-8 bottom-0 w-[2px] bg-slate-800"></div>
                        </template>

                        <!-- Marcador de Número do Passo -->
                        <div class="w-8 h-8 rounded-full bg-slate-900 border-2 border-indigo-500 flex items-center justify-center text-xs font-extrabold text-indigo-400 shrink-0 z-10"
                             :class="{ 'animate-pulse bg-indigo-500/20 border-indigo-400': !step.finishReason }">
                            <span x-text="step.stepCount || (sIdx + 1)"></span>
                        </div>

                        <!-- Card do Passo -->
                        <div class="flex-1 glass rounded-xl p-4 flex flex-col gap-3">
                            
                            <!-- Título do Raciocínio (Thought) -->
                            <div class="flex items-center gap-2 border-b border-white/5 pb-2">
                                <span class="w-2 h-2 rounded-full bg-indigo-400"></span>
                                <h4 class="text-xs font-bold text-indigo-300 uppercase tracking-wider">Pensamento do Agente</h4>
                            </div>

                            <!-- Texto do Pensamento -->
                            <p class="text-xs text-slate-300 leading-relaxed font-medium font-sans" x-text="step.text || 'Processando raciocínio...'"></p>

                            <!-- Ferramentas chamadas neste passo -->
                            <template x-if="step.toolCalls && step.toolCalls.length > 0">
                                <div class="flex flex-col gap-3 mt-2 border-t border-white/5 pt-3">
                                    <template x-for="(call, cIdx) in step.toolCalls" :key="cIdx">
                                        <div class="flex flex-col gap-2">
                                            <!-- Cabeçalho da Ferramenta Chamada -->
                                            <div class="flex items-center justify-between">
                                                <div class="flex items-center gap-2">
                                                    <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 uppercase tracking-wide">
                                                        AÇÃO (TOOL CALL)
                                                    </span>
                                                    <span class="text-xs font-mono font-bold text-slate-200" x-text="call.name"></span>
                                                </div>
                                            </div>

                                            <!-- Argumentos da Chamada -->
                                            <div class="bg-slate-950/80 rounded-lg p-3 border border-white/5">
                                                <span class="text-[10px] text-slate-500 font-bold uppercase tracking-wider">Argumentos:</span>
                                                <pre class="text-xs font-mono text-emerald-400 overflow-x-auto mt-1 custom-scrollbar leading-relaxed whitespace-pre-wrap" x-text="formatArguments(call.arguments)"></pre>
                                            </div>

                                            <!-- Resultado Correspondente à Ferramenta -->
                                            <template x-if="step.toolResults && step.toolResults[cIdx]">
                                                <div class="flex flex-col gap-1.5 mt-1">
                                                    <div class="flex items-center gap-2">
                                                        <span class="px-2 py-0.5 text-[10px] font-bold rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 uppercase tracking-wide">
                                                            RESULTADO (TOOL RESULT)
                                                        </span>
                                                    </div>
                                                    
                                                    <!-- Visualização de Resultados -->
                                                    <div class="bg-slate-950/50 rounded-lg p-3 border border-white/5 max-h-80 overflow-y-auto custom-scrollbar">
                                                        <!-- Se o resultado for uma tabela SQL (array de objetos) -->
                                                        <template x-if="isSqlResult(call.name, step.toolResults[cIdx].result)">
                                                            <div class="overflow-x-auto rounded border border-white/5">
                                                                <table class="min-w-full divide-y divide-white/10 text-[11px]">
                                                                    <thead class="bg-slate-900">
                                                                        <tr>
                                                                            <template x-for="col in getSqlResultColumns(step.toolResults[cIdx].result)" :key="col">
                                                                                <th scope="col" class="px-3 py-1.5 text-left font-bold text-slate-400 uppercase tracking-wider" x-text="col"></th>
                                                                            </template>
                                                                        </tr>
                                                                    </thead>
                                                                    <tbody class="divide-y divide-white/5 bg-slate-950/10">
                                                                        <template x-for="(row, rIndex) in getSqlResultRows(step.toolResults[cIdx].result)" :key="rIndex">
                                                                            <tr class="hover:bg-white/5 transition duration-150">
                                                                                <template x-for="val in Object.values(row)" :key="val">
                                                                                    <td class="px-3 py-1.5 whitespace-nowrap text-slate-300 font-mono" x-text="val"></td>
                                                                                </template>
                                                                            </tr>
                                                                        </template>
                                                                    </tbody>
                                                                </table>
                                                            </div>
                                                        </template>

                                                        <!-- Se for outro tipo de resultado (Ex: Markdown de RAG) -->
                                                        <template x-if="!isSqlResult(call.name, step.toolResults[cIdx].result)">
                                                            <pre class="text-[11px] font-mono text-slate-300 whitespace-pre-wrap leading-relaxed" x-text="formatToolResult(step.toolResults[cIdx].result)"></pre>
                                                        </template>
                                                    </div>
                                                </div>
                                            </template>
                                        </div>
                                    </template>
                                </div>
                            </template>

                            <!-- Finish Reason (se finalizou o passo) -->
                            <template x-if="step.finishReason">
                                <div class="mt-2 text-[10px] text-right font-semibold text-slate-500 uppercase tracking-wider">
                                    Status do Passo: <span class="text-indigo-400" x-text="step.finishReason">stop</span>
                                </div>
                            </template>

                        </div>
                    </div>
                </template>
                
            </div>
        </section>
    </main>

    <!-- Rodapé -->
    <footer class="glass py-2 px-6 border-t border-white/5 text-center text-[10px] text-slate-500 z-10 shrink-0 flex justify-between">
        <span>E-Cidade IA &copy; 2026. Todos os direitos reservados.</span>
        <span>Desenvolvido com Laravel Reverb, Prism & Google Gemini 2.5 Flash</span>
    </footer>

    <!-- Scripts da Aplicação Dashboard -->
    <script>
        function agentDashboard() {
            return {
                inputQuestion: '',
                isLoading: false,
                sessionId: localStorage.getItem('agent_session_id') || '',
                messages: [],
                steps: [],
                sessions: [],
                showDeleteConfirm: false,
                sessionToDelete: null,

                init() {
                    window.Pusher = Pusher;
                    
                    this.loadSessions();
                    
                    if (this.sessionId) {
                        this.loadHistory();
                    }
                    
                    try {
                        // O CDN do Laravel Echo pode expor LaravelEcho ou Echo
                        const EchoClass = window.LaravelEcho || window.Echo;
                        if (EchoClass) {
                            window.Echo = new EchoClass({
                                broadcaster: 'reverb',
                                key: '{{ env('REVERB_APP_KEY') }}',
                                wsHost: window.location.hostname,
                                wsPort: {{ env('REVERB_PORT', 8090) }},
                                forceTLS: false,
                                enabledTransports: ['ws', 'wss'],
                                disableStats: true
                            });
                            console.log('Laravel Echo inicializado com sucesso.');
                        } else {
                            console.error('Classe Echo ou LaravelEcho não encontrada no escopo global.');
                        }
                    } catch (e) {
                        console.error('Falha ao inicializar o Laravel Echo:', e);
                    }
                },

                loadSessions() {
                    fetch('/api/sessions')
                        .then(res => res.json())
                        .then(data => {
                            this.sessions = data.sessions || [];
                        })
                        .catch(err => console.error('Erro ao carregar sessões:', err));
                },

                loadHistory() {
                    this.messages = [];
                    this.steps = [];
                    if (!this.sessionId) return;
                    fetch('/api/history/' + this.sessionId)
                        .then(res => res.json())
                        .then(data => {
                            if (data.messages && data.messages.length > 0) {
                                data.messages.forEach(msg => {
                                    this.messages.push({
                                        type: 'user',
                                        content: msg.question
                                    });
                                    this.messages.push({
                                        type: 'agent',
                                        content: msg.response,
                                        sql: msg.sql_used
                                    });
                                });
                                this.$nextTick(() => {
                                    this.scrollToBottom('chat-messages');
                                });
                            }
                        })
                        .catch(err => console.error('Erro ao carregar histórico:', err));
                },

                selectSession(sessionId) {
                    if (this.sessionId === sessionId) return;
                    this.sessionId = sessionId;
                    localStorage.setItem('agent_session_id', sessionId);
                    this.loadHistory();
                },

                startNewChat() {
                    this.sessionId = 'session_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
                    localStorage.setItem('agent_session_id', this.sessionId);
                    this.messages = [];
                    this.steps = [];
                },

                clearSession(targetSessionId = null) {
                    const sid = targetSessionId || this.sessionId;
                    if (!sid) return;
                    this.sessionToDelete = sid;
                    this.showDeleteConfirm = true;
                },

                confirmDeleteSession() {
                    const sid = this.sessionToDelete;
                    if (!sid) return;
                    this.showDeleteConfirm = false;

                    fetch('/api/history/' + sid, {
                        method: 'DELETE',
                        headers: {
                            'X-CSRF-TOKEN': '{{ csrf_token() }}'
                        }
                    }).then(() => {
                        if (sid === this.sessionId) {
                            this.sessionId = '';
                            this.messages = [];
                            this.steps = [];
                            localStorage.removeItem('agent_session_id');
                        }
                        this.sessionToDelete = null;
                        this.loadSessions();
                    });
                },

                formatDate(dateStr) {
                    if (!dateStr) return '';
                    try {
                        const date = new Date(dateStr);
                        const day = String(date.getDate()).padStart(2, '0');
                        const month = String(date.getMonth() + 1).padStart(2, '0');
                        const hours = String(date.getHours()).padStart(2, '0');
                        const minutes = String(date.getMinutes()).padStart(2, '0');
                        return `${day}/${month} ${hours}:${minutes}`;
                    } catch (e) {
                        return dateStr;
                    }
                },

                setQuestion(question) {
                    this.inputQuestion = question;
                },

                formatArguments(args) {
                    if (typeof args === 'string') return args;
                    try {
                        return JSON.stringify(args, null, 2);
                    } catch (e) {
                        return String(args);
                    }
                },

                formatToolResult(result) {
                    if (typeof result !== 'string') {
                        try {
                            return JSON.stringify(result, null, 2);
                        } catch (e) {
                            return String(result);
                        }
                    }
                    return result;
                },

                isSqlResult(toolName, result) {
                    if (toolName !== 'mcp_execute_sql') return false;
                    try {
                        const parsed = typeof result === 'string' ? JSON.parse(result) : result;
                        return Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object';
                    } catch (e) {
                        return false;
                    }
                },

                getSqlResultColumns(result) {
                    try {
                        const parsed = typeof result === 'string' ? JSON.parse(result) : result;
                        return Object.keys(parsed[0]);
                    } catch (e) {
                        return [];
                    }
                },

                getSqlResultRows(result) {
                    try {
                        const parsed = typeof result === 'string' ? JSON.parse(result) : result;
                        return parsed;
                    } catch (e) {
                        return [];
                    }
                },

                formatResponse(text) {
                    if (!text) return '';
                    // Conversão super básica de quebras de linha e markdown negrito
                    let formatted = text
                        .replace(/\n/g, '<br>')
                        .replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-semibold">$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em class="text-slate-300">$1</em>');
                    return formatted;
                },

                // Função auxiliar para tentar extrair e formatar tabelas do texto final também
                extractTableData(text) {
                    return null;
                },

                submitQuestion() {
                    const question = this.inputQuestion.trim();
                    if (!question || this.isLoading) return;

                    // Reinicia estado de sessão e passos
                    this.isLoading = true;
                    // Gera um UUID único para a sessão se nao existir
                    if (!this.sessionId) {
                        this.sessionId = 'session_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
                        localStorage.setItem('agent_session_id', this.sessionId);
                    }
                    this.steps = [];
                    
                    // Adiciona pergunta do usuário ao chat
                    this.messages.push({
                        type: 'user',
                        content: question
                    });
                    this.inputQuestion = '';

                    // Scroll para a última mensagem
                    this.$nextTick(() => {
                        this.scrollToBottom('chat-messages');
                    });

                    // Subscreve-se ao canal WebSocket de forma resiliente
                    if (window.Echo) {
                        try {
                            console.log('Subscrevendo ao canal:', 'agent-session.' + this.sessionId);
                            window.Echo.channel('agent-session.' + this.sessionId)
                                .listen('.step.streamed', (e) => {
                                    console.log('WebSocket: Passo recebido via Reverb!', e);
                                    this.steps.push(e.stepData);
                                    
                                    this.$nextTick(() => {
                                        this.scrollToBottom('steps-timeline');
                                    });
                                });
                        } catch (wsError) {
                            console.error('Erro ao escutar canal de WebSockets:', wsError);
                        }
                    } else {
                        console.warn('Serviço de WebSocket (Echo) não disponível. Timeline em tempo real desativada.');
                    }

                    // Dispara a requisição HTTP para a API
                    fetch('/api/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': '{{ csrf_token() }}'
                        },
                        body: JSON.stringify({
                            question: question,
                            session_id: this.sessionId
                        })
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Falha na resposta do servidor.');
                        }
                        return response.json();
                    })
                    .then(data => {
                        console.log('Resposta final do agente:', data);
                        
                        // Usa data.steps do HTTP (sempre completo) para extrair SQL e dados.
                        // Antes usava this.steps (WebSocket) que pode não ter chegado ainda — race condition.
                        const sourceSteps = (data.steps && data.steps.length > 0) ? data.steps : this.steps;

                        let tableData = null;
                        let executedSql = data.sql_used || null;
                        let queryDurationMs = null;
                        
                        for (let i = sourceSteps.length - 1; i >= 0; i--) {
                            const step = sourceSteps[i];
                            if (step.toolCalls && step.toolCalls.length > 0) {
                                const sqlCallIndex = step.toolCalls.findIndex(c => c.name === 'mcp_execute_sql');
                                if (sqlCallIndex !== -1) {
                                    const args = step.toolCalls[sqlCallIndex].arguments;
                                    const currentSql = typeof args === 'string' ? args : (args.sql || JSON.stringify(args));
                                    
                                    if (step.toolResults && step.toolResults[sqlCallIndex]) {
                                        const rawRes = step.toolResults[sqlCallIndex].result;
                                        try {
                                            const parsed = typeof rawRes === 'string' ? JSON.parse(rawRes) : rawRes;
                                            let isSuccess = false;
                                            let rows = null;
                                            
                                            if (Array.isArray(parsed)) {
                                                rows = parsed;
                                                isSuccess = true;
                                            } else if (parsed && Array.isArray(parsed.rows)) {
                                                rows = parsed.rows;
                                                isSuccess = true;
                                                if (parsed.duration_ms != null) {
                                                    queryDurationMs = parsed.duration_ms;
                                                }
                                            }
                                            
                                            if (isSuccess) {
                                                tableData = rows && rows.length > 0 ? rows : null;
                                                executedSql = executedSql || currentSql;
                                                break;
                                            }
                                        } catch (e) {
                                            // Não era JSON de sucesso
                                        }
                                    }
                                }
                            }
                        }

                        // Garante que a timeline tem todos os passos mesmo se eventos WebSocket foram perdidos
                        if (data.steps && data.steps.length > this.steps.length) {
                            this.steps = data.steps;
                        }

                        // Adiciona a resposta final da IA ao chat
                        this.messages.push({
                            type: 'agent',
                            content: data.response,
                            tableData: tableData,
                            sql: executedSql,
                            durationMs: queryDurationMs
                        });
                        this.loadSessions();
                    })
                    .catch(error => {
                        console.error('Erro ao chamar o agente:', error);
                        this.messages.push({
                            type: 'agent',
                            content: 'Desculpe, ocorreu um erro ao processar sua solicitação no servidor. Verifique os logs do Laravel e do servidor MCP.'
                        });
                    })
                    .finally(() => {
                        this.isLoading = false;
                        
                        // Desinscreve-se do canal WebSocket de forma resiliente
                        if (window.Echo) {
                            try {
                                setTimeout(() => {
                                    window.Echo.leaveChannel('agent-session.' + this.sessionId);
                                    console.log('Desinscrito do canal:', 'agent-session.' + this.sessionId);
                                }, 5000);
                            } catch (e) {}
                        }

                        this.$nextTick(() => {
                            this.scrollToBottom('chat-messages');
                        });
                    });
                },

                scrollToBottom(elementId) {
                    const el = document.getElementById(elementId);
                    if (el) {
                        el.scrollTo({
                            top: el.scrollHeight,
                            behavior: 'smooth'
                        });
                    }
                }
            }
        }
    </script>
</body>
</html>
