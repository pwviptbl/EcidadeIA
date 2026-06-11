from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

from config import DATABASE_PATH, DATA_DIR


class ChatStorage:
    def __init__(self, path: Path = DATABASE_PATH):
        self.path = path
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                create table if not exists conversations (
                    id text primary key,
                    title text not null,
                    created_at text not null,
                    updated_at text not null
                )
                """
            )
            conn.execute(
                """
                create table if not exists messages (
                    id integer primary key autoincrement,
                    conversation_id text not null,
                    role text not null,
                    content text not null,
                    metadata text,
                    created_at text not null,
                    foreign key (conversation_id) references conversations(id)
                )
                """
            )

    def list_conversations(self) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                select id, title, created_at, updated_at
                from conversations
                order by updated_at desc
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def create_conversation(self, title: str = "Nova conversa") -> dict:
        now = datetime.now().isoformat(timespec="seconds")
        conversation = {
            "id": uuid.uuid4().hex,
            "title": title,
            "created_at": now,
            "updated_at": now,
        }
        with self._connect() as conn:
            conn.execute(
                """
                insert into conversations (id, title, created_at, updated_at)
                values (:id, :title, :created_at, :updated_at)
                """,
                conversation,
            )
        return conversation

    def get_or_create_default(self) -> dict:
        conversations = self.list_conversations()
        if conversations:
            return conversations[0]
        return self.create_conversation("Analise")

    def delete_conversation(self, conversation_id: str) -> bool:
        with self._connect() as conn:
            current = conn.execute(
                "select id from conversations where id = ?",
                (conversation_id,),
            ).fetchone()

            if not current:
                return False

            conn.execute("delete from messages where conversation_id = ?", (conversation_id,))
            conn.execute("delete from conversations where id = ?", (conversation_id,))
            return True

    def messages(self, conversation_id: str) -> list[dict]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                select id, role, content, created_at
                from messages
                where conversation_id = ?
                order by id asc
                """,
                (conversation_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def add_message(self, conversation_id: str, role: str, content: str, metadata: str | None = None):
        now = datetime.now().isoformat(timespec="seconds")
        with self._connect() as conn:
            conn.execute(
                """
                insert into messages (conversation_id, role, content, metadata, created_at)
                values (?, ?, ?, ?, ?)
                """,
                (conversation_id, role, content, metadata, now),
            )
            conn.execute(
                "update conversations set updated_at = ?, title = coalesce(nullif(title, ''), ?) where id = ?",
                (now, self._title_from_content(content), conversation_id),
            )

    def rename_if_default(self, conversation_id: str, first_message: str):
        title = self._title_from_content(first_message)
        with self._connect() as conn:
            current = conn.execute(
                "select title from conversations where id = ?",
                (conversation_id,),
            ).fetchone()
            if current and current["title"] in ("Nova conversa", "Analise"):
                conn.execute(
                    "update conversations set title = ? where id = ?",
                    (title, conversation_id),
                )

    def _title_from_content(self, content: str) -> str:
        title = " ".join(content.strip().split())
        return title[:60] if title else "Nova conversa"
