from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.models.user import User

from app.schemas.ai_prediction import AIPredictionResponse
from app.services.ai_prediction_service import ai_prediction_service


router = APIRouter(
    prefix="/ai-prediction",
    tags=["AI Prediction"]
)


@router.get(
    "/",
    response_model=AIPredictionResponse,
    summary="AI Attendance Prediction"
)
def get_ai_prediction_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user_email = current_user.get("sub")

    if user_email is None:
        raise HTTPException(
            status_code=401,
            detail="User email missing from authentication token"
        )

    user = (
        db.query(User)
        .filter(User.email == user_email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return ai_prediction_service(
        db=db,
        user_id=user.id
    )