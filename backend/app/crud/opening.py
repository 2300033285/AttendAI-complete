from sqlalchemy.orm import Session

from app.models.opening import Opening
from app.schemas.opening import OpeningCreate, OpeningUpdate


def create_opening(
    db: Session,
    opening: OpeningCreate,
):
    db_opening = Opening(
        job_title=opening.job_title,
        department=opening.department,
        location=opening.location,
        employment_type=opening.employment_type,
        description=opening.description,
        requirements=opening.requirements,
        experience=opening.experience,
        status=opening.status,
    )

    db.add(db_opening)
    db.commit()
    db.refresh(db_opening)

    return db_opening


def get_all_openings(
    db: Session,
):
    return (
        db.query(Opening)
        .order_by(Opening.created_at.desc())
        .all()
    )


def get_opening_by_id(
    db: Session,
    opening_id: int,
):
    return (
        db.query(Opening)
        .filter(Opening.id == opening_id)
        .first()
    )


def update_opening(
    db: Session,
    opening_id: int,
    opening: OpeningUpdate,
):
    db_opening = get_opening_by_id(
        db,
        opening_id,
    )

    if db_opening is None:
        return None

    update_data = opening.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            db_opening,
            field,
            value,
        )

    db.commit()
    db.refresh(db_opening)

    return db_opening


def delete_opening(
    db: Session,
    opening_id: int,
):
    db_opening = get_opening_by_id(
        db,
        opening_id,
    )

    if db_opening is None:
        return None

    db.delete(db_opening)
    db.commit()

    return db_opening