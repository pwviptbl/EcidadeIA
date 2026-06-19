#!/bin/bash

# Script para parar todos os serviços do projeto (MCP e Laravel/Sail)
# Executar a partir da máquina host

RED='\033[0;31m'
NC='\033[0m'

BASE_DIR="/home/dbseller/Modelos/MVP"

echo -e "${RED}Parando Servidor MCP (Python)...${NC}"
pkill -f 'server.py'

echo -e "${RED}Parando Queue Worker do Laravel...${NC}"
pkill -f 'queue:work'

echo -e "${RED}Parando Vite Dev Server...${NC}"
pkill -f 'vite'

echo -e "${RED}Derrubando containers do Laravel Sail...${NC}"
cd "$BASE_DIR/AgenteV3"
./vendor/bin/sail down

echo -e "${RED}Todos os serviços foram parados.${NC}"
