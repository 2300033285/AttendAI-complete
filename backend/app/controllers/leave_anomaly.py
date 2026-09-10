from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.leave_anomaly_service import (
    detect_leave_anomalies
)


router = APIRouter(
    prefix="/leave-anomaly",
    tags=["Leave Anomaly"],
    dependencies=[
        Depends(require_roles(["Admin"]))
    ],
)


@router.get("/{employee_id}")
def leave_anomaly(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return detect_leave_anomalies(
        db=db,
        employee_id=employee_id,
    )