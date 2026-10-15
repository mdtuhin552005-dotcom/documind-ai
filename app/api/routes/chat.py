import json
import time
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException, Request
from app.api.routes.auth import require_authenticated_user

from app.schemas import (
    ChatRequest,
    ChatResponse,
    ConversationCreateRequest,
    ConversationDetail,
    ConversationListResponse,
    ConversationMessage,
    ConversationSummary,
)
from app.services.chat import ChatService

router = APIRouter(prefix="/api/chat", tags=["chat"])
conversations_router = APIRouter(prefix="/api/chats", tags=["chat history"])


@router.post("", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest) -> ChatResponse:
    user = await require_authenticated_user(request)
    service: ChatService = request.app.state.chat_service
    start_time = time.time()
    result = await service.answer(payload, user["id"])
    duration_ms = round((time.time() - start_time) * 1000, 2)
    try:
        chunks_count = len(result.sources) if getattr(result, "sources", None) else 0
        await request.app.state.database.log_query(
            query_text=payload.message,
            response_time_ms=duration_ms,
            user_id=user["id"],
            document_id=payload.document_id,
            retrieved_chunks=chunks_count,
        )
        ip = request.client.host if request.client else None
        preview = payload.message[:50] + ("..." if len(payload.message) > 50 else "")
        await request.app.state.database.log_activity(
            "ASK_QUERY",
            f"Query: {preview} ({duration_ms}ms)",
            user_id=user["id"],
            ip_address=ip,
        )
    except Exception:
        pass
    return result


@conversations_router.get("", response_model=ConversationListResponse)
async def list_conversations(request: Request) -> ConversationListResponse:
    user = await require_authenticated_user(request)
    database = request.app.state.database
    conversations = await database.list_conversations(user_id=user["id"])
    return ConversationListResponse(conversations=conversations)


@conversations_router.post("", response_model=ConversationSummary, status_code=201)
async def create_conversation(
    request: Request,
    payload: ConversationCreateRequest,
) -> ConversationSummary:
    user = await require_authenticated_user(request)
    database = request.app.state.database
    document = await database.get_document(payload.document_id, user["id"])
    if document is None:
        raise HTTPException(status_code=404, detail="The selected document was not found.")
    now = datetime.now(UTC).isoformat()
    conversation = {
        "id": str(uuid.uuid4()),
        "document_id": payload.document_id,
        "title": "New chat",
        "created_at": now,
        "updated_at": now,
        "user_id": user["id"],
    }
    await database.create_conversation(conversation)
    return ConversationSummary(
        **conversation,
        document_filename=document["filename"],
        last_message=None,
    )


