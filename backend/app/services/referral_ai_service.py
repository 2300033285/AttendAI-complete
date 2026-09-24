from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.referral import Referral


def get_referral_ai_analysis(
    db: Session,
    employee_id: int
):

    total_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.employee_id == employee_id)
        .scalar()
        or 0
    )

    selected_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Selected"
        )
        .scalar()
        or 0
    )

    rejected_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Rejected"
        )
        .scalar()
        or 0
    )

    reviewed_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Reviewed"
        )
        .scalar()
        or 0
    )

    pending_referrals = (
        db.query(func.count(Referral.id))
        .filter(
            Referral.employee_id == employee_id,
            Referral.status == "Pending"
        )
        .scalar()
        or 0
    )

    # Calculate rates
    if total_referrals > 0:
        selection_rate = round(
            (selected_referrals / total_referrals) * 100,
            2
        )

        rejection_rate = round(
            (rejected_referrals / total_referrals) * 100,
            2
        )

        review_rate = round(
            (reviewed_referrals / total_referrals) * 100,
            2
        )
    else:
        selection_rate = 0
        rejection_rate = 0
        review_rate = 0

    # AI-ready performance category
    if total_referrals == 0:
        performance_category = "No Referral Activity"

    elif selection_rate >= 50:
        performance_category = "High Selection"

    elif selection_rate > 0:
        performance_category = "Moderate Selection"

    elif pending_referrals == total_referrals:
        performance_category = "Pending Review"

    else:
        performance_category = "Low Selection"

    return {
        "employee_id": employee_id,
        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "reviewed_referrals": reviewed_referrals,
        "rejected_referrals": rejected_referrals,
        "selected_referrals": selected_referrals,
        "selection_rate": selection_rate,
        "rejection_rate": rejection_rate,
        "review_rate": review_rate,
        "performance_category": performance_category
    }