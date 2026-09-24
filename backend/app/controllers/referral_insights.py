from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.referral_insights_service import (
    get_referral_insights
)

from app.schemas.referral_insights import (
    ReferralInsightsResponse
)


router = APIRouter(
    prefix="/referral-insights",
    tags=["Referral Insights"]
)


@router.get(
    "/",
    response_model=ReferralInsightsResponse
)
def referral_insights(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    )
):
    return get_referral_insights(db)