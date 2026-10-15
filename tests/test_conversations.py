import asyncio
import json
import uuid
from datetime import UTC, datetime

import aiosqlite

from app.database import DocumentDatabase


def test_conversation_and_messages_survive_database_reopen(tmp_path) -> None:
    database_path = tmp_path / "documind.sqlite3"
    document_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    async def exercise_database() -> None:
        database = DocumentDatabase(database_path)
        await database.initialize()
        await database.add_document(
            {
                "id": document_id,
                "filename": "handbook.pdf",
                "title": "handbook",
                "page_count": 3,
                "chunk_count": 4,
                "created_at": now,
                "file_path": str(tmp_path / "handbook.pdf"),
            }
        )
        await database.create_conversation(
            {
                "id": conversation_id,
                "document_id": document_id,
                "title": "New chat",
                "created_at": now,
                "updated_at": now,
            }
        )
        await database.add_conversation_message(
            {
                "conversation_id": conversation_id,
                "role": "user",
                "content": "What is the main policy?",
                "sources": "[]",
                "created_at": now,
            }
        )
        await database.add_conversation_message(
            {
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": "The policy covers access control.",
                "sources": json.dumps([{"page": 2, "excerpt": "Access control"}]),
                "created_at": now,
            }
        )

        reopened_database = DocumentDatabase(database_path)
        conversation = await reopened_database.get_conversation(conversation_id)
        messages = await reopened_database.get_conversation_messages(conversation_id)
        listed = await reopened_database.list_conversations()

        assert conversation is not None
        assert conversation["title"] == "What is the main policy?"
        assert len(messages) == 2
        assert json.loads(messages[1]["sources"]) == [{"page": 2, "excerpt": "Access control"}]
        assert listed[0]["id"] == conversation_id
        assert listed[0]["document_filename"] == "handbook.pdf"
        assert await reopened_database.delete_conversation(conversation_id)
        assert await reopened_database.get_conversation(conversation_id) is None

    asyncio.run(exercise_database())


def test_deleting_document_removes_its_saved_chats(tmp_path) -> None:
    database = DocumentDatabase(tmp_path / "documind.sqlite3")
    document_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    async def exercise_database() -> None:
        await database.initialize()
        await database.add_document(
            {
                "id": document_id,
                "filename": "notes.pdf",
                "title": "notes",
                "page_count": 1,
                "chunk_count": 1,
                "created_at": now,
                "file_path": str(tmp_path / "notes.pdf"),
            }
        )
        await database.create_conversation(
            {
                "id": conversation_id,
                "document_id": document_id,
                "title": "New chat",
                "created_at": now,
                "updated_at": now,
            }
        )

        assert await database.delete_document(document_id)
        assert await database.get_conversation(conversation_id) is None
        assert await database.list_conversations() == []

    asyncio.run(exercise_database())


def test_legacy_database_migrates_and_assigns_existing_rows_to_first_user(tmp_path) -> None:
    database_path = tmp_path / "legacy.sqlite3"
    document_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()

    async def exercise_migration() -> None:
        async with aiosqlite.connect(database_path) as legacy:
            await legacy.execute(
                """
                CREATE TABLE documents (
                    id TEXT PRIMARY KEY,
                    filename TEXT NOT NULL,
                    title TEXT NOT NULL,
                    page_count INTEGER NOT NULL,
                    chunk_count INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    file_path TEXT NOT NULL
                )
                """
            )
            await legacy.execute(
                """
                CREATE TABLE conversations (
                    id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            await legacy.execute(
                """
                INSERT INTO documents
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (document_id, "old.pdf", "old", 1, 1, now, "old.pdf"),
            )
            await legacy.execute(
                """
                INSERT INTO conversations
                VALUES (?, ?, ?, ?, ?)
                """,
                (conversation_id, document_id, "Old chat", now, now),
            )
            await legacy.commit()

        database = DocumentDatabase(database_path)
        await database.initialize()
        await database.create_user(
            {
                "id": "first-user",
                "email": "first@example.com",
                "password_hash": "test-hash",
                "full_name": "First User",
                "created_at": now,
            }
        )

        assert len(await database.list_documents(user_id="first-user")) == 1
        assert await database.list_documents(user_id="other-user") == []
        conversations = await database.list_conversations(user_id="first-user")
        assert [item["id"] for item in conversations] == [conversation_id]
        assert await database.list_conversations(user_id="other-user") == []

    asyncio.run(exercise_migration())
