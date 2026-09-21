from sqlalchemy.orm import Session

from app.crud.referral import (
    create_referral,
    get_all_referrals,
    get_referral_by_id,
    get_referrals_by_employee,
    update_referral,
    delete_referral,
)

from app.models.employee import Employee
from app.models.opening import Opening
from app.models.referral import Referral

from app.schemas.referral import (
    ReferralCreate,
    ReferralUpdate,
)


ALLOWED_STATUSES = [
    "Pending",
    "Reviewed",
    "Accepted",
    "Rejected",
]


# =====================================================
# CREATE REFERRAL
# =====================================================

def create_referral_service(
    db: Session,
    referral: ReferralCreate,
    employee_id: int,
):
    # Check employee exists
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        return None, "Employee not found."

    # Check job opening exists
    opening = (
        db.query(Opening)
        .filter(Opening.id == referral.opening_id)
        .first()
    )

    if opening is None:
        return None, "Job opening not found."

    # Only open jobs can receive referrals
    if opening.status != "Open":
        return (
            None,
            "Referrals can only be submitted for open job openings.",
        )

    # Validate candidate name
    if not referral.candidate_name.strip():
        return None, "Candidate name is required."

    # Validate candidate phone
    if not referral.candidate_phone.strip():
        return None, "Candidate phone is required."

    # Prevent duplicate referral
    # for the same candidate and opening
    existing_referral = (
        db.query(Referral)
        .filter(
            Referral.opening_id == referral.opening_id,
            Referral.candidate_email == referral.candidate_email,
        )
        .first()
    )

    if existing_referral:
        return (
            None,
            "This candidate has already been referred for this opening.",
        )

    # Create referral
    created_referral = create_referral(
        db=db,
        referral=referral,
        employee_id=employee_id,
    )

    return created_referral, None


# =====================================================
# GET ALL REFERRALS
# =====================================================

def get_all_referrals_service(
    db: Session,
):
    return get_all_referrals(db)


# =====================================================
# GET REFERRAL BY ID
# =====================================================

def get_referral_service(
    db: Session,
    referral_id: int,
):
    return get_referral_by_id(
        db=db,
        referral_id=referral_id,
    )


# =====================================================
# GET EMPLOYEE REFERRALS
# =====================================================

def get_employee_referrals_service(
    db: Session,
    employee_id: int,
):
    return get_referrals_by_employee(
        db=db,
        employee_id=employee_id,
    )


# =====================================================
# UPDATE REFERRAL
# =====================================================

def update_referral_service(
    db: Session,
    referral_id: int,
    referral: ReferralUpdate,
):
    # Check referral exists
    existing_referral = get_referral_by_id(
        db=db,
        referral_id=referral_id,
    )

    if existing_referral is None:
        return None, "Referral not found."

    # Validate status
    if (
        referral.status is not None
        and referral.status not in ALLOWED_STATUSES
    ):
        return (
            None,
            "Status must be Pending, Reviewed, Accepted, or Rejected.",
        )

    # Validate candidate name
    if (
        referral.candidate_name is not None
        and not referral.candidate_name.strip()
    ):
        return None, "Candidate name cannot be empty."

    # Validate candidate phone
    if (
        referral.candidate_phone is not None
        and not referral.candidate_phone.strip()
    ):
        return None, "Candidate phone cannot be empty."

    # Update referral
    updated_referral = update_referral(
        db=db,
        referral_id=referral_id,
        referral=referral,
    )

    return updated_referral, None


# =====================================================
# DELETE REFERRAL
# =====================================================

def delete_referral_service(
    db: Session,
    referral_id: int,
):
    # Check referral exists
    existing_referral = get_referral_by_id(
        db=db,
        referral_id=referral_id,
    )

    if existing_referral is None:
        return None, "Referral not found."

    # Delete referral
    deleted_referral = delete_referral(
        db=db,
        referral_id=referral_id,
    )

    return deleted_referral, None