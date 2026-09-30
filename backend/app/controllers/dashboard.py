from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user
from app.schemas.dashboard import (
    AdminDashboardResponse,
    EmployeeDashboardResponse,
)
from app.services.dashboard_service import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=Union[
        AdminDashboardResponse,
        EmployeeDashboardResponse,
    ],
    status_code=status.HTTP_200_OK,
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    dashboard_data, error = dashboard_service(
        db=db,
        current_user=current_user,
    )

    if error:

        if error in [
            "Employee profile is not linked to this user.",
            "Invalid employee ID associated with this user.",
            "User ID is missing from token.",
            "Employee profile not found.",
        ]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error,
            )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error,
        )

    return dashboard_data