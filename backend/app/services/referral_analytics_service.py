from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.referral import Referral


def get_referral_analytics(db: Session):

    total_referrals = (
        db.query(func.count(Referral.id))
        .scalar()
        or 0
    )

    pending_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Pending")
        .scalar()
        or 0
    )

    reviewed_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Reviewed")
        .scalar()
        or 0
    )

    rejected_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Rejected")
        .scalar()
        or 0
    )

    selected_referrals = (
        db.query(func.count(Referral.id))
        .filter(Referral.status == "Selected")
        .scalar()
        or 0
    )

    return {
        "total_referrals": total_referrals,
        "pending_referrals": pending_referrals,
        "reviewed_referrals": reviewed_referrals,
        "rejected_referrals": rejected_referrals,
        "selected_referrals": selected_referrals,
    }


# =====================================================
# OPENING-WISE REFERRAL ANALYTICS
# =====================================================

def get_opening_wise_referrals(db: Session):

    results = (
        db.query(
            Referral.opening_id,
            func.count(Referral.id).label("referral_count")
        )
        .group_by(Referral.opening_id)
        .order_by(Referral.opening_id)
        .all()
    )

    return [
        {
            "opening_id": opening_id,
            "referral_count": referral_count
        }
        for opening_id, referral_count in results
    ]

# =====================================================
# EMPLOYEE-WISE REFERRAL ANALYTICS
# =====================================================

def get_employee_wise_referrals(db: Session):

    results = (
        db.query(
            Referral.employee_id,
            func.count(Referral.id).label("referral_count")
        )
        .group_by(Referral.employee_id)
        .order_by(Referral.employee_id)
        .all()
    )

    return [
        {
            "employee_id": employee_id,
            "referral_count": referral_count
        }
        for employee_id, referral_count in results
    ]