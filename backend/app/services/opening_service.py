from sqlalchemy.orm import Session

from app.crud.opening import (
    create_opening,
    get_all_openings,
    get_opening_by_id,
    update_opening,
    delete_opening,
)

from app.schemas.opening import (
    OpeningCreate,
    OpeningUpdate,
)


def create_opening_service(
    db: Session,
    opening: OpeningCreate,
):
    if not opening.job_title.strip():
        return None, "Job title is required."

    if not opening.department.strip():
        return None, "Department is required."

    if not opening.location.strip():
        return None, "Location is required."

    if not opening.description.strip():
        return None, "Description is required."

    if opening.status not in ["Open", "Closed", "Draft"]:
        return None, "Status must be Open, Closed, or Draft."

    created_opening = create_opening(
        db,
        opening,
    )

    return created_opening, None


def get_all_openings_service(
    db: Session,
):
    return get_all_openings(db)


def get_opening_service(
    db: Session,
    opening_id: int,
):
    return get_opening_by_id(
        db,
        opening_id,
    )


def update_opening_service(
    db: Session,
    opening_id: int,
    opening: OpeningUpdate,
):
    existing_opening = get_opening_by_id(
        db,
        opening_id,
    )

    if existing_opening is None:
        return None, "Opening not found."

    if (
        opening.status is not None
        and opening.status not in ["Open", "Closed", "Draft"]
    ):
        return None, "Status must be Open, Closed, or Draft."

    updated_opening = update_opening(
        db,
        opening_id,
        opening,
    )

    return updated_opening, None


def delete_opening_service(
    db: Session,
    opening_id: int,
):
    existing_opening = get_opening_by_id(
        db,
        opening_id,
    )

    if existing_opening is None:
        return None, "Opening not found."

    deleted_opening = delete_opening(
        db,
        opening_id,
    )

    return deleted_opening, None