from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.crud.shift import (
    create_shift,
    get_all_shifts,
    get_shift_by_id,
    update_shift,
    delete_shift,
)
from app.schemas.shift import ShiftCreate, ShiftUpdate


def create_shift_service(
    db: Session,
    shift: ShiftCreate
):
    # Start and end cannot be exactly the same
    if shift.start_time == shift.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time and end time cannot be the same",
        )

    # Check duplicate shift name
    existing_shifts = get_all_shifts(db)

    for existing_shift in existing_shifts:
        if (
            existing_shift.shift_name.strip().lower()
            == shift.shift_name.strip().lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift with this name already exists",
            )

    return create_shift(db, shift)


def get_all_shifts_service(db: Session):
    return get_all_shifts(db)


def get_shift_by_id_service(
    db: Session,
    shift_id: int
):
    return get_shift_by_id(db, shift_id)


def update_shift_service(
    db: Session,
    shift_id: int,
    shift: ShiftUpdate
):
    existing_shift = get_shift_by_id(db, shift_id)

    if not existing_shift:
        return None

    # Start and end cannot be exactly the same
    if shift.start_time == shift.end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time and end time cannot be the same",
        )

    # Check duplicate shift name
    existing_shifts = get_all_shifts(db)

    for other_shift in existing_shifts:
        if other_shift.id == shift_id:
            continue

        if (
            other_shift.shift_name.strip().lower()
            == shift.shift_name.strip().lower()
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Shift with this name already exists",
            )

    return update_shift(db, shift_id, shift)


def delete_shift_service(
    db: Session,
    shift_id: int
):
    return delete_shift(db, shift_id)