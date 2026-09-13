from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.leave_insights_service import (
    get_leave_insights_service
)


router = APIRouter(
    prefix="/leave-insights",
    tags=["Leave Insights"],
    dependencies=[
        Depends(require_roles(["Admin"]))
    ],
)


@router.get("/{employee_id}")
def leave_insights(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_leave_insights_service(
        db=db,
        employee_id=employee_id,
    )