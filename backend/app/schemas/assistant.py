from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AssistantChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: UUID | None = None


class AssistantChatResponse(BaseModel):
    conversation_id: UUID
    answer: str
    provider: str = "Gemini"
    model: str


class AssistantMessageResponse(BaseModel):
    id: int
    conversation_id: UUID
    role: Literal["user", "model"]
    content: str
    created_at: str | None = None

    model_config = ConfigDict(from_attributes=True)