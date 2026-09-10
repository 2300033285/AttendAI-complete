from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.services.leave_ai_features_service import (
    get_leave_ai_features,
)


router = APIRouter(
    prefix="/leave-ai",
    tags=["Leave AI"],
    dependencies=[
        Depends(require_roles(["Admin"]))
    ],
)


@router.get("/features/{employee_id}")
def leave_ai_features(
    employee_id: int,
    db: Session = Depends(get_db),
):
    return get_leave_ai_features(
        db=db,
        employee_id=employee_id,
    )