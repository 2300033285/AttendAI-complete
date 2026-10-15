
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.assistant import (
    AssistantChatRequest,
    AssistantChatResponse,
)
from app.security import get_current_user
from app.services.assistant_service import assistant_chat_service

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=AssistantChatResponse)
def chat_with_assistant(
    request: AssistantChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    email = current_user.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="User email missing from authentication token.",
        )

    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Authenticated user not found.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive.",
        )

    return assistant_chat_service(
        db=db,
        user=user,
        message=request.message.strip(),
        conversation_id=request.conversation_id,
    )