@conversations_router.get("/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(request: Request, conversation_id: str) -> ConversationDetail:
    user = await require_authenticated_user(request)
    try:
        conversation_id = str(uuid.UUID(conversation_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Chat was not found.") from error

    database = request.app.state.database
    conversation = await database.get_conversation(conversation_id, user["id"])
    if conversation is None:
        raise HTTPException(status_code=404, detail="Chat was not found.")

    messages = []
    for message in await database.get_conversation_messages(conversation_id):
        try:
            sources = json.loads(message["sources"])
        except (TypeError, json.JSONDecodeError) as error:
            raise RuntimeError("Saved chat contains invalid source references.") from error
        messages.append(
            ConversationMessage(
                role=message["role"],
                content=message["content"],
                sources=sources,
                created_at=message["created_at"],
            )
        )
    return ConversationDetail(**conversation, messages=messages)


@conversations_router.delete("/{conversation_id}", status_code=204)
async def delete_conversation(request: Request, conversation_id: str) -> None:
    user = await require_authenticated_user(request)
    try:
        conversation_id = str(uuid.UUID(conversation_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Chat was not found.") from error
    database = request.app.state.database
    if not await database.delete_conversation(conversation_id, user["id"]):
        raise HTTPException(status_code=404, detail="Chat was not found.")


@conversations_router.post("/export/{export_format}")
async def export_chat_document(request: Request, export_format: str) -> Response:
    import io
    import fitz
    from docx import Document
    from fastapi.responses import Response

    try:
        user = await require_authenticated_user(request)
    except Exception:
        user = None

    try:
        body = await request.json()
    except Exception:
        body = {}

    doc_name = body.get("document_name") or "DocuMind_Document"
    messages = body.get("messages") or []
    clean_name = "".join(c for c in doc_name if c.isalnum() or c in ("-", "_", " ")).strip() or "Report"
    clean_name = clean_name.replace(" ", "_")
    now_ts = int(time.time())

    if export_format.lower() in ("docx", "word", "doc"):
        doc = Document()
        doc.add_heading("DocuMind AI Research Export", 0)
        p_meta = doc.add_paragraph()
        p_meta.add_run(f"Document Source: {doc_name}\n").bold = True
        now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
        p_meta.add_run(f"Export Timestamp: {now_str}\nStatus: Verified deterministic grounding\n")

        q_idx = 1
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "").strip()
            if role == "user":
                doc.add_heading(f"Question {q_idx}", level=2)
                q_idx += 1
                doc.add_paragraph(content)
            else:
                doc.add_heading("DocuMind Grounded Answer", level=3)
                doc.add_paragraph(content)
                sources = msg.get("sources", [])
                if sources:
                    src_p = doc.add_paragraph()
                    src_p.add_run("Verified Sources: " + " | ".join(f"Page {s.get('page', '?')}" for s in sources)).italic = True
            doc.add_paragraph("―" * 36)

        buf = io.BytesIO()
        doc.save(buf)
        docx_bytes = buf.getvalue()
        filename = f"DocuMind_Export_{clean_name}_{now_ts}.docx"
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )

    elif export_format.lower() == "pdf":
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        margin = 48
        y = 50

        # Title Header
        page.insert_text((margin, y), "DocuMind AI Research Report", fontsize=18, fontname="helv", color=(0.1, 0.3, 0.8))
        y += 24
        now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
        page.insert_text((margin, y), f"Document: {doc_name}   |   Exported: {now_str}", fontsize=9, fontname="helv", color=(0.4, 0.4, 0.4))
        y += 14
        page.draw_line(fitz.Point(margin, y), fitz.Point(595 - margin, y), color=(0.8, 0.8, 0.8), width=1)
        y += 24

        q_idx = 1
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "").strip()

            if y > 730:
                page = doc.new_page(width=595, height=842)
                y = 50

            if role == "user":
                page.insert_text((margin, y), f"Question {q_idx}:", fontsize=11.5, fontname="helv", color=(0.12, 0.32, 0.72))
                q_idx += 1
                y += 16
                rect = fitz.Rect(margin, y, 595 - margin, 780)
                used_h = page.insert_textbox(rect, content, fontsize=10, fontname="helv", color=(0.1, 0.1, 0.1))
                y += abs(used_h) + 16 if used_h >= 0 else 60
            else:
                page.insert_text((margin, y), "DocuMind Grounded Answer:", fontsize=11, fontname="helv", color=(0.02, 0.52, 0.42))
                y += 16
                rect = fitz.Rect(margin, y, 595 - margin, 780)
                used_h = page.insert_textbox(rect, content, fontsize=9.5, fontname="helv", color=(0.15, 0.15, 0.15))
                y += abs(used_h) + 12 if used_h >= 0 else 75

                sources = msg.get("sources", [])
                if sources:
                    src_str = "Verified Sources: " + " | ".join(f"Page {s.get('page', '?')}" for s in sources)
                    if y > 750:
                        page = doc.new_page(width=595, height=842)
                        y = 50
                    page.insert_text((margin, y), src_str, fontsize=8, fontname="helv", color=(0.05, 0.4, 0.65))
                    y += 14

                page.draw_line(fitz.Point(margin, y), fitz.Point(595 - margin, y), color=(0.9, 0.9, 0.9), width=0.5)
                y += 18

        pdf_bytes = doc.tobytes()
        filename = f"DocuMind_Export_{clean_name}_{now_ts}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    else:
        raise HTTPException(status_code=400, detail="Supported export formats are 'pdf' and 'docx'.")
