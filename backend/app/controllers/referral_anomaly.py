from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.referral_anomaly_service import (
    detect_referral_anomalies
)

from app.schemas.referral_anomaly import (
    ReferralAnomalyResponse
)


router = APIRouter(
    prefix="/referral-anomaly",
    tags=["Referral Anomaly"]
)


@router.get(
    "/{employee_id}",
    response_model=ReferralAnomalyResponse
)
def referral_anomaly(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    )
):
    return detect_referral_anomalies(
        db=db,
        employee_id=employee_id
    )