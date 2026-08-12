from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.schemas.shift import ShiftCreate, ShiftUpdate


def create_shift(db: Session, shift: ShiftCreate):
    new_shift = Shift(
        shift_name=shift.shift_name,
        start_time=shift.start_time,
        end_time=shift.end_time,
        status=shift.status,
    )

    db.add(new_shift)
    db.commit()
    db.refresh(new_shift)

    return new_shift


def get_all_shifts(db: Session):
    return db.query(Shift).all()


def get_shift_by_id(db: Session, shift_id: int):
    return (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )


def update_shift(
    db: Session,
    shift_id: int,
    shift: ShiftUpdate
):
    db_shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not db_shift:
        return None

    update_data = shift.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_shift, key, value)

    db.commit()
    db.refresh(db_shift)

    return db_shift


def delete_shift(db: Session, shift_id: int):
    db_shift = (
        db.query(Shift)
        .filter(Shift.id == shift_id)
        .first()
    )

    if not db_shift:
        return None

    db.delete(db_shift)
    db.commit()

    return db_shift