from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.referral_analytics_service import (
    get_referral_analytics,
    get_opening_wise_referrals,
    get_employee_wise_referrals,
)

from app.schemas.referral_analytics import (
    ReferralAnalyticsResponse,
    OpeningReferralAnalytics,
    EmployeeReferralAnalytics,
)


router = APIRouter(
    prefix="/referral-analytics",
    tags=["Referral Analytics"]
)


# =====================================================
# OVERALL REFERRAL ANALYTICS
# =====================================================

@router.get(
    "/",
    response_model=ReferralAnalyticsResponse
)
def referral_analytics(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return get_referral_analytics(db)


# =====================================================
# OPENING-WISE REFERRAL ANALYTICS
# =====================================================

@router.get(
    "/opening-wise",
    response_model=List[OpeningReferralAnalytics]
)
def opening_wise_referrals(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return get_opening_wise_referrals(db)


# =====================================================
# EMPLOYEE-WISE REFERRAL ANALYTICS
# =====================================================

@router.get(
    "/employee-wise",
    response_model=List[EmployeeReferralAnalytics]
)
def employee_wise_referrals(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return get_employee_wise_referrals(db)