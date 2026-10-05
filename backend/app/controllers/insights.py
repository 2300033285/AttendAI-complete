from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import require_roles

from app.schemas.insights import InsightsResponse
from app.services.insights_service import insights_service

router = APIRouter(
    prefix="/insights",
    tags=["Insights"],
)


@router.get(
    "/",
    response_model=InsightsResponse,
    summary="Organization Insights",
)
def get_insights_api(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(["Admin"])
    ),
):
    return insights_service(db)