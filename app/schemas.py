from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    title: str
    page_count: int
    chunk_count: int
    created_at: datetime


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=3000)


class ChatRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=64)
    chat_id: str | None = Field(default=None, min_length=1, max_length=64)
    question: str = Field(min_length=1, max_length=4000)
    history: list[ChatTurn] = Field(default_factory=list, max_length=12)


class SourceReference(BaseModel):
    page: int
    excerpt: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceReference]


class ConversationCreateRequest(BaseModel):
    document_id: str = Field(min_length=1, max_length=64)


class ConversationSummary(BaseModel):
    id: str
    document_id: str
    document_filename: str
    title: str
    created_at: datetime
    updated_at: datetime
    last_message: str | None = None


class ConversationListResponse(BaseModel):
    conversations: list[ConversationSummary]


class ConversationMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    sources: list[SourceReference] = Field(default_factory=list)
    created_at: datetime


class ConversationDetail(ConversationSummary):
    messages: list[ConversationMessage]


class HealthResponse(BaseModel):
    status: Literal["ok"]
    ai_configured: bool


class UserRegisterRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=6, max_length=128)
    full_name: str = Field(min_length=1, max_length=128)


class UserLoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=128)


class GoogleCredentialRequest(BaseModel):
    credential: str = Field(min_length=1, max_length=8192)


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: str


class AuthResponse(BaseModel):
    user: UserResponse
    token: str
    message: str


class DocumentSummaryResponse(BaseModel):
    document_id: str
    summary: str
    key_takeaways: list[str]
    estimated_read_time_minutes: int
