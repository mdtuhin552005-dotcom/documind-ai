from pathlib import Path
from typing import Any

import aiosqlite


class DocumentDatabase:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    async def initialize(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute("PRAGMA journal_mode=WAL")
            await database.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    title TEXT NOT NULL,
                    page_count INTEGER NOT NULL,
                    chunk_count INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    user_id TEXT REFERENCES users(id)
                )
                """
            )
            await database.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    user_id TEXT REFERENCES users(id)
                )
                """
            )
            await database.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL
                        REFERENCES conversations(id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    sources TEXT NOT NULL DEFAULT '[]',
                    created_at TEXT NOT NULL
                )
                """
            )
            await database.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            await database.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    token TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    created_at TEXT NOT NULL,
                    expires_at TEXT NOT NULL
                )
                """
            )
            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_conversations_updated
                ON conversations(updated_at DESC)
                """
            )
            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_conversation
                ON conversation_messages(conversation_id, id)
                """
            )
            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_sessions_user
                ON sessions(user_id)
                """
            )
            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_users_email
                ON users(email)
                """
            )
            for table in ("documents", "conversations"):
                cursor = await database.execute(f"PRAGMA table_info({table})")
                columns = {row[1] for row in await cursor.fetchall()}
                if "user_id" not in columns:
                    await database.execute(
                        f"ALTER TABLE {table} ADD COLUMN user_id TEXT REFERENCES users(id)"
                    )

            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_documents_user_created
                ON documents(user_id, created_at DESC)
                """
            )
            await database.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_conversations_user_updated
                ON conversations(user_id, updated_at DESC)
                """
            )
            cursor = await database.execute(
                "SELECT id FROM users ORDER BY created_at, id LIMIT 1"
            )
            first_user = await cursor.fetchone()
            if first_user is not None:
                await database.execute(
                    "UPDATE documents SET user_id = ? WHERE user_id IS NULL",
                    (first_user[0],),
                )
                await database.execute(
                    "UPDATE conversations SET user_id = ? WHERE user_id IS NULL",
                    (first_user[0],),
                )
            await database.commit()

    async def add_document(self, document: dict[str, Any]) -> None:
        values = {**document, "user_id": document.get("user_id")}
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute(
                """
                INSERT INTO documents
                    (id, filename, title, page_count, chunk_count, created_at, file_path, user_id)
                VALUES
                    (:id, :filename, :title, :page_count, :chunk_count, :created_at, :file_path, :user_id)
                """,
                values,
            )
            await database.commit()

    async def list_documents(self, user_id: str | None = None) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                """
                SELECT id, filename, title, page_count, chunk_count, created_at
                FROM documents
                WHERE (? IS NULL OR user_id = ?)
                ORDER BY created_at DESC
                """,
                (user_id, user_id),
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def get_document(
        self,
        document_id: str,
        user_id: str | None = None,
    ) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                "SELECT * FROM documents WHERE id = ? AND (? IS NULL OR user_id = ?)",
                (document_id, user_id, user_id),
            )
            row = await cursor.fetchone()
            return dict(row) if row is not None else None

    async def delete_document(self, document_id: str, user_id: str | None = None) -> bool:
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute("BEGIN")
            await database.execute(
                """
                DELETE FROM conversation_messages
                WHERE conversation_id IN (
                    SELECT id FROM conversations WHERE document_id = ?
                )
                """,
                (document_id,),
            )
            await database.execute(
                "DELETE FROM conversations WHERE document_id = ?",
                (document_id,),
            )
            cursor = await database.execute(
                "DELETE FROM documents WHERE id = ? AND (? IS NULL OR user_id = ?)",
                (document_id, user_id, user_id),
            )
            await database.commit()
            return cursor.rowcount > 0

    async def create_conversation(self, conversation: dict[str, Any]) -> None:
        values = {**conversation, "user_id": conversation.get("user_id")}
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute(
                """
                INSERT INTO conversations (id, document_id, title, created_at, updated_at, user_id)
                VALUES (:id, :document_id, :title, :created_at, :updated_at, :user_id)
                """,
                values,
            )
            await database.commit()

    async def list_conversations(
        self,
        limit: int = 50,
        user_id: str | None = None,
    ) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                """
                SELECT
                    conversations.id,
                    conversations.document_id,
                    conversations.title,
                    conversations.created_at,
                    conversations.updated_at,
                    documents.filename AS document_filename,
                    (SELECT content FROM conversation_messages
                     WHERE conversation_id = conversations.id
                     ORDER BY id DESC LIMIT 1) AS last_message
                FROM conversations
                JOIN documents ON documents.id = conversations.document_id
                WHERE (? IS NULL OR conversations.user_id = ?)
                ORDER BY conversations.updated_at DESC
                LIMIT ?
                """,
                (user_id, user_id, limit),
            )
            return [dict(row) for row in await cursor.fetchall()]

    async def get_conversation(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                """
                SELECT
                    conversations.id,
                    conversations.document_id,
                    conversations.title,
                    conversations.created_at,
                    conversations.updated_at,
                    documents.filename AS document_filename
                FROM conversations
                JOIN documents ON documents.id = conversations.document_id
                WHERE conversations.id = ? AND (? IS NULL OR conversations.user_id = ?)
                """,
                (conversation_id, user_id, user_id),
            )
            row = await cursor.fetchone()
            return dict(row) if row is not None else None

    async def get_conversation_messages(self, conversation_id: str) -> list[dict[str, Any]]:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                """
                SELECT role, content, sources, created_at
                FROM conversation_messages
                WHERE conversation_id = ?
                ORDER BY id
                """,
                (conversation_id,),
            )
            return [dict(row) for row in await cursor.fetchall()]

    async def add_conversation_message(self, message: dict[str, Any]) -> None:
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute(
                """
                INSERT INTO conversation_messages
                    (conversation_id, role, content, sources, created_at)
                VALUES (:conversation_id, :role, :content, :sources, :created_at)
                """,
                message,
            )
            await database.execute(
                """
                UPDATE conversations
                SET updated_at = :created_at,
                    title = CASE
                        WHEN title = 'New chat' AND :role = 'user'
                        THEN substr(:content, 1, 72)
                        ELSE title
                    END
                WHERE id = :conversation_id
                """,
                message,
            )
            await database.commit()

    async def delete_conversation(
        self,
        conversation_id: str,
        user_id: str | None = None,
    ) -> bool:
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute("BEGIN")
            await database.execute(
                """DELETE FROM conversation_messages
                WHERE conversation_id = ?
                  AND EXISTS (SELECT 1 FROM conversations
                              WHERE id = ? AND (? IS NULL OR user_id = ?))""",
                (conversation_id, conversation_id, user_id, user_id),
            )
            cursor = await database.execute(
                "DELETE FROM conversations WHERE id = ? AND (? IS NULL OR user_id = ?)",
                (conversation_id, user_id, user_id),
            )
            await database.commit()
            return cursor.rowcount > 0

    async def create_user(self, user: dict[str, Any]) -> None:
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute("BEGIN")
            await database.execute(
                """
                INSERT INTO users (id, email, password_hash, full_name, created_at)
                VALUES (:id, :email, :password_hash, :full_name, :created_at)
                """,
                user,
            )
            await database.execute(
                "UPDATE documents SET user_id = :id WHERE user_id IS NULL",
                {"id": user["id"]},
            )
            await database.execute(
                "UPDATE conversations SET user_id = :id WHERE user_id IS NULL",
                {"id": user["id"]},
            )
            await database.commit()

    async def get_user_by_email(self, email: str) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                "SELECT id, email, password_hash, full_name, created_at FROM users WHERE lower(email) = lower(?)",
                (email.strip(),),
            )
            row = await cursor.fetchone()
            return dict(row) if row is not None else None

    async def get_user_by_id(self, user_id: str) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                "SELECT id, email, full_name, created_at FROM users WHERE id = ?",
                (user_id,),
            )
            row = await cursor.fetchone()
            return dict(row) if row is not None else None

    async def create_session(self, session: dict[str, Any]) -> None:
        async with aiosqlite.connect(self.database_path) as database:
            await database.execute(
                """
                INSERT INTO sessions (token, user_id, created_at, expires_at)
                VALUES (:token, :user_id, :created_at, :expires_at)
                """,
                session,
            )
            await database.commit()

    async def get_session(self, token: str) -> dict[str, Any] | None:
        async with aiosqlite.connect(self.database_path) as database:
            database.row_factory = aiosqlite.Row
            cursor = await database.execute(
                """
                SELECT
                    sessions.token,
                    sessions.user_id,
                    sessions.expires_at,
                    users.email,
                    users.full_name,
                    users.created_at AS user_created_at
                FROM sessions
                JOIN users ON users.id = sessions.user_id
                WHERE sessions.token = ?
                """,
                (token,),
            )
            row = await cursor.fetchone()
            return dict(row) if row is not None else None

    async def delete_session(self, token: str) -> bool:
        async with aiosqlite.connect(self.database_path) as database:
            cursor = await database.execute("DELETE FROM sessions WHERE token = ?", (token,))
            await database.commit()
            return cursor.rowcount > 0
