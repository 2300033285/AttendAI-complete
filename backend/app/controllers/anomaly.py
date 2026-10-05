from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.schemas.anomaly import (
    AnomalyResponse,
    EmployeeAnomalyResponse,
)

from app.services.anomaly_service import (
    anomaly_service,
    employee_anomaly_service,
)


router = APIRouter(
    prefix="/anomalies",
    tags=["Anomaly Detection"],
)


@router.get(
    "/",
    response_model=AnomalyResponse,
    summary="Get Attendance Anomalies",
    description="Returns attendance anomalies detected from attendance records. Admin access only.",
)
def get_anomalies_api(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return anomaly_service(db)


@router.get(
    "/employee/{employee_id}",
    response_model=EmployeeAnomalyResponse,
    summary="Get Employee Anomalies",
    description=(
        "Returns attendance, leave, and referral anomalies "
        "for a specific employee. Admin access only."
    ),
)
def get_employee_anomalies_api(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    result = employee_anomaly_service(
        db=db,
        employee_id=employee_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return result