#!/bin/bash

# Script para iniciar todos os serviços do projeto (MCP e Laravel/Sail)
# Executar a partir da máquina host

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BASE_DIR="/home/dbseller/Modelos/MVP"

echo -e "${BLUE}=== 1. Iniciando Servidor MCP (Python) ===${NC}"
cd "$BASE_DIR/mcp"
if [ ! -d ".venv" ]; then
    echo "Ambiente virtual .venv não encontrado em $BASE_DIR/mcp. Criando..."
    python3 -m venv .venv
fi

# Ativa venv e instala dependências se necessário
source .venv/bin/activate
pip install -r requirements.txt

# Inicia o servidor MCP em background
echo "Rodando servidor MCP na porta 8010..."
nohup env MCP_TRANSPORT=streamable-http MCP_HOST=0.0.0.0 MCP_PORT=8010 python3 server.py > mcp_server.log 2>&1 &
MCP_PID=$!
echo -e "${GREEN}✔ Servidor MCP iniciado em background (PID: $MCP_PID). Logs em mcp/mcp_server.log${NC}"
deactivate

echo -e "\n${BLUE}=== 2. Iniciando Laravel Sail (Docker) ===${NC}"
cd "$BASE_DIR/AgenteV3"
./vendor/bin/sail up -d
echo -e "${GREEN}✔ Containers iniciados.${NC}"

# Verifica node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${BLUE}Instalando dependências do Node (npm install)...${NC}"
    ./vendor/bin/sail npm install
fi

echo -e "\n${BLUE}=== 2.1 Iniciando Laravel Reverb (Websockets) ===${NC}"
nohup ./vendor/bin/sail artisan reverb:start --host=0.0.0.0 --port=8090 > reverb.log 2>&1 &
REVERB_PID=$!
echo -e "${GREEN}✔ Laravel Reverb iniciado em background. Logs em AgenteV3/reverb.log${NC}"

echo -e "\n${BLUE}=== 3. Iniciando Queue Worker ===${NC}"
nohup ./vendor/bin/sail artisan queue:work > queue_worker.log 2>&1 &
QUEUE_PID=$!
echo -e "${GREEN}✔ Queue Worker iniciado em background. Logs em AgenteV3/queue_worker.log${NC}"

echo -e "\n${BLUE}=== 4. Iniciando Vite Dev Server ===${NC}"
nohup ./vendor/bin/sail npm run dev > vite_dev.log 2>&1 &
VITE_PID=$!
echo -e "${GREEN}✔ Vite iniciado em background. Logs em AgenteV3/vite_dev.log${NC}"

echo -e "\n${GREEN}=== Tudo pronto! ===${NC}"
echo "Para parar os serviços rodando em background no host, você pode rodar:"
echo "  pkill -f 'server.py'"
echo "  pkill -f 'queue:work'"
echo "  pkill -f 'vite'"
echo "  cd $BASE_DIR/AgenteV3 && ./vendor/bin/sail down"
