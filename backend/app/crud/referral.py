from sqlalchemy.orm import Session

from app.models.referral import Referral
from app.schemas.referral import ReferralCreate, ReferralUpdate


def create_referral(
    db: Session,
    referral: ReferralCreate,
    employee_id: int,
):
    db_referral = Referral(
        employee_id=employee_id,
        opening_id=referral.opening_id,
        candidate_name=referral.candidate_name,
        candidate_email=referral.candidate_email,
        candidate_phone=referral.candidate_phone,
        resume_url=referral.resume_url,
        referral_message=referral.referral_message,
        status="Pending",
    )

    db.add(db_referral)
    db.commit()
    db.refresh(db_referral)

    return db_referral


def get_all_referrals(db: Session):
    return (
        db.query(Referral)
        .order_by(Referral.created_at.desc())
        .all()
    )


def get_referral_by_id(
    db: Session,
    referral_id: int,
):
    return (
        db.query(Referral)
        .filter(Referral.id == referral_id)
        .first()
    )


def get_referrals_by_employee(
    db: Session,
    employee_id: int,
):
    return (
        db.query(Referral)
        .filter(Referral.employee_id == employee_id)
        .order_by(Referral.created_at.desc())
        .all()
    )


def update_referral(
    db: Session,
    referral_id: int,
    referral: ReferralUpdate,
):
    db_referral = get_referral_by_id(
        db=db,
        referral_id=referral_id,
    )

    if db_referral is None:
        return None

    update_data = referral.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(db_referral, field, value)

    db.commit()
    db.refresh(db_referral)

    return db_referral


def delete_referral(
    db: Session,
    referral_id: int,
):
    db_referral = get_referral_by_id(
        db=db,
        referral_id=referral_id,
    )

    if db_referral is None:
        return None

    db.delete(db_referral)
    db.commit()

    return db_referral