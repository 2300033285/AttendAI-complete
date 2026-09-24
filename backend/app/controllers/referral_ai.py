from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.referral_ai_service import (
    get_referral_ai_analysis
)

from app.schemas.referral_ai import (
    ReferralAIResponse
)


router = APIRouter(
    prefix="/referral-ai",
    tags=["Referral AI"]
)


@router.get(
    "/{employee_id}",
    response_model=ReferralAIResponse
)
def referral_ai_analysis(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    )
):
    return get_referral_ai_analysis(
        db=db,
        employee_id=employee_id
    )