from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import uuid

app = FastAPI(title="AgenteV2 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
        self.job_states: dict[str, dict] = {}
        
    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def send_event(self, client_id: str, event_type: str, data: dict):
        if client_id in self.active_connections:
            message = {"type": event_type, "data": data}
            await self.active_connections[client_id].send_text(json.dumps(message))

manager = ConnectionManager()

class QueryRequest(BaseModel):
    client_id: str
    question: str
    
class AnswerRequest(BaseModel):
    client_id: str
    job_id: str
    answer: str

@app.post("/ask")
async def ask_question(request: QueryRequest):
    job_id = str(uuid.uuid4())
    manager.job_states[job_id] = {"status": "started", "question": request.question}
    
    # Fire and forget the pipeline execution
    asyncio.create_task(run_pipeline_job(request.client_id, job_id, request.question))
    
    return {"job_id": job_id, "status": "processing"}

@app.post("/answer")
async def answer_human_in_loop(request: AnswerRequest):
    if request.job_id not in manager.job_states:
        return {"error": "Job not found"}
        
    # We will resume the job by setting the answer
    manager.job_states[request.job_id]["human_answer"] = request.answer
    return {"status": "resumed"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)
    try:
        while True:
            # Keep connection alive
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)

async def run_pipeline_job(client_id: str, job_id: str, question: str):
    # This is a stub for the real pipeline execution
    # It will be integrated with the classes from agente_v2
    try:
        await manager.send_event(client_id, "stage_update", {"stage": "IntentExtractor", "status": "started"})
        await asyncio.sleep(2) # Simulating LLM call
        await manager.send_event(client_id, "stage_update", {"stage": "IntentExtractor", "status": "done"})
        
        await manager.send_event(client_id, "stage_update", {"stage": "BusinessResolver", "status": "started"})
        await asyncio.sleep(2) # Simulating LLM call
        
        # Simulating Human-in-the-loop
        await manager.send_event(client_id, "human_input_required", {
            "job_id": job_id,
            "message": "Dúvida de negócio: qual é o bairro exato?"
        })
        
        # Wait for human input
        timeout = 60
        while timeout > 0:
            if "human_answer" in manager.job_states[job_id]:
                break
            await asyncio.sleep(1)
            timeout -= 1
            
        answer = manager.job_states[job_id].get("human_answer", "No answer")
        await manager.send_event(client_id, "stage_update", {"stage": "BusinessResolver", "status": "done", "human_answer": answer})
        
        # Finish
        await manager.send_event(client_id, "pipeline_complete", {
            "job_id": job_id,
            "sql": "SELECT * FROM bairro LIMIT 10",
            "answer": "O sistema gerou a seguinte resposta baseada em seus dados."
        })
    except Exception as e:
        await manager.send_event(client_id, "error", {"message": str(e)})
