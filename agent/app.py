from __future__ import annotations

import json

from flask import Flask, jsonify, render_template, request

from config import AGENTE_DEBUG, AGENTE_HOST, AGENTE_PORT
from services.catalog import Catalog
from services.mcp_client import McpClient
from services.planner import AgentPlanner
from services.storage import ChatStorage


app = Flask(__name__)

storage = ChatStorage()
mcp_client = McpClient()
catalog = Catalog(mcp_client=mcp_client)
planner = AgentPlanner(catalog, mcp_client)


@app.get("/")
def index():
    conversation = storage.get_or_create_default()
    return render_template("index.html", conversation_id=conversation["id"])


@app.get("/api/bootstrap")
def bootstrap():
    conversation = storage.get_or_create_default()
    return jsonify(
        {
            "active_conversation": conversation,
            "conversations": storage.list_conversations(),
            "messages": storage.messages(conversation["id"]),
        }
    )


@app.post("/api/conversations")
def create_conversation():
    conversation = storage.create_conversation()
    return jsonify(conversation), 201


@app.get("/api/conversations/<conversation_id>/messages")
def messages(conversation_id):
    return jsonify({"messages": storage.messages(conversation_id)})


@app.delete("/api/conversations/<conversation_id>")
def delete_conversation(conversation_id):
    deleted = storage.delete_conversation(conversation_id)
    if not deleted:
        return jsonify({"message": "Conversa nao encontrada."}), 404

    active = storage.get_or_create_default()
    return jsonify(
        {
            "active_conversation": active,
            "conversations": storage.list_conversations(),
            "messages": storage.messages(active["id"]),
        }
    )


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    conversation_id = payload.get("conversation_id") or storage.get_or_create_default()["id"]
    message = str(payload.get("message") or "").strip()

    if not message:
        return jsonify({"message": "Mensagem nao informada."}), 422

    storage.rename_if_default(conversation_id, message)
    storage.add_message(conversation_id, "user", message)

    history = storage.messages(conversation_id)
    result = planner.handle(message, history=history)
    metadata = {
        "sql": result.sql,
        "row_count": len(result.rows or []),
        "payload": result.metadata,
    }
    storage.add_message(conversation_id, "assistant", result.answer, json.dumps(metadata, ensure_ascii=True))

    return jsonify(
        {
            "answer": result.answer,
            "sql": result.sql,
            "rows": (result.rows or [])[:50],
            "metadata": metadata,
            "conversations": storage.list_conversations(),
            "messages": storage.messages(conversation_id),
        }
    )


@app.get("/api/health")
def health():
    try:
        remote = mcp_client.health()
        ok = True
    except Exception as exc:
        remote = {"message": str(exc)}
        ok = False

    return jsonify({"ok": ok, "ecidade": remote, "planner_build": planner.BUILD_ID})


if __name__ == "__main__":
    app.run(host=AGENTE_HOST, port=AGENTE_PORT, debug=AGENTE_DEBUG)
