from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import get_current_user, require_roles

from app.schemas.shift import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse,
)

from app.services.shift_service import (
    create_shift_service,
    get_all_shifts_service,
    get_shift_by_id_service,
    update_shift_service,
    delete_shift_service,
)


router = APIRouter(
    prefix="/shifts",
    tags=["Shifts"],
)


@router.post(
    "/",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Shift",
)
def create_shift_api(
    shift: ShiftCreate,
    current_user=Depends(
        require_roles(["Admin", "HR", "Manager"])
    ),
    db: Session = Depends(get_db),
):
    return create_shift_service(db, shift)


@router.get(
    "/",
    response_model=List[ShiftResponse],
    summary="Get All Shifts",
)
def get_all_shifts_api(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_all_shifts_service(db)


@router.get(
    "/{shift_id}",
    response_model=ShiftResponse,
    summary="Get Shift By ID",
)
def get_shift_by_id_api(
    shift_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    shift = get_shift_by_id_service(db, shift_id)

    if not shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    return shift


@router.put(
    "/{shift_id}",
    response_model=ShiftResponse,
    summary="Update Shift",
)
def update_shift_api(
    shift_id: int,
    shift: ShiftUpdate,
    current_user=Depends(
        require_roles(["Admin", "HR", "Manager"])
    ),
    db: Session = Depends(get_db),
):
    updated_shift = update_shift_service(
        db,
        shift_id,
        shift,
    )

    if not updated_shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    return updated_shift


@router.delete(
    "/{shift_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Shift",
)
def delete_shift_api(
    shift_id: int,
    current_user=Depends(
        require_roles(["Admin"])
    ),
    db: Session = Depends(get_db),
):
    deleted_shift = delete_shift_service(
        db,
        shift_id,
    )

    if not deleted_shift:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shift not found",
        )

    return {
        "message": "Shift deleted successfully"
    }